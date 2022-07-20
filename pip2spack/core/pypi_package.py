import json
from typing import Any, Dict, List

import requests
from jinja2 import Environment, FileSystemLoader, PackageLoader

from pip2spack.framework.messages import Messages


class PyPiPackage:
    content: dict = {}
    versions: list = []
    url: str = ""
    homepage: str = ""
    maintainers: list = []
    package_name: str = ""
    summary: str = ""
    source: bool = False

    def __init__(self, content):
        self.content = self._download_missing_information(content)

        self._url(source=self.__detect_approach())

        if self.source:
            self._versions_formatter()
        else:
            self._wheel_versions_formatter()
        self.version_builder()

        self.package_name_builder()
        self.summary_builder()
        self.homepage_builder()

    @property
    def _get_versions(self):
        self.versions = []
        self._versions_formatter()
        self.version_builder()
        return self.versions

    def __detect_approach(self) -> bool:
        return True if self.content["urls"][0]["url"].endswith(".tar.gz") else False

    @staticmethod
    def _download_missing_information(package_name: str) -> Dict[str, Any]:
        if package_name.startswith("py-"):
            package_name = package_name.replace("py-", "")
        status = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        if status.status_code != 200:
            print("Package doesnt not exist at PyPi.org")
            raise
        return json.loads(status.content)

    def _url(self, source):
        def _generate_pypi_uri(filename_with_version):
            if not filename_with_version:
                raise Exception("Can not generate a proper master link to the package")
            return (
                f"https://pypi.io/packages/source/{filename_with_version[0]}/"
                f'{"-".join(filename_with_version.split("-")[:-1])}/{filename_with_version}'
            )

        if source:
            for url in self.content["urls"]:
                if url["url"].endswith(".tar.gz"):
                    self.url = _generate_pypi_uri(url["url"].split("/")[-1])
                    self.source = True
                    break
        else:
            # preferable packages are .tar.gz, but some author does not include it, they just provide .whl package
            for u in self.content["urls"]:
                if u["url"].endswith(".whl"):
                    self.url = u["url"]
                    self.source = False
                    break

        if not self.url:
            raise Exception("Source package was not found")

        elif self.url and not self.source:
            print("[Experimental] Using a wheel package...")

    def _homepage(self):
        self.homepage = self.content["home_page"]

    def _versions_formatter(self):
        for version, version_content in self.content["releases"].items():
            only_sdist_version = [
                x
                for x in version_content
                if (x["url"].endswith(".tar.gz") and x["packagetype"] == "sdist")
            ]
            if not only_sdist_version:
                continue

            for proper_version in only_sdist_version:
                try:
                    # TODO Not support .whl packages yet. Only source code in .tar.gz
                    if not proper_version["filename"].endswith(".tar.gz"):
                        continue
                    self.versions.append(
                        (str(version), str(proper_version["digests"]["sha256"]))
                    )
                except IndexError:
                    continue

    def _wheel_versions_formatter(self):
        # TODO: Experimental support of the .whl. It can be pulled out if creates more cons than props
        for version, version_content in self.content["releases"].items():
            only_bdist_wheel_version = [
                x
                for x in version_content
                if (x["url"].endswith(".whl") and x["packagetype"] == "bdist_wheel")
            ]

            for proper_version in only_bdist_wheel_version:
                try:
                    if not proper_version["filename"].endswith(".whl"):
                        continue
                    self.versions.append(
                        (str(version), str(proper_version["digests"]["sha256"]))
                    )
                except IndexError:
                    continue

    def version_builder(self) -> str:
        raw_versions: str = ""
        for v in self.versions:
            raw_versions += f'version("{str(v[0])}", sha256="{str(v[1])}")\n'
        return raw_versions

    def package_name_builder(self) -> str:
        name = self.content["info"]["name"]
        if name[0].islower():
            name = name[0].upper() + name[1:]

        l_name = list(name)
        for i in [index for index, element in enumerate(l_name) if element == "-"]:
            try:
                if l_name[i + 1].islower():
                    l_name[i + 1] = l_name[i + 1].upper()
            except Exception as e:
                Messages.error(f"package_name_builder: {e}")
            finally:
                name = "".join(l_name).replace("-", "")

        if not name.startswith("Py"):
            name = "Py" + name
        self.package_name = name
        return name

    def summary_builder(self):
        self.summary = self.content["info"]["summary"]

    def homepage_builder(self):
        self.homepage = self.content["info"]["project_urls"]["Homepage"]

    def _generate_data(self) -> dict:
        return {
            "package_name": self.package_name,
            "summary": self.summary,
            "homepage": self.homepage,
            "url": self.url,
            "versions": self.versions,
            "depends_on_setuptools": False,
        }

    def generate_file(self):
        env = Environment(loader=PackageLoader("pip2spack", "templates"))
        template = env.get_template("package.j2")
        return template.render(**self._generate_data())

    @staticmethod
    def generate_custom_file(abspath: str, versions):
        env = Environment(loader=FileSystemLoader(abspath))
        template = env.get_template("package.py")
        return template.render({"versions": versions})

    def download_versions(self, versions: List = None):
        if not versions:
            latest_version = self.content["info"]["version"]
            latest_filename = self.content["releases"].get(latest_version)[0][
                "filename"
            ]
            Messages.warn(
                f"Missing versions parameter, downloading a latest one v{latest_version}"
            )
            r = requests.get(url=self.url)
            self.__save_content(latest_filename, r.content)

    @staticmethod
    def __save_content(name: str, content: bytes):
        import os
        import tempfile

        path = tempfile.gettempdir()
        pip2spack = os.path.join(path, "pip2spack")
        content_filename = os.path.join(pip2spack, name)
        os.makedirs(pip2spack, exist_ok=True)

        with open(content_filename, "wb") as content_to_save:
            content_to_save.write(content)
            Messages.info(f"Content was saved into {content_filename}")
