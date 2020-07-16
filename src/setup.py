import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

with open("../VERSION", "r") as vr:
    version_number = vr.read()

with open("../requirements.txt", "r") as req:
    requirements = []
    for l in req.readlines():
        requirements.append(l.rstrip())

setuptools.setup(
    name="pip2spack",
    version=version_number,
    author="Nex Sabre",
    author_email="nexsabre@protonmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NexSabre/pip2spack",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pip2spack = pip2spack.main:main'
        ],
    },
)
