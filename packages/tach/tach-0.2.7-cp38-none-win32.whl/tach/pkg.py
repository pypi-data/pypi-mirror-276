from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

from tach import errors
from tach import filesystem as fs
from tach.colors import BCOLORS
from tach.constants import CONFIG_FILE_NAME, PACKAGE_FILE_NAME, TOOL_NAME
from tach.core import ProjectConfig
from tach.interactive import SelectedPackage, get_selected_packages_interactive
from tach.parsing import dump_project_config_to_yaml

__package_yml_template = """tags: ['{dir_name}']\n"""


@dataclass
class SetPackagesResult:
    package_paths: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def set_packages(
    selected_packages: list[SelectedPackage],
    path: str,
    exclude_paths: Optional[list[str]] = None,
) -> SetPackagesResult:
    package_paths: list[str] = []
    warnings: list[str] = []

    for existing_package, package_yml_path in fs.walk_configured_packages(
        root=path, exclude_paths=exclude_paths
    ):
        # If this package was not selected, we should delete the package.yml
        if not any(
            fs.canonical(selected_package.full_path) == fs.canonical(existing_package)
            for selected_package in selected_packages
        ):
            fs.delete_file(package_yml_path)

    for selected_package in selected_packages:
        init_py_path = os.path.join(selected_package.full_path, "__init__.py")
        if not os.path.exists(init_py_path):
            warnings.append(
                f"{BCOLORS.OKCYAN}Created __init__.py in selected package: '{selected_package.full_path}'{BCOLORS.ENDC}"
            )
            fs.write_file(init_py_path, f"# Generated by '{TOOL_NAME} init'")
        package_yml_path = os.path.join(
            selected_package.full_path, f"{PACKAGE_FILE_NAME}.yml"
        )
        package_paths.append(selected_package.full_path)
        if os.path.exists(package_yml_path):
            warnings.append(
                f"{BCOLORS.OKCYAN}Package file '{package_yml_path}' already exists.{BCOLORS.ENDC}"
            )
            continue
        package_yml_content = __package_yml_template.format(
            dir_name=fs.canonical(selected_package.full_path).replace(os.path.sep, ".")
        )
        fs.write_file(package_yml_path, package_yml_content)

    return SetPackagesResult(package_paths=package_paths, warnings=warnings)


@dataclass
class InitRootResult:
    warnings: list[str] = field(default_factory=list)


def init_root(root: str) -> InitRootResult:
    project_config_path = fs.get_project_config_path(root)
    if project_config_path:
        return InitRootResult(
            warnings=[
                f"{BCOLORS.OKCYAN}Project already contains {CONFIG_FILE_NAME}.yml{BCOLORS.ENDC}"
            ]
        )

    # Initialize an empty/default project configuration
    project_config = ProjectConfig()
    project_config_path = os.path.join(root, f"{CONFIG_FILE_NAME}.yml")
    config_yml_content = dump_project_config_to_yaml(project_config)
    fs.write_file(project_config_path, config_yml_content)

    return InitRootResult(warnings=[])


def pkg_edit_interactive(
    root: str, depth: Optional[int] = 1, exclude_paths: Optional[list[str]] = None
) -> tuple[bool, list[str]]:
    if not os.path.isdir(root):
        raise errors.TachSetupError(f"The path {root} is not a directory.")

    if exclude_paths is None:
        exclude_paths = ["tests/", "docs/"]

    warnings: list[str] = []

    # We only want to auto-select if the project appears not to have been configured already
    auto_select_initial_packages = fs.get_project_config_path(root) == ""
    selected_packages = get_selected_packages_interactive(
        root,
        depth=depth,
        exclude_paths=exclude_paths,
        auto_select_initial_packages=auto_select_initial_packages,
    )
    if selected_packages is not None:
        set_packages_result = set_packages(
            selected_packages=selected_packages, path=root, exclude_paths=exclude_paths
        )
        warnings.extend(set_packages_result.warnings)

        init_root_result = init_root(root)
        warnings.extend(init_root_result.warnings)
    else:
        return False, [f"{BCOLORS.OKCYAN}No changes saved.{BCOLORS.ENDC}"]

    return True, warnings
