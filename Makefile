.PHONY:test dev

export .env

dev:
	flake8 src --max-line-length=120
	pytest --cov=. -x test

test:
	flake8 src --max-line-length=120
	pytest --cov=. test
	coverage html
	open htmlcov/index.html

venv:
	echo PYTHONPATH=`pwd`/src > .env
	pipenv --update 
	pipenv update --dev --python 3
