import json

import requests

from pip2spack.framework.messages import Messages


class Verification:
    def __init__(self, arguments: list):
        self.__ready_packages = self.validate_pip_package_exists(arguments)
        self.show_packages_for_process(self.__ready_packages, arguments)

    @property
    def available_packages(self):
        return self.__ready_packages

    @staticmethod
    def validate_pip_package_exists(potential_packages):
        if not potential_packages:
            return

        packages_status = {}
        for package in potential_packages:
            status = requests.get(f"https://pypi.org/pypi/{package}/json")
            if status.status_code != 200:
                continue
            packages_status[package] = json.loads(status.content)
        return packages_status

    @staticmethod
    def show_packages_for_process(package_ready, all_packages):
        """Display at the terminal a information about arability of provided package names"""
        packages_not_found = [x for x in all_packages if x not in package_ready]
        packages_found = [k for k, v in package_ready.items()]
        Messages.package_availability(packages_found, packages_not_found)
