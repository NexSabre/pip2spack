# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Package automatically generated using 'pip2spack' converter

from spack import *


class {{ package_name }}(PythonPackage):
    """
    {{ summary }}
    """

    homepage = "{{ homepage }}"
    url      = "{{ url }}"

    {% for v in versions %}
    version('{{ v[0] }}', sha256='{{ v[1] }}'){% endfor %}

    # depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    {% if depends_on_setuptools %}
    depends_on('py-setuptools', type='build')
    {% else %}
    # depends_on('py-setuptools', type='build')
    {% endif %}

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
