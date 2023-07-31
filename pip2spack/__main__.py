from typing import List

import typer
from typing_extensions import Annotated

from pip2spack.actions.create.create_action import create_action
from pip2spack.actions.dowload import download_action
from pip2spack.actions.update.update_action import update_action
from pip2spack.core.verification import Verification
from pip2spack.framework.helpers import get_spack_repository

app = typer.Typer()

PACKAGE_TYPE = Annotated[
    List[str], typer.Argument(help="Name of the package at pypi.org")
]


@app.command(help="Create a new package")
def create(names: PACKAGE_TYPE) -> None:
    get_spack_repository()
    create_action(names=names)


@app.command(help="Update an existing package name")
def update(names: PACKAGE_TYPE):
    get_spack_repository()
    update_action(names)


@app.command(help="Download package")
def download(names: PACKAGE_TYPE):
    get_spack_repository()
    download_action(names)


if __name__ == "__main__":
    app()
