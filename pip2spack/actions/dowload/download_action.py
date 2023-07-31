from typing import List

from pip2spack.core.pypi_package import PyPiPackage
from pip2spack.core.verification import Verification
from pip2spack.framework.messages import Messages


# TODO @NexSabre add parameter for specific version download
def download_action(names: List[str]):
    ready_packages = Verification(names).available_packages
    for key, value in ready_packages.items():
        Messages.info(f"Download latest package for the {key}")

        d_package = PyPiPackage(key)
        d_package.download_versions()
