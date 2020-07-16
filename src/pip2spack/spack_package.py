from jinja2 import Environment, PackageLoader, select_autoescape


class SpackPackage:
    content: dict = {}
    versions: list = []
    url: str = ""
    homepage: str = ""
    maintainers: list = []
    package_name: str = ''
    summary: str = ''

    def __init__(self, content):
        self.content = content
        self._url()

        self._versions_formatter()
        self.version_builder()

        self.package_name_builder()
        self.summary_builder()
        self.homepage_builder()

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
            only_sdist_version = [x for x in version_content if (x["url"].endswith(".tar.gz") and x["packagetype"] == "sdist")]
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
        env = Environment(loader=PackageLoader('pip2spack', 'templates'),
                          autoescape=select_autoescape(['j2']))
        template = env.get_template('package.py')
        return template.render(**self._generate_data())
