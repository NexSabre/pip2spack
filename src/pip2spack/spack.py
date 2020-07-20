from dataclasses import dataclass
from os import getenv, listdir
from os.path import exists, join, relpath, abspath
from typing import AnyStr

import constants
from constants import BUILDIN_REPOSITORY_REL_PATH


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
        package_py_path: str = join(*(f"{self.builtin_repository}", package_name, "package.py"))
        if not self.exists(package_name) or not exists(package_py_path):
            # TODO create a new one
            print(f"Package {package_name} does not exist in the builtin repository")
            raise
        return abspath(package_py_path)


@dataclass
class Package:
    package_path: AnyStr
    _package_name: AnyStr = None
    _raw_package: AnyStr = None

    versions = []

    def _open(self):
        with open(self.package_path, 'r') as package_py:
            self._raw_package = package_py.read()

    def replace_structure_with_marker(self, ):
        self.modificated_package = self._raw_package.split('\n')
        if not isinstance(self.modificated_package, list):
            raise

        rows_with_version = []
        for index, content in enumerate(self.modificated_package):
            if "version(" in content:
                rows_with_version.append((index, content.lstrip().rstrip()))

        print(rows_with_version)
        for row in rows_with_version:
            self.modificated_package[row[0]] = self.modificated_package[row[0]].replace(row[1],
                                                                                        constants.MARKER_VERSION)

    def generate_modificated_package(self, save: bool = False):
        if not save:
            return '\n'.join(self.modificated_package).lstrip()

    @staticmethod
    def available_markers(marker_name):
        return {"version": constants.MARKER_VERSION}.get(marker_name, None)

    @staticmethod
    def _count_trailing_spaces(sentence) -> int:
        return len(sentence) - len(sentence.lstrip())


if __name__ == "__main__":
    # TODO generate tests base on this queries
    spack = Spack()
    print(spack.builtin_repository)
    print(spack.list_py_packages())
    print(spack.exists("py-adal"))
    print(spack.get_package_path("py-adal"))

    package = Package(package_path=spack.get_package_path("py-adal"))
    package._open()
    print(package._raw_package)
    print(package.available_markers("version"))
    print(package._count_trailing_spaces("    version"))
    print(package.replace_structure_with_marker())
