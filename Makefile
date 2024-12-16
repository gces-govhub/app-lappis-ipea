setup:
	pip install poetry==1.8.5
	poetry config virtualenvs.in-project false
	poetry config warnings.export false
	poetry lock
	poetry install --no-root --with dev
	poetry export --without-hashes --format=requirements.txt > requirements.txt
	bash setup-git-hooks.sh

format:
	poetry run black .
	poetry run ruff check --fix .
	poetry run sqlfmt ./src/dbt
	poetry run sqlfluff fix ./src/dbt

lint:
	poetry run black . --check
	poetry run ruff check .
	poetry run mypy .
	poetry run sqlfmt ./src/dbt --check
	poetry run sqlfluff lint ./src/dbt

test:
	poetry run pytest tests
