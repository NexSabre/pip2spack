import argparse
import json
import os

import requests

from pip2spack.spack_package import SpackPackage
from pip2spack.spack import Spack, Package


def main():
    parser = argparse.ArgumentParser(description='Create a spack package base on:')
    parser.add_argument('-u', '--update', action='store_true')
    parser.add_argument('name', type=str, nargs='+', help='Package name on the pypi.org')

    args = parser.parse_args()

    ready_packages = validate_pip_package_exists(args.name)
    show_packages_for_process(ready_packages, args.name)

    if not args.update:
        generate_packages(ready_packages)
    else:
        update_packages(ready_packages)


def update_packages(ready_packages):
    for p in ready_packages:
        package = Package(package_name=p)
        package.replace_structure_with_marker()
        package.generate_modded_package()


def generate_packages(ready_packages):
    for key, value in ready_packages.items():
        print(f"INFO:: Generating package for the {key}")
        s_package = SpackPackage(value)
        generated_file = s_package.generate_file()

        create_directory(key)
        created_package_uri = create_package(key, generated_file)
        print(f"_OK_:: Package for {key} was generated\n\t"
              f":: If \'spack install py-{key}\' return any problems, try to uncomment:\n\t"
              f":: \tdepends_on('py-setuptools', type='build')\n\t"
              f":: at {created_package_uri}")


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
    if not packages_not_found:
        print()
        return

    print("\nPackages not found:")
    for p in packages_not_found:
        print(f'\t{p}')
    else:
        print()


def get_spack_repository() -> str:
    """Return a absolute path about spack repository"""
    if not os.getenv("SPACK_ROOT", False):
        print('Please provide a information about SPACK_ROOT')
        exit(1)

    repository_suburi = os.path.relpath('var/spack/repos/builtin/packages/')
    repository_full_path = os.path.join(os.getenv("SPACK_ROOT"), repository_suburi)

    if not os.path.exists(repository_full_path):
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


def create_package(name, raw) -> str:
    if not name.startswith('py-'):
        name = 'py-' + name
    target_path = os.path.join(get_spack_repository(),
                               name)
    with open(os.path.join(target_path, 'package.py'), 'w') as f:
        f.write(raw)

    return os.path.join(target_path, 'package.py')


if __name__ == "__main__":
    main()
