import json
from typing import List
from urllib.request import Request

import requests
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

from pip2spack.framework.messages import Messages


class PyPiPackage:
    content: dict = {}
    versions: list = []
    url: str = ""
    homepage: str = ""
    maintainers: list = []
    package_name: str = ''
    summary: str = ''

    def __init__(self, content):
        self.content = self._download_missing_information(content)
        self._url()

        self._versions_formatter()
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

    @staticmethod
    def _download_missing_information(content):
        if isinstance(content, str):
            if content.startswith('py-'):
                content = content.replace("py-", '')
            status = requests.get(f'https://pypi.org/pypi/{content}/json')
            if status.status_code != 200:
                print("Package doesnt not exist at PyPi.org")
                raise
            return json.loads(status.content)
        else:
            return content

    def _url(self):
        def _generate_pypi_uri(filename_with_version):
            return f'https://pypi.io/packages/source/{filename_with_version[0]}/' \
                   f'{filename_with_version.split("-")[0]}/{filename_with_version}'

        latest_filename: str = ''
        for url in self.content["urls"]:
            if url["url"].endswith(".tar.gz"):
                latest_filename = url["url"].split('/')[-1]
                break
        self.url = _generate_pypi_uri(latest_filename)

        if not self.url:
            print("Source package was not found")

    def _homepage(self):
        self.homepage = self.content['home_page']

    def _versions_formatter(self):
        for version, version_content in self.content['releases'].items():
            only_sdist_version = [x for x in version_content if
                                  (x["url"].endswith(".tar.gz") and x["packagetype"] == "sdist")]
            if not only_sdist_version:
                continue
            for proper_version in only_sdist_version:
                try:
                    # TODO Not support .whl packages yet. Only source code in .tar.gz
                    if not proper_version['filename'].endswith('.tar.gz'):
                        continue
                    self.versions.append(
                        (str(version), str(proper_version['digests']['sha256']))
                    )
                except IndexError:
                    continue

    def version_builder(self) -> str:
        raw_versions: str = ''
        for v in self.versions:
            raw_versions += f'version(\"{str(v[0])}\", sha256=\"{str(v[1])}\")\n'
        return raw_versions

    def package_name_builder(self) -> str:
        name = self.content['info']['name']
        if name[0].islower():
            name = name[0].upper() + name[1:]

        l_name = list(name)
        for i in [index for index, element in enumerate(l_name) if element == '-']:
            try:
                if l_name[i + 1].islower():
                    l_name[i + 1] = l_name[i + 1].upper()
            except:
                pass
            finally:
                name = ''.join(l_name).replace('-', '')

        if not name.startswith("Py"):
            name = "Py" + name
        self.package_name = name
        return name

    def summary_builder(self):
        self.summary = self.content['info']['summary']

    def homepage_builder(self):
        self.homepage = self.content['info']['project_urls']['Homepage']

    def _generate_data(self) -> dict:
        return {
            "package_name": self.package_name,
            "summary": self.summary,
            "homepage": self.homepage,
            "url": self.url,
            "versions": self.versions,
            "depends_on_setuptools": False
        }

    def generate_file(self):
        env = Environment(loader=PackageLoader('pip2spack', 'templates'))
        template = env.get_template('package.j2')
        return template.render(**self._generate_data())

    @staticmethod
    def generate_custom_file(abspath: str, versions):
        env = Environment(loader=FileSystemLoader(abspath))
        template = env.get_template('package.py')
        return template.render({"versions": versions})

    def download_versions(self, versions: List = None):
        if not versions:
            latest_version = self.content['info']['version']
            latest_filename = self.content['releases'].get(latest_version)[0]["filename"]
            Messages.warn(f"Missing versions parameter, downloading a latest one v{latest_version}")
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

        with open(content_filename, 'wb') as content_to_save:
            content_to_save.write(content)
            Messages.info(f"Content was saved into {content_filename}")
