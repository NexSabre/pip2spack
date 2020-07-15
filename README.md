# pip2Spack

Automatically create a spack package base on the pypi.org information

## Installation (not available yet)
Later, the package will be added into pypi repository.
```
pip install pip2spack
```

# Build
To build a .whl package

```
pip install setuptools wheel twine
python setup.py sdist bdist_wheel
```

Than go to `dist` directory and type

```
pip install pip2spack-0.1-py3-none-any.whl
```

## Run
Before you run the script download a spack and export `SPACK_ROOT`. 

To run a script, provide a package names:
```
pip2spack {package_names_for_convert}
```

Example:
```
pip2spack jsl 
```

