from pip2spack.core.pypi_package import PyPiPackage
from pip2spack.core.verification import Verification
from pip2spack.framework.messages import Messages


def download_action(name: str):
    ready_packages = Verification(
        [
            name,
        ]
    ).available_packages
    for key, value in ready_packages.items():
        Messages.info(f"Download latest package for the {key}")

        d_package = PyPiPackage(value)
        d_package.download_versions()
