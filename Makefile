all: clean build publish

clean:
	@echo "Cleaning..."
	rm -rf src/build src/dist pip2spack.egg-info
	@echo "Cleaning... Done"

build:
	@echo "Building..."
	cd src; python setup.py sdist bdist_wheel
	@echo "Building... Done"

publish:
	twine upload src/dist/*