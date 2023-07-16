PYTHON ?= python3
PIP ?= pip

install:
	$(PIP) install curses datetime numpy csv matplotlib

run:
	$(PYTHON) main.py

.phony: install run