from unittest import TestCase

from pip2spack.core.pypi_package import PyPiPackage
from pip2spack.tests.test_data import test_data_ctypesgen as ready_packages


class Test_TestProblematicPackages(TestCase):
    def setUp(self) -> None:
        self.spack = PyPiPackage(ready_packages["ctypesgen"])

    def test_ctypesgen_should_be_categorized_as_not_source(self):
        self.assertFalse(self.spack.source, "Package should be tread as wheel package")

    def test_ctypesgen_should_contains_only_wheel_version(self):
        self.assertEqual(len(self.spack.versions), 6)