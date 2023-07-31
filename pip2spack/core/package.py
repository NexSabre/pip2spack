import os
from dataclasses import dataclass
from typing import List

from pip2spack.core.pypi_package import PyPiPackage
from pip2spack.core.spack_repository import SpackRepository
from pip2spack.framework import constants as constants
from pip2spack.framework.messages import Messages


@dataclass
class Package:
    package_name: str
    package_path: str
    _raw_package: str

    versions: List
    modification_package: List

    def __post_init__(self):
        self.package_path = SpackRepository().get_package_path(
            package_name=self.package_name
        )
        self._open()

    def _open(self):
        with open(self.package_path, "r") as package_py:
            self._raw_package = package_py.read()

    def replace_structure_with_marker(self):
        self.modification_package = self._raw_package.split("\n")
        if not isinstance(self.modification_package, list):
            raise

        rows_with_version = []
        for index, content in enumerate(self.modification_package):
            if "version(" in content:
                rows_with_version.append((index, content.lstrip().rstrip()))

        rows_with_version.reverse()  # start removing an empty rows from bottom file
        for index, row in enumerate(rows_with_version):
            if index == 0:
                self.modification_package[row[0]] = self.modification_package[
                    row[0]
                ].replace(row[1], constants.MARKER_VERSION)
            else:
                del self.modification_package[row[0]]

        self.replace_marker_with_template()

    def replace_marker_with_template(self):
        rows_with_version = []
        for index, content in enumerate(self.modification_package):
            if constants.MARKER_VERSION in content:
                rows_with_version.append(index)

        if not [x for x in self.modification_package if constants.MARKER_VERSION in x]:
            Messages.error(
                f"{self.package_name} :: pip2spack can not find a 'version' tag.\n\t"
                f" Please create a new package with:\n\t"
                f"  pip2spack create {self.package_name}"
            )
            return

        rows_with_version.reverse()  # start removing an empty rows from bottom file
        for index, row in enumerate(rows_with_version):
            if index == 0:
                spaces = self._count_trailing_spaces(self.modification_package[row])
                self.modification_package[row] = self.modification_package[row].replace(
                    constants.MARKER_VERSION, constants.marker_version_template(spaces)
                )
            else:
                break

        self.generate_modded_package(save=True)
        if not self.save(self.update_newest_versions(self.package_name)):
            Messages.error(
                f"Something went wrong, package {self.package_name} was not updated"
            )
        else:
            Messages.ok(
                f"{self.package_name} :: builtin package was updated at {self.package_path}"
            )

    def update_newest_versions(self, package_name):
        sp = PyPiPackage(package_name)
        file = sp.generate_custom_file(
            os.path.dirname(os.path.realpath(self.package_path)), sp._get_versions
        )
        return file

    def save(self, new_file):
        with open(self.package_path, "w") as package:
            package.write(new_file)
            return True

    def generate_modded_package(self, save: bool = False):
        if not save:
            return "\n".join(self.modification_package).lstrip()
        self.save("\n".join(self.modification_package).lstrip())

    @staticmethod
    def available_markers(marker_name):
        return {"version": constants.MARKER_VERSION}.get(marker_name, None)

    @staticmethod
    def _count_trailing_spaces(sentence) -> int:
        return len(sentence) - len(sentence.lstrip())
