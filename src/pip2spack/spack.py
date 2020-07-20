from dataclasses import dataclass
from os import getenv, listdir
from os.path import exists, join, relpath

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


if __name__ == "__main__":
    # TODO generate tests base on this queries
    spack = Spack()
    print(spack.builtin_repository)
    print(spack.list_py_packages())
    print(spack.exists("py-adal"))
