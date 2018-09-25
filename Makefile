#!make
# Default values, can be overridden either on the command line of make
# or in .env

.PHONY: init vars test coverage \
	version vars ps \
	build pull changelog \
	release push-qa push-prod

VERSION:=$(shell \
	docker run --rm -it \
		-v $(PWD)/bin/update_release.py:/usr/src/app/update_release.py \
		-v $(PWD)/versions.py:/usr/src/app/versions.py \
		python-requests update_release.py -v)


init:
ifeq ($(wildcard .env),)
	cp .env.sample .env
	echo PYTHONPATH=`pwd`/src >> .env
endif
	pipenv install --dev --three 

test: check-env
	flake8 src --max-line-length=120
	pytest --cov=src test

coverage: test
	coverage html
	open htmlcov/index.html

version:
	@echo CHANGELOG GENERATOR:
	@docker run -it --rm \
		-v "$(pwd)":/usr/local/src/your-app \
		ferrarimarco/github-changelog-generator:1.14.3 \
		--version
	@echo ''
	@echo APPLICATION: 
	@echo Version: $(VERSION)
	@echo ''
	@echo Updating release numbers...
	@docker run --rm -it \
		-v $(PWD)/.git:/usr/src/app/.git \
		-v $(PWD)/versions.py:/usr/src/app/versions.py \
		-v $(PWD)/bin/update_release.py:/usr/src/app/update_release.py \
		python-requests update_release.py

vars: check-env
	@echo '  Version: $(VERSION)'
	@echo '  PYTHONPATH: $(PYTHONPATH)'
	@echo ''
	@echo '  GITHUB_OWNER=${GITHUB_OWNER}'
	@echo '  GITHUB_REPO=${GITHUB_REPO}'
	@echo '  GITHUB_USER=${GITHUB_USER}'
	@echo '  GITHUB_KEY=${GITHUB_KEY}'
	@echo '  CHANGELOG_GITHUB_TOKEN=${CHANGELOG_GITHUB_TOKEN}'

check-env:
ifeq ($(wildcard .env),)
	@echo ".env file is missing. Create it from .env.sample"
	@exit 1
else
include .env
export
endif

login:
	docker login

build:
	cd bin && docker build -t python-requests .

pull: build
	docker pull ferrarimarco/github-changelog-generator:1.14.3

ps:
	# A lightly formatted version of docker ps
	docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}} ago'

changelog: check-env
	@echo updating CHANGELOG...
	@docker run -it --rm \
		-v $(PWD):/usr/local/src/your-app \
		ferrarimarco/github-changelog-generator:1.14.3 \
		-u ${GITHUB_OWNER} -p ${GITHUB_REPO} -t ${CHANGELOG_GITHUB_TOKEN}

	# update versions
	@docker run --rm -it \
		-v $(PWD)/.git:/usr/src/app/.git \
		-v $(PWD)/versions.py:/usr/src/app/versions.py \
		-v $(PWD)/bin/update_release.py:/usr/src/app/update_release.py \
		python-requests update_release.py

	# commit master
	git add CHANGELOG.md
	git add versions.py
	git commit -m "updated CHANGELOG (and version numbers)"
	git push

check-release: check-env
	# make sure we are in master
	@docker run --rm -it \
		-v $(PWD)/.git:/usr/src/app/.git \
		-v $(PWD)/versions.py:/usr/src/app/versions.py \
		-v $(PWD)/bin/update_release.py:/usr/src/app/update_release.py \
		python-requests update_release.py check --branch=master

	# update versions and ask for confirmation
	@docker run --rm -it \
		-v $(PWD)/.git:/usr/src/app/.git \
		-v $(PWD)/versions.py:/usr/src/app/versions.py \
		-v $(PWD)/bin/update_release.py:/usr/src/app/update_release.py \
		python-requests update_release.py

	VERSION=$(shell \
	docker run --rm -it \
		-v $(PWD)/bin/update_release.py:/usr/src/app/update_release.py \
		-v $(PWD)/versions.py:/usr/src/app/versions.py \
		python-requests update_release.py -v)

	@echo Version used will be $(VERSION)

	@docker run --rm -it \
		-v $(PWD)/.git:/usr/src/app/.git \
		-v $(PWD)/versions.py:/usr/src/app/versions.py \
		-v $(PWD)/bin/update_release.py:/usr/src/app/update_release.py \
		python-requests update_release.py confirm

release: check-release
	# create branch and tag
	git checkout -b release-$(VERSION)
	git add .
	git commit -m "Prepared release $(VERSION)"
	git push --set-upstream origin release-$(VERSION)

	git tag $(VERSION)
	git tag -f qa-release
	git push --tags --force

	# updating CHANGELOG
	make changelog

	# create github release
	@docker run --rm -it \
		-v $(PWD)/.git:/usr/src/app/.git \
		-v $(PWD)/versions.py:/usr/src/app/versions.py \
		-v $(PWD)/bin/update_release.py:/usr/src/app/update_release.py \
		-e GITHUB_USER=${GITHUB_USER} \
		-e GITHUB_OWNER=${GITHUB_OWNER} \
		-e GITHUB_REPO=${GITHUB_REPO} \
		-e GITHUB_KEY=${GITHUB_KEY} \
		python-requests update_release.py publish

	# git merge master
	git checkout master
	git merge release-$(VERSION)
	git push

push-qa:
	# update tags
	git tag -f qa-release
	git push --tags --force

	# updating CHANGELOG
	make changelog

push-prod:
	@# confirm push to production
	@docker run --rm -it \
		-v $(PWD)/.git:/usr/src/app/.git \
		-v $(PWD)/versions.py:/usr/src/app/versions.py \
		-v $(PWD)/bin/update_release.py:/usr/src/app/update_release.py \
		python-requests update_release.py confirm --prod

	# update tags
	git tag -f prod-release
	git push --tags --force

	# updating CHANGELOG
	make changelog
