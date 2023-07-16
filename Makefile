PYTHON ?= python3
PIP ?= pip

install:
	$(PIP) install curses datetime numpy csv matplotlib scipy

run:
	$(PYTHON) src/main.py

.phony: install run