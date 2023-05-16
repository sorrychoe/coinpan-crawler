.PHONY: init format lint data clear

NAME = coinpan_crawler

SHELL := bash
python = python3

ifeq ($(OS),Windows_NT)
	python := python
endif

all:
	@echo 'coinpan_crawler'
	@echo "코인판 사이트 자유게시판 크롤러"

init:
	$(python) -m pip install --upgrade pip
	$(python) -m pip install -r requirements.txt
	$(python) -m pre_commit install

format:
	$(python) -m black --config=pyproject.toml Attendance_Automation/
	$(python) -m isort --settings-file=pyproject.toml Attendance_Automation/

lint:
	$(python) -m flake8 --config=.flake8 Attendance_Automation/

data:
	@streamlit run ./coinpan_crawler/coinpan_crawler.py

clear:
	@rm -fr **/__pycache__ *.xlsx
