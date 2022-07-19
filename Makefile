.PHONY: clean
clean:
	@echo "Cleaning..."
	rm -rf build dist pip2spack.egg-info
	@echo "Cleaning... Done"

.PHONY: format
format:
	@echo "Formatting..."
	python -m black -t py36 .
	python -m isort pip2spack/ tests/ --profile black
	@echo "Formatting... Done"

.PHONY: check
check:
	python -m black --check -t py36 pip2spack/ tests/

.PHONY: test
test:
	pytest tests/

.PHONY: build
build:
	@echo "Building..."
	python setup.py sdist bdist_wheel --universal
	@echo "Building... Done"

.PHONY: publish
publish: clean format build
	twine upload dist/*