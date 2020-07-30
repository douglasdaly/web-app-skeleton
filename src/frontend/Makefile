#!/usr/bin/env make -f
#
#	Setup
#

# - Ensure the .env file is copied over first
.env:
	@cp sample.env .env

# - Include .env variables & set defaults (if needed)
-include: .env

PKG_MGR ?= yarn

ifeq ($(PKG_MGR), yarn)
	RUN_PRE = yarn
	VENV_CREATE = yarn install
else
	RUN_PRE = npm run
	VENV_CREATE = npm install
endif


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
setup-venv:  ### Sets up Node virtual environment.
	@printf '\033[36m%s\033[0m\n' 'CREATING NODE ENVIRONMENT'
	$(VENV_CREATE)

# Unit testing
.PHONY: test
test:  ## Run the Jest unit tests.
	$(RUN_PRE) test:unit

# Linting
.PHONY: lint
lint:  ## Runs ESLint for code linting.
	$(RUN_PRE) lint

# Debugging
.PHONY: debug
debug:  ## Runs the frontend in debug mode.
	FRONTEND_APP_ENV=debug $(RUN_PRE) serve

# Build
.PHONY: build
build:  ## Builds the frontend application.
	$(RUN_PRE) build
