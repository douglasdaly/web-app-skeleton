#!/usr/bin/env make -f
#
#	Setup
#

# - Ensure the .env file is copied over first
.env:
	@cp sample.env .env

# - Include .env variables & set defaults (if needed)
-include .env

PYTHON ?= python
PKG_MGR ?= pipenv
PYTEST_CORES ?= auto

# - Directories
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SUBDIR_ROOTS := alembic app scripts tests
DIRS := . $(shell find $(SUBDIR_ROOTS) -type d)
GARBAGE_PATTERNS := *.pyc *~ *-checkpoint.ipynb *.egg-info __pycache__/
GARBAGE := $(foreach DIR,$(DIRS),$(addprefix $(DIR)/,$(GARBAGE_PATTERNS)))

# - Backend tools
REQS_SEPARATE = 0
ifeq ($(PKG_MGR), pipenv)
	RUN_PRE = pipenv run
	VENV_ACTIVATE = . $(shell pipenv --venv)/bin/activate

	ifneq (,$(wildcard ./Pipfile.lock))
		VENV_CREATE = pipenv sync --dev
	else
		VENV_CREATE = pipenv install --dev
	endif

	VENV_REMOVE = pipenv --rm
else
	REQUIREMENTS_SEPARATE = 1

	RUN_PRE =
	VENV_ACTIVATE = source venv/bin/activate
	VENV_CREATE = virtualenv venv
	VENV_REQUIREMENTS = pip install -r requirements.txt
	VENV_REMOVE = rm -rf venv
endif

VENV_DEACTIVATE = deactivate

RUN_ALEMBIC = $(RUN_PRE) alembic
RUN_FLAKE8 = $(RUN_PRE) flake8
RUN_MYPY = $(RUN_PRE) mypy
RUN_PYTEST = $(RUN_PRE) pytest
RUN_PYTHON = $(RUN_PRE) $(PYTHON)
RUN_UVICORN = $(RUN_PRE) uvicorn


#
#	Recipes
#
.DEFAULT-GOAL := help-short

# Help
.PHONY: help-short
help-short:
	@printf 'Usage: make \033[36m[target]\033[0m\n'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*? ## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*? ## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ''

.PHONY: help
help:  ## Shows the help menu for all targets.
	@printf 'Usage: make \033[36m[target]\033[0m\n'
	@echo ''
	@echo 'Main targets:'
	@grep -E '^[a-zA-Z_-]+:.*? ## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*? ## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ''
	@echo 'Specific sub-targets:'
	@grep -E '^[a-zA-Z_-]+:.*? ### .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*? ### "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ''

# Environment
# - Setup
.PHONY: setup
setup: .env setup-venv  ## Sets up the development environment.

.PHONY: setup-venv
setup-venv:  ### Sets up Python virtual environment.
	@printf '\033[36m%s\033[0m\n' 'CREATING PYTHON ENVIRONMENT'
	$(VENV_CREATE)
ifeq ($(SEPARATE_REQS), 1)
	@printf '\033[36m%s\033[0m\n' 'INSTALLING PYTHON REQUIREMENTS'
	$(VENV_ACTIVATE) && $(VENV_REQUIREMENTS) && $(VENV_DEACTIVATE)
endif

# - Teardown
.PHONY: teardown
teardown: teardown-venv  ## Tears down the development environment.

.PHONY: teardown-venv
teardown-venv:  ### Removes the Python virtual environment.
	@printf '\033[36m%s\033[0m\n' 'REMOVING PYTHON ENVIRONMENT'
	$(VENV_REMOVE)

# - Cleaning
.PHONY: clean
clean: clean  ## Cleans up unnecessary Python files.
	rm -rf $(GARBAGE)

# Unit testing
.PHONY: test
test:  ## Runs the Python unit tests.
	$(RUN_PYTEST) -n $(PYTEST_CORES)

# Coverage
.PHONY: coverage
coverage:  ## Runs code coverage checks.
	$(RUN_PYTEST) --cov=src/ -n $(PYTEST_CORES)

# Linting
.PHONY: lint
lint:  ## Runs code linting.
	$(RUN_FLAKE8)

# MyPy
.PHONY: mypy
mypy:  ## Runs MyPy type checking.
	$(RUN_MYPY) ./app

# Debugging
.PHONY: debug
debug:  ## Runs the application for debugging.
	@printf '\033[36m%s\033[0m\n' 'STARTING BACKEND FOR DEBUGGING'
	$(RUN_UVICORN) app.main:app --debug --reload --port=$(SERVER_PORT)

# Storage
# - Alembic
.PHONY: alembic-upgrade
alembic-upgrade:
	$(RUN_ALEMBIC) upgrade head

.PHONY: alembic-revise
alembic-revise:
	$(RUN_ALEMBIC) revision

# Misc.
.PHONY: cloc
cloc:  ## Count lines of code
	cloc $(SUBDIR_ROOTS) --exclude-dir=__pycache__,dist
