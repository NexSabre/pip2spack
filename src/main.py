import argparse
import json
import os

import requests

from spack_package import SpackPackage


def main():
    parser = argparse.ArgumentParser(description='Create a spack package base on:')
    parser.add_argument('name', type=str, nargs='+', help='Package name on the pypi.org')

    args = parser.parse_args()
    ready_packages = validate_pip_package_exists(args.name)
    show_packages_for_process(ready_packages, args.name)

    s_package = SpackPackage(ready_packages["jsl"])
    generated_file = s_package.generate_file()

    create_directory("jsl")
    create_package("jsl", generated_file)


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


def create_package(name, raw):
    if not name.startswith('py-'):
        name = 'py-' + name
    target_path = os.path.join(get_spack_repository(),
                               name)
    with open(os.path.join(target_path, 'package.py'), 'w') as f:
        f.write(raw)


if __name__ == "__main__":
    main()
