ruff = uv run ruff check .
pytest = uv run pytest --cov=.

.PHONY: format
format:
	uv run ruff check . --fix

.PHONY: lint
lint:
	$(ruff)

.PHONY: test
test:
	$(pytest) tests

.PHONY: test_with_report
test_with_report:
	$(pytest) tests --cov-report=xml