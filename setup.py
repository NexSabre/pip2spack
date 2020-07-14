import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as vr:
    version_number = vr.read()

setuptools.setup(
    name="md",
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
    entry_points={
        'console_scripts': [
            'pip2spack = src.main:main'
        ],
    },
)