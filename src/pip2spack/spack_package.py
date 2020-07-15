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
        self.url = self.content["urls"][0]["url"]

    def _homepage(self):
        self.homepage = self.content['home_page']

    def _versions_formatter(self):
        for version, version_content in self.content['releases'].items():
            try:
                # TODO Not support .whl packages yet. Only source code in .tar.gz
                if not version_content[0]['filename'].endswith('.tar.gz'):
                    continue
                self.versions.append(
                    (str(version), str(version_content[0]['digests']['sha256']))
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
