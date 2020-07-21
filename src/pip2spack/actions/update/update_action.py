from pip2spack.actions.action import Action
from pip2spack.core.package import Package
from pip2spack.core.verification import Verification


class UpdateAction(Action):
    ACTION = "update"
    PARAM_NAME = "ACTION"

    def fill_parser_arguments(self):
        self.parser.add_argument('name', type=str, nargs='+', help='Package name on the pypi.org')

    def process_action(self, configuration):
        ready_packages = Verification(configuration.name).available_packages
        self.update_packages(ready_packages)

    @staticmethod
    def update_packages(package_names):
        if isinstance(package_names, dict):
            package_names = [k for k, v in package_names.items()]

        for p_name in package_names:
            package = Package(package_name=p_name)
            package.replace_structure_with_marker()
            package.generate_modded_package()
