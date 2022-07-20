import pytest
from pytest_mock import MockFixture

from tests.pip2spack.core.mocks import (
    PYPI_CONFIGSHELL_FB_RESPONSE_MOCK,
    PYPI_CTYPESGEN_RESPONSE_MOCK,
    PYPI_RESPONSES,
)


@pytest.fixture
def mock_pypi_configshell_fb_response(mocker: MockFixture) -> None:
    mocker.patch(
        "pip2spack.core.pypi_package.PyPiPackage._download_missing_information",
        return_value=PYPI_CONFIGSHELL_FB_RESPONSE_MOCK,
    )


@pytest.fixture
def mock_pypi_jsl_response(mocker: MockFixture) -> None:
    mocker.patch(
        "pip2spack.core.pypi_package.PyPiPackage._download_missing_information",
        return_value=PYPI_RESPONSES["jsl"],
    )


@pytest.fixture
def mock_pypi_ctypesgen_response(mocker: MockFixture) -> None:
    mocker.patch(
        "pip2spack.core.pypi_package.PyPiPackage._download_missing_information",
        return_value=PYPI_CTYPESGEN_RESPONSE_MOCK["ctypesgen"],
    )
