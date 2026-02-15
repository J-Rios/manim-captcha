
SHELL = /bin/bash
SCRIPTS="./scripts"

.PHONY: help start kill status monitor errors

help:
	@ echo ""
	@ echo "Usage:"
	@ echo "  setup: Setup Project and install requirements"
	@ echo "  test: Run project tests"
	@ echo "  test-ci: Run project tests for CI execution"
	@ echo "  check_code_style: Run Code Style Checks"
	@ echo "  check_static_types: Run Static Types Checks"
	@ echo ""

setup:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/setup

test:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/run_tests

test-ci:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/run_tests --ci

check_code_style:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/check_code_style

check_static_types:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/check_static_types
