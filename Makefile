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

.PHONY: dbuild
dbuild:
	docker build -t pip2spack .

.PHONY: drun
drun:
	docker run -it pip2spack
