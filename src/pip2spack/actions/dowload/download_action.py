from pip2spack.actions.action import Action
from pip2spack.framework.messages import Messages
from pip2spack.core.pypi_package import PyPiPackage
from pip2spack.core.verification import Verification


class DownloadAction(Action):
    ACTION = "download"
    PARAM_NAME = "ACTION"

    def fill_parser_arguments(self):
        self.parser.add_argument('name', type=str, nargs='+', help='Package name on the pypi.org')

    def process_action(self, configuration):
        ready_packages = Verification(configuration.name).available_packages
        self.download(ready_packages)

    @staticmethod
    def download(ready_packages):
        for key, value in ready_packages.items():
            Messages.info(f"Download latest package for the {key}")

            d_package = PyPiPackage(value)
            d_package.download_versions()
