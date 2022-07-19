.PHONY: clean
clean:
	@echo "Cleaning..."
	rm -rf src/build src/dist src/pip2spack.egg-info
	@echo "Cleaning... Done"

.PHONY: format
format:
	@echo "Formatting..."
	python -m black -t py36 .
	python -m isort src/ tests/ --profile black
	@echo "Formatting... Done"

.PHONY: check
check:
	python -m black --check -t py36 src/ tests/

.PHONY: build
build:
	@echo "Building..."
	cd src; python setup.py sdist bdist_wheel --universal
	@echo "Building... Done"

.PHONY: publish
publish: clean format build
	twine upload dist/*