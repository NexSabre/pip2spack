from unittest import TestCase

from main import SpackPackage
from test_data import test_data as ready_packages


class TestSpackPackage(TestCase):
    def setUp(self) -> None:
        self.spack = SpackPackage(ready_packages["jsl"])

    def test_package_name_builder(self):
        package_name = self.spack.package_name_builder()
        self.assertEqual("PyJsl", package_name)

    def test_package_name_builder_replace_dash(self):
        self.spack.content['info']['name'] = "jsl-up"
        package_name = self.spack.package_name_builder()
        self.assertEqual("PyJslUp", package_name)
