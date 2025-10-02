# Course Link Getter Makefile

.PHONY: test test-quick install clean help

# Default target
help:
	@echo "Available targets:"
	@echo "  test        - Run all tests with verbose output"
	@echo "  test-quick  - Run tests quickly (pytest -q)"
	@echo "  install     - Install dependencies"
	@echo "  clean       - Clean up temporary files"
	@echo "  ci          - Run CI-friendly tests"

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests with verbose output
test:
	python -m pytest tests/test_store.py -v

# Run tests quickly (CI-friendly)
test-quick:
	python -m pytest tests/test_store.py -q

# CI-friendly test command
ci: test-quick

# Clean up temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +