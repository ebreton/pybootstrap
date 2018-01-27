.PHONY:test dev

export .env

venv:
	pipenv --update 
	pipenv update --dev --python 3

test:
	flake8 src --max-line-length=120
	pytest --cov=. test
	coverage html
	open htmlcov/index.html

dev:
	flake8 src --max-line-length=120
	pytest --cov=. -x test
