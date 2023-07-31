import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pip2spack",
    version="2.0.0a",
    author="Nex Sabre",
    author_email="nexsabre@protonmail.com",
    description="Automatically create and update a spack package base on the pypi.org information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NexSabre/pip2spack",
    packages=setuptools.find_packages(),
    package_data={"pip2spack": ["templates/*.j2"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests==2.22.0",
        "jinja2==2.11.3",
        "dataclasses==0.6",
        "markupsafe==2.0.1",
        "typer==0.9.0",
    ],
    entry_points={
        "console_scripts": ["pip2spack = pip2spack.__main__:app"],
    },
)
