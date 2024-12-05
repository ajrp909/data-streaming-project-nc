test:
	venv/bin/pytest tests/

reformat:
	venv/bin/black src/ tests/

lint:
	venv/bin/flake8 src/ tests/