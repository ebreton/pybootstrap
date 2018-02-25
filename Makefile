#!make
# Default values, can be overridden either on the command line of make
# or in .env

.PHONY: init vars test coverage

vars:
	@echo 'Environment-related vars:'
	@echo '  PYTHONPATH=${PYTHONPATH}'

init:
ifeq ($(wildcard .env),)
	cp .env.sample .env
	echo PYTHONPATH=`pwd`/src >> .env
endif
	pipenv --update 
	pipenv install --dev --python 3

test: check-env
	flake8 src --max-line-length=120
	pytest --cov=src test

coverage: test
	coverage html
	open htmlcov/index.html

check-env:
ifeq ($(wildcard .env),)
	@echo "Please create your .env file first, from .env.sample or by running make venv"
	@exit 1
else
include .env
export
endif
