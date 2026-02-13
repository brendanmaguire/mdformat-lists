##############
# Tests
##############
.PHONY: unit-test
unit-test:
	uv run pytest

.PHONY: coverage
coverage:
	uv run pytest --cov --cov-report=term-missing --cov-report=html

##############
# Code Quality
##############
.PHONY: type-check
type-check:
	uv run ty check

.PHONY: lint
lint:
	uv run ruff check
	uv run ruff format --check
	uv run mdformat *.md --check --number

.PHONY: code-quality-check
code-quality-check: lint type-check

.PHONY: format
format:
	uv run ruff check --fix
	uv run ruff format
	uv run mdformat *.md --number
