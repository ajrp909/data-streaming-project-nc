test:
	venv/bin/pytest tests/ -vrP --testdox

reformat:
	venv/bin/black src/ tests/ --line-length 79 

lint:
	venv/bin/flake8 src/ tests/ -v

mypy:
	venv/bin/mypy src/ tests/ --check-untyped-defs

security:
	venv/bin/bandit -r src/

checks:
	make test
	make reformat
	make lint
	make mypy
	make security