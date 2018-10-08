.PHONY: test

coverage:
	coverage run -m unittest discover

lint:
	flake8 quince

test:
	python -m unittest discover

run:
	python -m quince.main

build-osx:
	rm -rf build dist
	python3 setup.py py2app --packages=PIL
