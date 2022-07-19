from unittest import TestCase

from src.pip2spack.core.pypi_package import PyPiPackage
from tests.old_tests.test_data import test_data as ready_packages


class TestSpackPackage(TestCase):
    def setUp(self) -> None:
        self.spack = PyPiPackage(ready_packages["jsl"])

    def test_package_name_builder(self):
        package_name = self.spack.package_name_builder()
        self.assertEqual("PyJsl", package_name)

    def test_package_name_builder_replace_dash(self):
        self.spack.content["info"]["name"] = "jsl-up"
        package_name = self.spack.package_name_builder()
        self.assertEqual("PyJslUp", package_name)

    def test_generator_is_not_null(self):
        return_message = self.spack._generate_data()
        for key, value in return_message.items():
            if key in ("depends_on_setuptools",):
                continue
            self.assertTrue(value, msg=f"{key} is not true")
