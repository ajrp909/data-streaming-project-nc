test:
	venv/bin/pytest tests/

lint:
	venv/bin/flake8 src/ tests/