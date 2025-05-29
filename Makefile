PORT ?= 8000

install:
	uv sync

lint:
	uv run ruff check

start:
	uv run uvicorn src:app --host 0.0.0.0 --port $(PORT) --reload

prod-start:
	uvicorn src:app --host 0.0.0.0 --port $(PORT) --workers 5
