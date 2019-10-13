.PHONY: start clean init update-deps

start:
	poetry shell


clean:
	poetry cache:clear --all --no-interaction -- pypi


init: clean
	poetry install


update-deps: init
	poetry update
