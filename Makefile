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

.PHONY: lint
lint:
	flake8 pip2spack/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics --exclude .git,__pycache__,build,dist,pip2spack/templates
	flake8 pip2spack/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=120 --statistics --exclude .git,__pycache__,build,dist,pip2spack/templates,tests/pip2spack/core/mocks.py

.PHONY: mypy
mypy:
	python -m mypy pip2spack/ tests/

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