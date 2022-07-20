from pip2spack.core.pypi_package import PyPiPackage


class TestPyPiPackage:
    def test_pypi_package__generate_correct_path_for_package_with_dash_in_name(
        self, mock_pypi_configshell_fb_response: None
    ) -> None:
        """Base on the issue #16 https://github.com/NexSabre/pip2spack/issues/16"""
        assert (
            PyPiPackage("configshell-fb").url
            == "https://pypi.io/packages/source/c/configshell-fb/configshell-fb-1.1.29.tar.gz"
        )

    def test_pypi_package__verify_package_name_builder__configshell_fb(
        self, mock_pypi_configshell_fb_response: None
    ):
        assert PyPiPackage("configshell-fb").package_name_builder() == "PyConfigshellFb"

    def test_pypi_package__verify_package_name_builder__jsl(
        self, mock_pypi_jsl_response: None
    ) -> None:
        assert PyPiPackage("jsl").package_name_builder() == "PyJsl"

    def test_pypi_package__package_name_builder_should_replace_dash_in_the_info_name(
        self, mock_pypi_jsl_response: None
    ) -> None:
        package = PyPiPackage("jsl")
        package.content["info"]["name"] = "jsl-up"

        assert package.package_name_builder() == "PyJslUp"

    def test_pypi_package__test_generate_data_return_message(
        self, mock_pypi_jsl_response: None
    ) -> None:
        return_message = PyPiPackage("jsl")._generate_data()
        for k, v in return_message.items():
            if k == "depends_on_setuptools":
                continue
            assert v, "Should be True"

    def test_pypi_package__ctypesgen_should_be_categorized_as_not_source(
        self, mock_pypi_ctypesgen_response: None
    ) -> None:
        assert not PyPiPackage(
            "ctypesgen"
        ).source, (
            "Package should be tread as wheel package, source should be unavailable"
        )
