.PHONY: test

coverage:
	coverage run -m unittest discover

lint:
	flake8

test:
	python -m unittest discover

run:
	python -m quince.main