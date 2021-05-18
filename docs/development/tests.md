# Tests

The Reporting-System uses [PyTest](https://docs.pytest.org/en/6.2.x/) to run all Unit-Tests.

## Reports
till `pip 21.3`:
```sh
pip install --use-feature=in-tree-build -e .
```
`pip 21.3+`:
```sh
pip install -e .
```

`pytest` or 
```sh
coverage run --source=src -m pytest && coverage report -m
```

## The Test Structure

### File Placement and Naming Convention
Tests are located in the ``tests`` folder. The overall structure mimics the structure of the source-code.
This means that all tests files are named after the python script the test.
For example:

The class and methods of the file ``src/reporting/core/input.py`` are tested by the ``tests/core/test_input.py`` script.

### Flagging

### Fixtures
