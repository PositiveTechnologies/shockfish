clean:
	@echo "Cleaning:"
	find . -name '*.pyc' -delete

test: clean
	@echo "Testing:"
	python3.5 $(shell which nosetests) tests/

init:
	pip install -r requirements.txt
	@export "PYTHONPATH=$PYTHONPATH:`pwd`"

install: init

all: install test

.PHONY: clean test