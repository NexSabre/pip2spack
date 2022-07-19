from dataclasses import dataclass
from os import getenv, listdir
from os.path import abspath, exists, join, relpath
from typing import AnyStr

from pip2spack.framework.constants import BUILTIN_REPOSITORY_REL_PATH
from pip2spack.framework.messages import Messages


@dataclass
class SpackRepository:
    _spack_root: str = getenv("SPACK_ROOT", None)
    _builtin_repository: str = (
        f"{join(_spack_root, relpath(BUILTIN_REPOSITORY_REL_PATH))}"
        if _spack_root
        else ""
    )

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
        if not package_name.startswith("py-"):
            package_name = "py-" + package_name
        package_py_path: str = join(
            *(f"{self.builtin_repository}", package_name, "package.py")
        )
        if not self.exists(package_name) or not exists(package_py_path):
            # TODO create a new one
            Messages.warn(
                f"Package {package_name} does not exist in the builtin repository"
            )
            raise
        return abspath(package_py_path)
