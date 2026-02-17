
SHELL = /bin/bash
SCRIPTS="./scripts"

.PHONY: help setup test test_ci check_code_style check_static_types

help:
	@ echo ""
	@ echo "Usage:"
	@ echo "  setup: Setup Project and install requirements"
	@ echo "  test: Run project tests"
	@ echo "  test_ci: Run project tests for CI execution"
	@ echo "  check_code_style: Run Code Style Checks"
	@ echo "  check_static_types: Run Static Types Checks"
	@ echo "  install: Install local package in edit mode"
	@ echo "  publish: Publish the library to pypi"
	@ echo ""

check_code_style:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/check_code_style

check_static_types:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/check_static_types

install:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/install

publish:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/publish

setup:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/setup

test:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/run_tests

test_ci:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/run_tests --ci
