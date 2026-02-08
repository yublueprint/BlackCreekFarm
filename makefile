PYTHON_VERSION := $(shell python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null)
UNAME_S := $(shell uname -s)

ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    PYTHON_EXE := python
    VENV = venv
    PYTHON = $(VENV)/Scripts/python.exe
    PIP = $(VENV)/Scripts/pip.exe
    FLAKE8 = $(VENV)/Scripts/flake8.exe
    COVERAGE = $(VENV)/Scripts/coverage.exe
    BLACK = $(VENV)/Scripts/black.exe
    AUTOFLAKE = $(VENV)/Scripts/autoflake.exe
    ISORT = $(VENV)/Scripts/isort.exe
else
    DETECTED_OS := $(UNAME_S)
    PYTHON_EXE := python3
    VENV = venv
    PYTHON = $(VENV)/bin/python
    PIP = $(VENV)/bin/pip
    FLAKE8 = $(VENV)/bin/flake8
    COVERAGE = $(VENV)/bin/coverage
    BLACK = $(VENV)/bin/black
    AUTOFLAKE = $(VENV)/bin/autoflake
    ISORT = $(VENV)/bin/isort
endif

.PHONY: help build migrate signup run test lint coverage lint-fix clean info check-python

check-python:
	@echo "Detected Python version: $(PYTHON_VERSION)"
	@if [ "$(shell echo $(PYTHON_VERSION) | cut -d. -f1)" -ne 3 ]; then \
		echo "Python 3 is required. Detected Python version: $(PYTHON_VERSION)"; \
		exit 1; \
	fi

info: check-python
	@echo "Detected OS: $(DETECTED_OS)"

help: info
	@echo "Available commands:"
	@echo "  make build       - Setup virtual environment and install dependencies"
	@echo "  make migrate     - Apply database migrations"
	@echo "  make signup      - Create Django superuser"
	@echo "  make run         - Run Django development server"
	@echo "  make test        - Run Django tests"
	@echo "  make lint        - Run code linting with flake8"
	@echo "  make coverage    - Run tests with coverage reporting"
	@echo "  make lint-fix    - Auto-format and fix lint issues (black, autoflake, isort)"
	@echo "  make clean       - Remove virtual environment and temporary files"

build: check-python info
	$(PYTHON_EXE) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

migrate:
	$(PYTHON) manage.py migrate

signup:
	$(PYTHON) manage.py createsuperuser

run:
	$(PYTHON) manage.py collectstatic
	$(PYTHON) manage.py runserver

test:
	@echo "🧪 Running tests..."
	$(PYTHON) -m pytest -v --disable-warnings

coverage:
	@echo "📊 Generating coverage report..."
	@if [ -f .coverage ]; then \
		$(PYTHON) -m coverage report -m; \
		$(PYTHON) -m coverage html; \
		echo "→ Open htmlcov/index.html for detailed report."; \
	else \
		echo "⚠️  No .coverage data found. Run 'make test' first."; \
	fi

lint:
	$(FLAKE8) app

lint-fix:
	@echo "Running black..."
	$(BLACK) app/
	@echo "Running autoflake..."
	$(AUTOFLAKE) --in-place --remove-unused-variables --remove-all-unused-imports -r app/
	@echo "Running isort..."
	$(ISORT) app/
	@echo "Done fixing lint issues!"

clean: info
	@echo "Removing virtual environment and cache files..."
	rm -rf $(VENV)
	@find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || powershell -Command "Get-ChildItem -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force"
	@find . -type f -name "*.pyc" -delete 2>/dev/null || powershell -Command "Get-ChildItem -Recurse -Filter '*.pyc' | Remove-Item -Force"
