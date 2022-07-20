from pip2spack.actions.action import Action
from pip2spack.core.pypi_package import PyPiPackage
from pip2spack.core.verification import Verification
from pip2spack.framework.helpers import create_directory, create_package
from pip2spack.framework.messages import Messages


class CreateAction(Action):
    ACTION = "create"
    PARAM_NAME = "ACTION"

    def fill_parser_arguments(self):
        self.parser.add_argument(
            "name", type=str, nargs="+", help="Package name on the pypi.org"
        )

    def process_action(self, configuration):
        ready_packages = Verification(configuration.name).available_packages
        self.generate_packages(ready_packages)

    @staticmethod
    def generate_packages(ready_packages):
        for key, value in ready_packages.items():
            Messages.info(f"Generating package for the {key}")

            s_package = PyPiPackage(value)
            generated_file = s_package.generate_file()

            create_directory(key)
            created_package_uri = create_package(key, generated_file)
            print(
                f" OK  :: Package for {key} was generated\n\t "
                f":: If 'spack install py-{key}' return any problems, try to uncomment:\n\t "
                f":: \tdepends_on('py-setuptools', type='build')\n\t "
                f":: at {created_package_uri}"
            )
