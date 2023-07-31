from typing import List

from pip2spack.core.package import Package
from pip2spack.core.verification import Verification


def update_action(names: List[str]) -> None:
    package_names = Verification(names).available_packages

    if isinstance(package_names, dict):
        package_names = [k for k, v in package_names.items()]

    for p_name in package_names:
        package = Package(package_name=p_name)
        package.replace_structure_with_marker()
        package.generate_modded_package()
