#########################################
# Python-opinionated makefile
#########################################

define default-help
# Invoke: 'make help'
endef
.PHONY: default
default: help


{% if project_type == 'app_src' or project_type == 'app_flat' or project_type == 'lib_src' or project_type == 'lib_flat' %}
define build-help
# Build {{project_slug}} python packages from project
endef
.PHONY: build
build:
	@echo " ## make build [BEGIN]"
	poetry build
	@echo " ## make build [DONE]"



{% endif %}
define build-docker-help
# Build docker image from Dockerfile
endef
.PHONY: build-docker
build-docker:
	@echo " ## make build-docker [BEGIN]"
	docker build -t {{project_slug}}-dev --target {{project_slug}}-dev  .
	docker build -t {{project_slug}}-ci --target {{project_slug}}-ci  .
	docker build -t {{project_slug}}-deploy --target {{project_slug}}-deploy  .
	@echo " ## make build-docker [DONE]"


define clean-help
# Remove virtual python environment & build artifacts if applicable
endef
.PHONY: clean
clean:
	@echo " ## make clean [BEGIN]"
	rm -fr $(VIRTUAL_ENV) || true
	rm -fr .dist || true
	@echo " ## make clean [DONE]"

define check-help
# Check depedency integrity with poetry check
endef
.PHONY: check
check:
	@echo " ## make check [BEGIN]"
	poetry check
	@echo " ## make check [DONE]"


define docs-help
# Build docs with makefile
endef
.PHONY: docs
docs:
	@echo " ## make docs [BEGIN]"
	$(MAKE) -C ./docs dirhtml
	@echo " ## make docs [DONE]"


define install-help
# Run poetry to install all none-dev packages.
# defined in pyproject.toml
endef
.PHONY: install
install:
	@echo " ## make install [BEGIN]"
	poetry install --without=dev --no-interaction --sync
	@echo " ## make install [DONE]"


define install-all-help
# Run poetry to install all packages including dev packages
# defined in pyproject.toml.
endef
.PHONY: install-all
install-all:
	@echo " ## make install [BEGIN]"
	poetry install --no-interaction --sync
	@echo " ## make install [DONE]"


define freeze-help
# Run poetry to install all packages including dev packages
# defined in pyproject.toml.
endef
.PHONY: freeze
freeze:
	@echo " ## make freeze [BEGIN]"
	poetry export --without=dev --without-hashes --format=requirements.txt > requirements.txt
	poetry export --with=dev --without-hashes --format=requirements.txt > requirements-dev.txt
	@echo " ## make freeze [DONE]"


define format-help
# Run linters and auto formatters.
# This uses black and isort
endef
.PHONY: format
format:
	@echo " ## make format [BEGIN]"
	flake8
	isort .
	black .
	@echo " ## make format [DONE]"


define verify-help
# Run linters and verify project integrity.
# This includes flake8, isort, black and mypy.
endef
.PHONY: verify
verify:
	@echo " ## make verify [BEGIN]"
	flake8
	isort --check .
	black --check .
	mypy .
	@echo " ## make verify [DONE]"



{% if project_type == 'app_src' %}

define run-help
# Run application, postfix with ARGS="..." for cli arguments.
# Such that ARGS="<--flags> <input_data>" for flags and input data.
# As an example: `make run ARGS="--help"`
endef
.PHONY: run
run:
	@echo " ## make run [BEGIN]"
	python src/{{project_slug}}/main.py ${ARGS}
	@echo " ## make run [DONE]"

{% elif project_type == 'app_flat' %}
define run-help
# Run application, postfix with INPUT="..." for cli arguments.
# Such that ARGS="<--flags> <input_data>" for flags and input data.
# As an example: `make run ARGS="--help"`
endef
.PHONY: run
run:
	@echo " ## make run [BEGIN]"
	python {{project_slug}}/main.py ${ARGS}
	@echo " ## make run [DONE]"

{% endif %}
{%if project_type == "django"%}
define migrate-help
# Run database migration through django manage.py
endef
.PHONY: migrate
migrate:
	@echo " ## make migrate [BEGIN]"
	./manage.py migrate
	@echo " ## make migrate [DONE]"

define collectstatic-help
# Run database migration through django manage.py
endef
.PHONY: collectstatic
collectstatic:
	@echo " ## make run [BEGIN]"
	./manage.py collectstatic --no-input
	@echo " ## make run [DONE]"

{% endif %}
define tests-help
# Run tests via pytest
endef
.PHONY: tests
tests:
	@echo " ## make test [BEGIN]"
	pytest --cov --cov-report term --cov-report xml:coverage.xml --junitxml report.xml .
	@echo " ## make test [DONE]"


define deploy-help
# Deploy project with helm
endef
.PHONY: deploy
deploy:
	@echo " ## make deploy [BEGIN]"
	
	@echo " ## make deploy [DONE]"


define release-help
# Release python packages defined in pyproject.toml to package repository
# This command uses twine and will need to be authenticated with repository
endef
.PHONY: release
release:
	@echo " ## make release [BEGIN]"
	twine upload dist/*
	@echo " ## make release [DONE]"


define help-help
# Print the description of every target
endef
.PHONY: help
help:
	@./.print_help.py

define help-verbose-help
# Print the verbose description of every target
endef
.PHONY: help-verbose
help-verbose:
	@./.print_help.py --verbose