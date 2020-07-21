import os
from dataclasses import dataclass
from typing import AnyStr

from pip2spack.core.spack_repository import SpackRepository
from pip2spack.framework import constants as constants
from pip2spack.framework.messages import Messages
from pip2spack.core.pypi_package import PyPiPackage


@dataclass
class Package:
    package_name: AnyStr
    package_path: AnyStr = None
    _raw_package: AnyStr = None

    versions = []

    def __post_init__(self):
        s = SpackRepository()
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

        if not [x for x in self.modificated_package if constants.MARKER_VERSION in x]:
            Messages.error(f"{self.package_name} :: pip2spack can not find a \'version\' tag.\n\t Please create a new package with:\n\t  pip2spack create {self.package_name}")
            return

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
            Messages.error(f"Something went wrong, package {self.package_name} was not updated")
        else:
            Messages.ok(f"{self.package_name} :: builtin package was updated at {self.package_path}")

    def update_newest_versions(self, package_name):
        sp = PyPiPackage(package_name)
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
