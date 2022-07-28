import os


def get_spack_repository() -> str:
    """Return an absolute path about spack repository"""
    spack_root = os.getenv("SPACK_ROOT", "")
    if not spack_root:
        print("Please provide a information about SPACK_ROOT")
        exit(1)

    repository_suburi = os.path.relpath("var/spack/repos/builtin/packages/")
    repository_full_path = os.path.join(spack_root, repository_suburi)

    if not os.path.exists(repository_full_path):
        print("Spack repository does not exists")
        exit(1)
    return repository_full_path


def create_directory(package_name):
    """Create a package directory for the provided package name"""
    if not package_name.startswith("py-"):
        package_name = "py-" + package_name
    target_path = os.path.join(get_spack_repository(), package_name)
    if os.path.exists(target_path):
        return False
    try:
        os.makedirs(target_path)
    except FileExistsError:
        pass
    finally:
        return os.path.exists(target_path)


def create_package(name, raw) -> str:
    if not name.startswith("py-"):
        name = "py-" + name
    target_path = os.path.join(get_spack_repository(), name)
    with open(os.path.join(target_path, "package.py"), "w") as f:
        f.write(raw)

    return os.path.join(target_path, "package.py")
