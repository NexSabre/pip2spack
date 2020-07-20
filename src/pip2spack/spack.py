import os
from dataclasses import dataclass
from os import getenv, listdir
from os.path import exists, join, relpath, abspath
from typing import AnyStr

import constants
from constants import BUILDIN_REPOSITORY_REL_PATH
from spack_package import SpackPackage


@dataclass
class Spack:
    _spack_root: str = getenv("SPACK_ROOT", None)
    _builtin_repository: str = f'{join(_spack_root, relpath(BUILDIN_REPOSITORY_REL_PATH))}' if _spack_root else ""

    @property
    def directory(self):
        return self._spack_root

    @directory.setter
    def directory(self, custom_spack_root):
        if not exists(custom_spack_root):
            raise
        self._spack_root = custom_spack_root

    @property
    def builtin_repository(self):
        return self._builtin_repository

    def list_all_packages(self):
        return listdir(self.builtin_repository)

    def list_py_packages(self):
        return [x for x in self.list_all_packages() if x.startswith("py-")]

    def exists(self, package_name: str, python_only: bool = True) -> bool:
        if python_only:
            return package_name in self.list_py_packages()
        else:
            return package_name in self.list_all_packages()

    def get_package_path(self, package_name: str) -> AnyStr:
        """Return absolute path to the package.py if exists in builtin repository"""
        if not package_name.startswith('py-'):
            package_name = "py-" + package_name
        package_py_path: str = join(*(f"{self.builtin_repository}", package_name, "package.py"))
        if not self.exists(package_name) or not exists(package_py_path):
            # TODO create a new one
            print(f"Package {package_name} does not exist in the builtin repository")
            raise
        return abspath(package_py_path)


@dataclass
class Package:
    package_name: AnyStr
    package_path: AnyStr = None
    _raw_package: AnyStr = None

    versions = []

    def __post_init__(self):
        s = Spack()
        self.package_path = s.get_package_path(package_name=self.package_name)
        self._open()

    def _open(self):
        with open(self.package_path, 'r') as package_py:
            self._raw_package = package_py.read()

    def replace_structure_with_marker(self):
        self.modificated_package = self._raw_package.split('\n')
        if not isinstance(self.modificated_package, list):
            raise

        rows_with_version = []
        for index, content in enumerate(self.modificated_package):
            if "version(" in content:
                rows_with_version.append((index, content.lstrip().rstrip()))

        rows_with_version.reverse()  # start removing a empty rows from bottom file
        for index, row in enumerate(rows_with_version):
            if index == 0:
                self.modificated_package[row[0]] = self.modificated_package[row[0]].replace(row[1],
                                                                                            constants.MARKER_VERSION)
            else:
                del self.modificated_package[row[0]]

        self.replace_marker_with_template()

    def replace_marker_with_template(self):
        rows_with_version = []
        for index, content in enumerate(self.modificated_package):
            if constants.MARKER_VERSION in content:
                rows_with_version.append(index)
        rows_with_version.reverse()  # start removing a empty rows from bottom file
        for index, row in enumerate(rows_with_version):
            if index == 0:
                spaces = self._count_trailing_spaces(self.modificated_package[row])
                self.modificated_package[row] = \
                    self.modificated_package[row].replace(constants.MARKER_VERSION,
                                                          constants.marker_version_template(spaces))
            else:
                break
        self.generate_modded_package(save=True)
        if not self.save(self.update_newest_versions(self.package_name)):
            print(f"ERRR:: Something went wrong, package {self.package_name} was not updated")
        else:
            print(f" OK :: {self.package_name} :: builtin package was updated at {self.package_path}")

    def update_newest_versions(self, package_name):
        sp = SpackPackage(package_name)
        file = sp.generate_custom_file(os.path.dirname(os.path.realpath(self.package_path)), sp.get_versions)
        return file

    def save(self, new_file):
        with open(self.package_path, 'w') as package:
            package.write(new_file)
            return True

    def generate_modded_package(self, save: bool = False):
        if not save:
            return '\n'.join(self.modificated_package).lstrip()
        self.save('\n'.join(self.modificated_package).lstrip())

    @staticmethod
    def available_markers(marker_name):
        return {"version": constants.MARKER_VERSION}.get(marker_name, None)

    @staticmethod
    def _count_trailing_spaces(sentence) -> int:
        return len(sentence) - len(sentence.lstrip())


if __name__ == "__main__":
    # TODO generate tests base on this queries
    package = Package(package_name="py-codecov")
    print(package.replace_structure_with_marker())
    print(package.generate_modded_package())
