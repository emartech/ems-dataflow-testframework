SHELL=/bin/bash
.PHONY: test check

test: ## Run all unit tests
	py.test -o python_files="test_*.py"

check: ## Check codestyle
	pylint --rcfile=.pylintrc --output-format=colorized setup.py
