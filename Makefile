test:
	venv/bin/pytest tests/

reformat:
	venv/bin/black src/ tests/

lint:
	venv/bin/flake8 src/ tests/

mypy:
	venv/bin/mypy src/ tests/

security:
	venv/bin/bandit -r src/

checks:
	make test
	make reformat
	make lint
	make mypy
	make security