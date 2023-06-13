.PHONY: help build test notebook exec dashboard
.DEFAULT_GOAL := help

# Docker image build info
PROJECT:=tch-test-tandoor-ds-app
USERNAME:=$(shell git config user.name | sed 's/ /-/g')
RELEASE:=0.0.0
BUILD_TAG?=latest

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@echo "python starter project tch-test-tandoor-ds-app"
	@echo "====================="
	@echo
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

########################################################
## Local development
########################################################

build: ## Build the latest image
	docker build --target main --progress=plain -t $(PROJECT):${BUILD_TAG} .

test: ## Run tests
	docker build --target test --progress=plain -t $(PROJECT):test .

notebook: DARGS?=-v "${CURDIR}":/opt/app -p 8888:8888
notebook: ## Run jupyterlab notebook
	docker run -it --rm $(DARGS) $(PROJECT):${BUILD_TAG} jupyter lab \
		--ip=0.0.0.0 \
		--allow-root \
		--NotebookApp.token="" \
		--NotebookApp.password=""

exec: ARGS?=/bin/bash
exec: DARGS?=-v "${CURDIR}":/opt/app
exec: ## Exec into the container
	docker run -it --rm $(DARGS) $(PROJECT) $(ARGS)

dashboard: DARGS?=-v "${CURDIR}"/src:/opt/app/src -v "${CURDIR}"/data:/opt/app/data -p 8050:8050
dashboard: ## Run dash server
	docker run -it --rm $(DARGS) $(PROJECT):${BUILD_TAG}

precommit: ARGS?=black .
precommit: DARGS?=-v ${CURDIR}:/opt/app
precommit: # run all precommit hooks
	docker run --rm $(DARGS) $(PROJECT) $(ARGS)

doc-update: ARGS?=sphinx-apidoc --full -A $(USERNAME) -H $(PROJECT) -R $(RELEASE) -a ./src/ -o docs/
doc-update: DARGS?=-v "${CURDIR}":/opt/app
doc-update:
	docker run --rm $(DARGS) $(PROJECT) $(ARGS)

doc-publish: ARGS?=make html
doc-publish: DARGS?=-v "${CURDIR}":/opt/app -w /opt/app/docs
doc-publish:
	docker run --rm $(DARGS) $(PROJECT) $(ARGS)

doc-clean:
	rm -rf docs/
