.PHONY: install format crawling clear
\
NAME = coinpan_crawler

SHELL := bash
python = python3

ifeq ($(OS),Windows_NT)
	python := python
endif

all:
	@echo 'coinpan_crawler'

install:
	$(python) -m pip install $(pip_user_option) --upgrade pip \
	$(python) -m pip install $(pip_user_option) --upgrade 'build>=0.7' 'setuptools>=61.0,<64.0' 'wheel>=0.37' \
	$(python) -m pip install $(pip_user_option) -r requirements.txt \
	pre-commit install

format:
	$(python) -m isort --settings-file=setup.cfg src/
	$(python) -m flake8 --config=setup.cfg src/

crawling:
	$(python) src/crawler/coinpan_crawler.py

dashboard:
	$(python) src/main.py

clear:
	@rm -fr src/**/__pycache__

reset:
	@rm -fr src/data/*.csv
