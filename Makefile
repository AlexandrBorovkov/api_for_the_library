PORT ?= 8000

start:
	uv run uvicorn src:app --host 0.0.0.0 --port $(PORT) --reload

prod-start:
	uvicorn src:app --host 0.0.0.0 --port $(PORT) --workers 5
