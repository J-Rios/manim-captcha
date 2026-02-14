
SHELL = /bin/bash
SCRIPTS="./scripts"

.PHONY: help start kill status monitor errors

help:
	@ echo ""
	@ echo "Usage:"
	@ echo "  setup: Setup Project and install requirements"
	@ echo ""

setup:
	@ chmod +x $(SCRIPTS)/*
	@ $(SCRIPTS)/setup
