# pip2Spack
![Test](https://github.com/NexSabre/pip2spack/workflows/Test/badge.svg?branch=master)
[![PyPI version](https://badge.fury.io/py/pip2spack.svg)](https://badge.fury.io/py/pip2spack)

Automatically create and update a spack package base on the pypi.org information.

__Cons__:
 - Faster package creation than using the default option `spack create`
 - Automatic updating of existing packages with information contained on pypi.org
 
 
## TL;DR
```
// install 
pip install pip2spack 

// create new one
pip2spack create jsl

// update a internal (bultin) package
pip2spack update codecov 

// download latest package locally 
pip2spack download jsl codecov
```


## Installation
Later, the package will be added into pypi repository.
```
pip install pip2spack
```

## Build
To build a .whl package

```
pip install setuptools wheel twine
python setup.py sdist bdist_wheel
```

Than go to `dist` directory and type

```
pip install pip2spack-1.0-py3-none-any.whl
```

## Run
Before you run the script download a spack and export `SPACK_ROOT`. 
### Create a new package
To run a script, provide a package names:
```
pip2spack create {package_names_for_convert}
```

Example for creation one new package:
```
pip2spack create jsl 
```

you can also create more than one in single run:
```
pip2spack create jsl codecov
```

### Updating existing packages (builtin)
Since v0.2, pip2spack is able to update builtin packages to newest version base on the pypi.org information.

__No more adding a new version thru Spack's Pull Requests!__ 

Example:
```
pip2spack update codecov
```

__Notice:__ You can not to create and update packages at once. These operations are separated (in actual version)


### Downloading a newest packages locally
Since v1.1, pip2spack is able to download latest `.tar.gz`/`.whl` package locally, using `download` command

Example:
```
pip2spack download jsl codecov
```

Packages will be stored at the `temp` directory (depends on the OS), proper information wit storage place will be displayed.
