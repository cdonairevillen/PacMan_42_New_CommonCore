PYTHON      := python3
VENV        := .venv
ARGS        ?= config.json
REQ         := resources/requirements.txt
MAZE_WHL    := resources/mazegenerator-00001-py3-none-any.whl
HS			:= high_score

PIP         := $(VENV)/bin/pip
PY          := $(VENV)/bin/python

MYPY_FLAGS  := --warn-return-any \
               --warn-unused-ignores \
               --ignore-missing-imports \
               --disallow-untyped-defs \
               --check-untyped-defs

INSTALL_STAMP := $(VENV)/.deps_installed

all: run

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)

$(INSTALL_STAMP): $(VENV)/bin/activate $(REQ)
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install --no-cache-dir -r $(REQ)
	$(PY) -m pip install --no-cache-dir $(MAZE_WHL)
	@touch $(INSTALL_STAMP)

install: $(INSTALL_STAMP)

run: install
	$(PY) pac-man.py $(ARGS)

restart:
	@rm -rf $(HS)
	@echo "Leaderboard deleted. The new leaderboard will be generated \
	when the game is launched"

debug: install
	$(PY) pdb pac-man.py $(ARGS)

packaging: install
	.venv/bin/pip install pyinstaller
	.venv/bin/python -m PyInstaller --onefile --add-data "assets:assets" --add-data "resources:resources" --paths src pac-man.py
	cp config.json dist/config.json
	chmod +x ./dist/pac-man

lint: install
	$(PY) -m flake8 src --exclude .venv
	$(PY) -m mypy src $(MYPY_FLAGS) --exclude .venv

lint-strict: install
	$(PY) -m flake8 src --exclude .venv
	$(PY) -m mypy src --strict $(MYPY_FLAGS) --exclude .venv

clean:
	@rm -rf $(VENV)
	@rm -rf .mypy_cache
	@rm -rf dist
	@rm -rf build
	@find . -type d -name "__pycache__" -exec rm -rf {} +

re: clean run

help:
	@echo "make run                     -> Run project (default: config.json)"
	@echo "make run ARGS=mi_config.json -> Run with custom config"
	@echo "make install                 -> Install dependencies"
	@echo "make lint                    -> Run linters"
	@echo "make lint-strict             -> Run linters (strict mode)"
	@echo "make clean                   -> Clean project"
	@echo "make re                      -> Clean and run"

.PHONY: all install run debug clean lint lint-strict help re