
SHELL = /bin/bash
SCRIPTS="./scripts"

.PHONY: help start kill status monitor errors

help:
	@ echo ""
	@ echo "Usage:"
	@ echo "  setup: Setup Project and install requirements"
	@ echo "  check_code_style: Run Code Style Checks"
	@ echo "  check_static_types: Run Static Types Checks"
	@ echo ""

setup:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/setup

check_code_style:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/check_code_style

check_static_types:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/check_static_types
