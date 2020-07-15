import json
import os
import argparse
import requests


def main():
    parser = argparse.ArgumentParser(description='Create a spack package base on:')
    parser.add_argument('name', type=str, nargs='+', help='Package name on the pypi.org')

    args = parser.parse_args()
    ready_packages = validate_pip_package_exists(args.name)
    show_packages_for_process(ready_packages, args.name)

    s_package = SpackPackage(ready_packages["jsl"])


def validate_pip_package_exists(potential_packages):
    if not potential_packages:
        return

    packages_status = {}
    for package in potential_packages:
        status = requests.get(f'https://pypi.org/pypi/{package}/json')
        if status.status_code != 200:
            continue
        packages_status[package] = json.loads(status.content)
    return packages_status


def show_packages_for_process(package_ready, all_packages):
    """Display at the terminal a information about arability of provided package names"""
    print("Packages ready to convert:")
    for key, _ in package_ready.items():
        print(f"\t{key}")

    packages_not_found = [x for x in all_packages if x not in package_ready]
    print("\nPackages not found:")
    for p in packages_not_found:
        print(f'\t{p}')


def get_spack_repository() -> str:
    """Return a absolute path about spack repository"""
    if not os.getenv("SPACK_ROOT", False):
        print('Please provide a information about SPACK_ROOT')
        exit(1)

    repository_suburi = 'var/spack/repos/builtin/packages/'
    repository_full_path = os.path.join(os.getenv("SPACK_ROOT"), repository_suburi)

    if not os.path.exists(repository_suburi):
        print('Spack repository does not exists')
        exit(1)
    return repository_full_path


def create_directory(package_name):
    """Create a package directory for the provided package name"""
    if not package_name.startswith('py-'):
        package_name = 'py-' + package_name
    target_path = os.path.join(get_spack_repository(),
                               package_name)
    if os.path.exists(target_path):
        return False
    try:
        os.makedirs(target_path)
    except FileExistsError:
        pass
    finally:
        return os.path.exists(target_path)


def create_package(name, raw):
    target_path = os.path.join(get_spack_repository(),
                               name)
    with open(os.path.join(target_path, 'package.j2'), 'w') as f:
        f.write(raw)


def prepare_template(name) -> str:
    package_template = '''\
    # Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
    # Spack Project Developers. See the top-level COPYRIGHT file for details.
    #
    # SPDX-License-Identifier: (Apache-2.0 OR MIT)
    # ----------------------------------------------------------------------------
    # If you submit this package back to Spack as a pull request,
    # please first remove this boilerplate and all FIXME comments.
    #
    # This is a template package file for Spack.  We've put "FIXME"
    # next to all the things you'll want to change. Once you've handled
    # them, you can save this file and test your package like this:
    #
    #     spack install {name}
    #
    # You can edit this file again by typing:
    #
    #     spack edit {name}
    #
    # See the Spack documentation for more information on packaging.
    # ----------------------------------------------------------------------------
    from spack import *
    class {class_name}({base_class_name}):
        """FIXME: Put a proper description of your package here."""
        # FIXME: Add a proper url for your package's homepage here.
        homepage = "{homepage}"
        url      = "{url}"
    '''

    version = "version('{version_number}', sha256='{sha256}'"

    dependencies = """"\
    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    # depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))"""

    body_def = """\
    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args"""


class SpackPackage(object):
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

        print(self.url)
        self._versions_formatter()
        print(self.version_builder())

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
        print(self.versions)

    def version_builder(self) -> str:
        raw_versions: str = ''
        for v in self.versions:
            raw_versions += f'version("{str(v[0])}", sha256="{str(v[1])}")\n'
        return raw_versions

    def package_name_builder(self) -> str:
        name = self.content['info']['name']
        if name[0].islower():
            name = name[0].upper() + name[1:]

        l_name = list(name)
        for i in [index for index, element in enumerate(l_name) if element == '-']:
            try:
                if l_name[i+1].islower():
                    l_name[i+1] = l_name[i+1].upper()
            except:
                pass
            finally:
                name = ''.join(l_name).replace('-', '')

        if not name.startswith("Py"):
            name = "Py" + name
        return name

    def summary_builder(self):
        self.summary = self.content['summary']


if __name__ == "__main__":
    main()
    from jinja2 import Environment, PackageLoader, select_autoescape

    env = Environment(loader=PackageLoader('src', 'templates'),
                      autoescape=select_autoescape(['j2']))
    template = env.get_template('package.j2')
    print(template.render(description="sdfsdf"))
