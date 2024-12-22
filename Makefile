coffee:
	@printf 'Enjoy your coffee! ☕️\n'

lint:
	@poetry run black .
	@poetry run isort . --profile black
	@poetry run flake8 .

pre-commit:
	pre-commit run --all-files --show-diff-on-failure

.PHONY: coffee lint pre-commit