SHELL=/bin/bash
.PHONY: test publish build check
.DEFAULT_GOAL := build

build: check test it-test ## Build package

dist-build:
	python setup.py sdist

publish: dist-build ## Publish package to PyPi
	twine upload dist/*

test: ## Run all tests
	py.test -o python_files="test_*.py"

check:
	pylint --rcfile=.pylintrc --output-format=colorized \
		setup.py \
#		testframework \
#		tests \
