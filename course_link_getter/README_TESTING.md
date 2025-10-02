# Course Link Getter - Testing Guide

## Overview

This project includes comprehensive pytest-based tests for the CatalogStore functionality. All tests are designed to be CI-friendly and run under 2 seconds.

## Test Structure

### Test File: `tests/test_store.py`

- **15 test cases** covering all CatalogStore functionality
- **Fixtures** for sample catalog data and loaded store
- **Performance tests** ensuring operations complete under 2 seconds
- **Model validation** for Course and Category structures

### Test Categories

1. **Data Loading Tests**
   - Load catalog from JSON file
   - Handle non-existent files
   - Validate catalog structure

2. **Filter Tests**
   - Category-only filtering
   - Category + subcategory filtering
   - Text search on titles and tags
   - Case-insensitive search
   - Combined filters
   - No matches scenarios

3. **Data Validation Tests**
   - Course model validation
   - Category model validation
   - Required fields and data types
   - Link format validation

4. **Performance Tests**
   - Operations complete under 2 seconds
   - Bulk operations efficiency

## Running Tests

### Quick Test (CI-friendly)
```bash
# Run tests with minimal output
python -m pytest tests/test_store.py -q

# Using Makefile
make test-quick
```

### Verbose Test
```bash
# Run tests with detailed output
python -m pytest tests/test_store.py -v

# Using Makefile
make test
```

### All Tests
```bash
# Run all tests in the project
python -m pytest

# Using Makefile
make ci
```

## CI/CD Setup

### GitHub Actions

The project includes two GitHub Actions workflows:

1. **`.github/workflows/ci.yml`** - Simple CI workflow
2. **`.github/workflows/test.yml`** - Comprehensive testing with coverage

### Local CI Simulation

```bash
# Install dependencies
make install

# Run CI tests
make ci

# Clean up
make clean
```

## Test Requirements

### Dependencies
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting (optional)
- `platformdirs` - Cross-platform directories

### Sample Data
- Tests use `assets/catalog.sample.json` fixture
- Contains 26+ courses across 3 categories
- Validates >= 20 courses requirement

## Test Results

### Performance
- **Total runtime**: ~0.07 seconds
- **Well under 2-second requirement**
- **15 tests passed**

### Coverage
- All CatalogStore methods tested
- All filter combinations covered
- Error scenarios included
- Model validation comprehensive

## CI-Friendly Features

1. **Fast Execution**: All tests complete in under 2 seconds
2. **No External Dependencies**: Uses local sample data
3. **Deterministic**: No random or time-dependent tests
4. **Clean Output**: Minimal output with `-q` flag
5. **Exit Codes**: Proper exit codes for CI systems

## Test Commands Reference

```bash
# Basic test execution
pytest tests/test_store.py

# Quick test (CI-friendly)
pytest tests/test_store.py -q

# Verbose test
pytest tests/test_store.py -v

# With coverage
pytest tests/test_store.py --cov=core

# Specific test
pytest tests/test_store.py::TestCatalogStore::test_filter_category_only

# Using Makefile
make test-quick    # Quick tests
make test         # Verbose tests
make ci           # CI tests
make clean        # Clean up
```

## Troubleshooting

### Common Issues

1. **Module not found**: Ensure you're in the `course_link_getter` directory
2. **Sample data missing**: Verify `assets/catalog.sample.json` exists
3. **Dependencies missing**: Run `make install` or `pip install -r requirements.txt`

### Debug Mode

```bash
# Run with debug output
pytest tests/test_store.py -v -s

# Run specific test with debug
pytest tests/test_store.py::TestCatalogStore::test_filter_category_only -v -s
```

## Contributing

When adding new tests:

1. Follow the existing test structure
2. Use fixtures for data setup
3. Ensure tests run under 2 seconds
4. Include both positive and negative test cases
5. Add performance tests for new functionality

## Test Data

The test suite uses `assets/catalog.sample.json` which contains:
- **26 courses** across 3 categories
- **English**: IELTS, TOEIC, Speaking subcategories
- **Programming**: Python, Web, Data subcategories  
- **Design**: UI/UX, Graphic subcategories
- **Valid HTTP links** for all courses
- **Diverse providers** and tags
