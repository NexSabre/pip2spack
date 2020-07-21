BUILTIN_REPOSITORY_REL_PATH = "var/spack/repos/builtin/packages"

MARKER_VERSION = "{% pip2spack_version_marker %}"
MARKER_VERSION_TEMPLATE = """{% for v in versions|reverse %}
version('{{ v[0] }}', sha256='{{ v[1] }}'){% endfor %}"""


def marker_version_template(space: int = 0):
    spaces = ' ' * space
    return "{% for v in versions|reverse %}\n" + spaces + "version('{{ v[0] }}', sha256='{{ v[1] }}'){% endfor %}"
