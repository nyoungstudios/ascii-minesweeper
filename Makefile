help:
	@echo 'help - Show this message'
	@echo 'run - Runs the minesweeper game'
	@echo 'clean - Removes all Python cache and temporary files'
	@echo 'clean-all - Removes all Python cache, temporary files, and build folders'
	@echo 'clean-build - Removes Python build folders'
	@echo 'install - Installs this Python package'

clean: clean-pyc

clean-all: clean-pyc clean-build

clean-pyc:
	@find . -type f -name '*.pyc' -exec rm -f {} +
	@find . -type f -name '*.pyo' -exec rm -f {} +
	@find . -type f -name '*~' -exec rm -f {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +

clean-build:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info

run:
	@python minesweeper/play.py

install:
	@python setup.py install
