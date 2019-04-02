SHELL:=/bin/bash
PROJECT:=radio
all: build test

test:
	( \
		source venv/bin/activate; \
		coverage run --branch --source=${PROJECT} --omit="*test*" -m pytest ${PROJECT}/test/; \
		coverage report; \
		echo ; echo ; \
		echo "===== Methods >= 3 Complexity Below =====" ; \
		echo ; \
		find ./radio/*.py | xargs -L1 python3 -m mccabe --min=4; \
		echo ; echo ; \
		echo "===== Tests > 4 Complexity Below =====" ; \
		echo ; \
		find ./radio/test/*.py | xargs -L1 python3 -m mccabe --min=6; \
		echo ; echo ; \
	)

build:
	python3.6 -m venv venv
	( \
		source venv/bin/activate; \
		pip install -r requirements.txt; \
		pip install -e .; \
	)

run:
	( \
		source venv/bin/activate; \
		./cli.py; \
	)

clean:
	rm -rf venv/
	rm -rf .tox/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf *.egg-info
	rm -rf .coverage
	find ${PROJECT} -name "__pycache__" -type d -exec rm -rf {} +
