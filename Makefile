#!/usr/bin/env make -f
#
#	Configuration
#
BACKEND_DIR = ./src/backend
FRONTEND_DIR = ./src/frontend

#
#	Setup
#

# - Ensure the .env file is copied over first
.env:
	@cp sample.env .env

# - Include .env variables & set defaults (if needed)
-include .env

# - Directories
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SUBDIR_ROOTS := docs
DIRS := . $(shell find $(SUBDIR_ROOTS) -type d)
GARBAGE_PATTERNS := *.pyc *~ *-checkpoint.ipynb *.egg-info __pycache__/
GARBAGE := $(foreach DIR,$(DIRS),$(addprefix $(DIR)/,$(GARBAGE_PATTERNS)))

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
.PHONY: setup
setup: setup-backend setup-frontend  ## Sets up the development environment.

.PHONY: setup-backend
setup-backend:  ### Sets up the backend's development environment.
	$(MAKE) -C $(BACKEND_DIR) setup

.PHONY: setup-frontend
setup-frontend:  ### Sets up the frontend's development environment.
	$(MAKE) -C $(FRONTEND_DIR) setup

.PHONY: teardown
teardown:  ## Tears down the development environment.
	$(MAKE) -C $(BACKEND_DIR) teardown

.PHONY: clean
clean:  ## Cleans up unnecessary project files.
	rm -rf $(GARBAGE)
	$(MAKE) -C $(BACKEND_DIR) clean

# Unit testing
.PHONY: test
test: test-backend  ## Runs the project's unit tests.

.PHONY: test-backend
test-backend:  ## Runs the backend's unit tests.
	$(MAKE) -C $(BACKEND_DIR) test

# Coverage
.PHONY: coverage
coverage: coverage-backend  ## Runs code coverage checks.

.PHONY: coverage-backend
coverage-backend:  ### Runs code coverage checks on the backend.
	$(MAKE) -C $(BACKEND_DIR) coverage

# Linting
.PHONY: lint
lint: lint-backend  ## Runs all code linting.

.PHONY: lint-backend
lint-backend:  ### Runs code linting on the backend.
	$(MAKE) -C $(BACKEND_DIR) lint

# Debugging
.PHONY: debug
debug: debug-backend  ## Debugs the application on the local machine.

.PHONY: debug-backend
debug-backend:  ### Runs the backend application for debugging.
	$(MAKE) -C $(BACKEND_DIR) debug

.PHONY: debug-frontend
debug-frontend:  ### Runs the frontend application for debugging.
	$(MAKE) -C $(FRONTEND_DIR) debug

# Misc.
.PHONY: cloc
cloc:  ## Count lines of code
	cloc ./scripts ./src --exclude-dir=__pycache__,.nuxt,dist,node_modules
