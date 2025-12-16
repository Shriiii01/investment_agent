.PHONY: install test run clean

install:
	pip install -r requirements.txt

test:
	pytest

run:
	streamlit run agent.py

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

