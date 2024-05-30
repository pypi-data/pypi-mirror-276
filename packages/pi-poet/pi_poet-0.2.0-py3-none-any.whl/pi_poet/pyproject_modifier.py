import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib as toml
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Self

MATCH_ALL = r"^.*$"

EXCLUDE_DIRS = ["__pycache__", ".vscode", ".git", "docker_staging"]


@dataclass
class PackageMatch:
    """
    A class to match a package and change the version
    Special variables:
        {package} - The source package name
        {version} - The source version
        {package.version} - The matching package version
        {package.path.relative} - The relative path to the package from src
        {package.path.absolute} - The absolute path to the package
    """

    package_regex: str  ## Regex of the package name to match, example: r"^mypackage.*$"
    version_regex: str = MATCH_ALL  ## Regex of what part of the version to change
    version_to: str = "{package.version}"  ## The new version to change to


@dataclass
class ToLocalMatch(PackageMatch):
    version_to: str = (
        '{develop = true, path = "{package.path.relative}"}'  ## The new version to change to
    )


@dataclass
class ToRemoteMatch(PackageMatch):
    version_to: str = "{package.version}"  ## The new version to change to


class BuildSystem(Enum):
    SETUPTOOLS = "setuptools"
    POETRY = "poetry"
    FLIT = "flit"
    HATCHLING = "hatchling"
    PDM = "pdm"


def _get_build_system(
    data: dict, search_for: BuildSystem = None, default: Any = None
) -> BuildSystem:
    for build_system in data["build-system"]["requires"]:
        v = None
        if "poetry-core" in build_system:
            v = BuildSystem.POETRY
        elif "setuptools" in build_system:
            v = BuildSystem.SETUPTOOLS
        elif "flit" in build_system:
            v = BuildSystem.FLIT
        elif "hatchling" in build_system:
            v = BuildSystem.HATCHLING
        elif "pdm" in build_system:
            v = BuildSystem.PDM
        if not search_for and v:
            return v
        if search_for and v == search_for:
            return v

    else:
        if default:
            return default
        raise ValueError(f"Unsupported build system: {build_system}")


@dataclass
class PyPackage:
    name: str  ## The name of the package
    version: str  ## The version of the package
    path: Path  ## The path to the pyproject.toml file
    dependencies: dict[str, Any] = field(default_factory=dict)  ## The dependencies of the package
    toml_data: dict[str, Any] = field(default_factory=dict)  ## The toml data of the package

    @staticmethod
    def get_dependencies(file_path) -> dict:
        with open(file_path, "rb") as file:
            data = toml.load(file)

        dependencies = {}
        if _get_build_system(data, BuildSystem.POETRY, None):
            # Extracting main dependencies
            if "dependencies" in data["tool"]["poetry"]:
                dependencies.update(data["tool"]["poetry"]["dependencies"])

            # Extracting dependencies in groups
            if "group" in data["tool"]["poetry"]:
                for group, group_data in data["tool"]["poetry"]["group"].items():
                    if "dependencies" in group_data:
                        dependencies.update(group_data["dependencies"])
        elif _get_build_system(data, BuildSystem.SETUPTOOLS, None) and "project" in data:
            if "dependencies" in data["project"]:
                dependencies.update({dep: None for dep in data["project"]["dependencies"]})

        return dependencies

    @staticmethod
    def from_path(path: str | Path) -> Self:
        path = Path(path).expanduser().resolve()
        with open(path, "rb") as fp:
            data = toml.load(fp)
        dependencies = PyPackage.get_dependencies(path)
        build = _get_build_system(data, BuildSystem.POETRY, None)
        if build == BuildSystem.POETRY:
            poetry = data["tool"]["poetry"]
            return PyPackage(
                name=poetry["name"],
                version=poetry["version"],
                path=path,
                dependencies=dependencies,
                toml_data=data,
            )
        else:
            try:
                proj = data["project"]
                return PyPackage(
                    name=proj["name"],
                    version=proj["version"],
                    path=path,
                    dependencies=dependencies,
                    toml_data=data,
                )
            except:
                print(f"Could not read the {path} file", file=sys.stderr)
                raise

    def __str__(self) -> str:
        return f"{self.name}=={self.version}"

    def __repr__(self) -> str:
        return str(self)

    def relative_to_package(self, other: Self) -> Path:
        """
        Get the relative path to the other package
        Args:
            other.path is the path to the pyproject.toml file
        Returns:
            The relative path to the other package
        """
        return Path(os.path.relpath(self.path, other.path.parent))

    def _rmlock(self, missing_ok: bool = True):
        """
        Remove the lock file for the package
        """
        lockfile = self.path.parent / "poetry.lock"
        if lockfile.exists():
            lockfile.unlink(missing_ok=missing_ok)


def _special_substitutions(s: str, pkg: PyPackage, other_pkg: PyPackage) -> str:
    """
    Perform special substitutions
    Args:
        s (str): The string to substitute
        pkg (PyPackage): The package to substitute
        other_pkg (PyPackage): The other package to substitute
    Returns:
        The substituted string
    """
    if "{package}" in s:
        s = s.replace("{package}", pkg.name)
    if "{version}" in s:
        s = s.replace("{version}", f'"{pkg.version}"')
    if "{package.version}" in s:
        s = s.replace("{package.version}", f'"{other_pkg.version}"')
    if "{package.path.relative}" in s:
        s = s.replace("{package.path.relative}", str(other_pkg.relative_to_package(pkg).parent))
    if "{package.path.absolute}" in s:
        s = s.replace("{package.path.absolute}", str(other_pkg.path.parent))
    return s


@dataclass
class Poet:
    src: Path
    pyproj: PyPackage = None
    ## The directory to search for other pyproject.toml files, for example, the workspace directory
    package_dir: Path = None
    ## The projects that are found in the package_dir
    packages: dict[str, PyPackage] = field(default_factory=dict)
    exclude_dirs: list[str] = field(default_factory=lambda: EXCLUDE_DIRS)

    def __post_init__(self):
        self.src = Path(self.src).expanduser().resolve()
        if not self.src.exists():
            raise FileNotFoundError(f"Could not find the file {self.src}")
        ## Verify that toml is readable
        with open(self.src, "rb") as fp:
            toml.load(fp)
        self.pyproj = PyPackage.from_path(self.src)
        if self.package_dir and not self.packages:
            self.package_dir = Path(self.package_dir).expanduser().resolve()
            tomls = self.find_pyproject_tomls(self.package_dir)
            self.packages = {proj.name: proj for proj in [PyPackage.from_path(f) for f in tomls]}

    @staticmethod
    def find_pyproject_tomls(
        base_directory: str | Path, exclude_dirs=None, file_match="pyproject.toml"
    ) -> list[Path]:
        pyproject_files = []
        base_directory = Path(base_directory).expanduser().resolve()

        for root, dirs, files in os.walk(base_directory):
            if exclude_dirs:
                dirs[:] = [d for d in dirs if d not in exclude_dirs]

            if file_match in files:
                pyproject_files.append(Path(os.path.join(root, file_match)))

        return pyproject_files

    @staticmethod
    def find_pyprojects(base_directory: str | Path, exclude_dirs=None) -> dict[str, PyPackage]:
        pyproject_files = Poet.find_pyproject_tomls(base_directory, exclude_dirs)
        return {proj.name: proj for proj in [PyPackage.from_path(f) for f in pyproject_files]}

    def convert_to_remote(
        self,
        match_patterns: list[PackageMatch],
        dest_file: str = None,
        in_place: bool = False,
        use_toml_sort: bool = True,
    ) -> list[tuple[str, str]]:
        return self._convert_to(
            match_patterns=match_patterns,
            dest_file=dest_file,
            in_place=in_place,
            use_toml_sort=use_toml_sort,
        )

    def convert_to_local(
        self,
        match_patterns: list[PackageMatch],
        dest_file: str = None,
        in_place: bool = False,
        use_toml_sort: bool = True,
    ) -> list[tuple[str, str]]:
        return self._convert_to(
            match_patterns=match_patterns,
            dest_file=dest_file,
            in_place=in_place,
            use_toml_sort=use_toml_sort,
        )

    def _convert_to(
        self,
        match_patterns: list[PackageMatch],
        dest_file: str = None,
        in_place: bool = False,
        use_toml_sort: bool = True,
    ) -> list[tuple[str, str]]:
        """
        Convert the pyproject.toml file and change particular packages to a different format
        Args:
            src_file (str | PyPackage): The source file to read from
            match_patterns (list[PackageMatch]): The patterns to match and change
            change_to (str): The new format to change the package to
            dest_file (str): The destination file to write to
            in_place (bool): Whether to write to the source file or not
            use_toml_sort (bool): Whether to sort the toml file or not
            only_primitive_types (bool): Whether to check if the previous package info is a primitive type
        """
        src_file = self.src
        pyproj = self.pyproj
        # Create a backup in case something goes wrong
        with tempfile.TemporaryDirectory() as tmpdirname:
            backup_file = shutil.copy(pyproj.path, tmpdirname)
        if dest_file is not None and in_place:
            raise ValueError("Only one of dest_file or in_place can be specified")
        if in_place:
            dest_file = pyproj.path
        if not in_place and not backup_file:
            raise ValueError("destination file is required when in_place is False")
        changes: list[tuple[str, str]] = []
        new_lines = []
        with open(pyproj.path) as fp:
            for line in fp:
                if not "=" in line:
                    new_lines.append(line)
                    continue
                sline = line.strip()
                package, previous_package_info = sline.split("=", maxsplit=1)
                package = package.strip()
                previous_package_info = previous_package_info.strip()

                new_value = ""
                matched = False

                for mp in match_patterns:
                    m = re.match(mp.package_regex, package)
                    if not m:
                        continue
                    package_name = m.group(0)
                    matched = True
                    try:
                        matched_package = self.packages[package_name]
                    except KeyError:
                        ## This package is not in the packages
                        ## This might be a package that is not in the workspace and isn't
                        ## a problem unless we are trying to do special substitutions
                        matched_package = None

                    new_value = re.sub(mp.version_regex, mp.version_to, previous_package_info)
                    ## Perform special replacements
                    new_value = _special_substitutions(
                        new_value, pkg=pyproj, other_pkg=matched_package
                    )

                if matched:
                    new_line = f"{package} = {new_value}\n"
                    if line != new_line:
                        changes.append((line, new_line))
                        line = new_line

                new_lines.append(line)
        if not changes:
            if use_toml_sort:
                run_bash_command(f"toml-sort {dest_file}")
            return changes
        try:
            ## write to a temporary file first
            with tempfile.NamedTemporaryFile("w", delete=False) as tmpfile:
                tmpfile.writelines(new_lines)
                tmpfile.close()
                shutil.copy(tmpfile.name, dest_file)
        except Exception as e:
            print(f"Error occurred: {e}", file=sys.stderr)
            raise

        if use_toml_sort:
            run_bash_command(f"toml-sort {dest_file}")
        return changes


def run_bash_command(
    command,
    output_file: str = None,
    error_file: str = None,
    cwd: str | Path = None,
    verbose: bool = True,
) -> bool:
    if cwd:
        cwd = str(cwd)
    try:
        # Run the command
        if verbose:
            print(f"Cmd: {command}, cwd={cwd}", flush=True)

        result = subprocess.run(
            command,
            shell=True,  # Use shell to run the command
            check=True,  # Raise an error if the command fails
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture standard error
            text=True,  # Decode output to string
            cwd=cwd,  # Change to the specified directory
        )
        if result.stdout and output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
            if verbose:
                print(f"Command Output: {result.stdout}")
        if result.stderr and error_file:
            with open(error_file, "w") as f:
                f.write(result.stderr)
            if verbose:
                print("Command Error Output:\n", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}", file=sys.stderr)
        print("Standard Output:", e.stdout, file=sys.stderr)
        print("Standard Error:", e.stderr, file=sys.stderr)
        return False


def _check_value_is_primitive(value):
    primitives = (bool, str, int, float, type(None))
    try:
        js = json.loads(value)
        if not isinstance(js, primitives):
            raise ValueError(
                f"Advanced types, i.e array or dict, are currently not supported. Got {js}"
            )
    except json.JSONDecodeError:
        print(f"Could not parse the package info: {value}", file=sys.stderr)
        raise


def custom_sort_dict(input_dict, order_list):
    # Create a helper function to provide the custom sort key
    def sort_key(key):
        if key in order_list:
            return (0, order_list.index(key))
        else:
            return (1, key)

    # Sort the dictionary keys using the custom sort key
    sorted_keys = sorted(input_dict.keys(), key=sort_key)

    # Create a new dictionary based on the sorted keys
    sorted_dict = {key: input_dict[key] for key in sorted_keys}

    return sorted_dict


def create_dag(packages: list[PyPackage]) -> dict[str, set[str]]:
    dag = {}
    for package in packages:
        if package.name not in dag:
            dag[package.name] = set()
        for dep in package.dependencies.keys():
            if dep not in dag:
                dag[dep] = set()
            dag[dep].add(package.name)
    return dag


def topological_sort(dag: dict[str, set[str]]) -> list[str]:
    def visit(node):
        if node in temp_mark:
            raise ValueError(f"Cycle detected: {node}")
        if node not in perm_mark:
            temp_mark.add(node)
            for neighbor in dag.get(node, []):
                visit(neighbor)
            temp_mark.remove(node)
            perm_mark.add(node)
            result.append(node)

    temp_mark = set()
    perm_mark = set()
    result = []

    for node in dag:
        if node not in perm_mark:
            visit(node)

    return result[::-1]  # reverse the result to get the correct order

