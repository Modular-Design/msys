# MSYS
> A Framework for modular Systems

[![pip](https://img.shields.io/pypi/v/msys.svg)](https://pypi.org/project/msys/)
[![Documentation Status](https://readthedocs.org/projects/msys-docs/badge/?version=latest)](https://msys-docs.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/363596972.svg)](https://zenodo.org/badge/latestdoi/363596972)
![workflow](https://github.com/willi-z/msys/actions/workflows/ci.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/willi-z/msys/branch/main/graph/badge.svg?token=CG4DIOZZ6C)](https://codecov.io/gh/willi-z/msys)

See the [Documentation](https://msys-docs.readthedocs.io/en/latest/) form more information.

## Usage
Launch server with:
```shell
msys
```
or
```shell
msys serve
```
further details with:
```shell
msys serve --help
```

list all commands with:
```shell
msys --help
```

## Testing
till `pip 21.3`:
```shell
pip install --use-feature=in-tree-build -e .
```
`pip 21.3+`:
```shell
pip install -e .
```

```shell
coverage run --source=src -m pytest && coverage report -m
```

Check registered modules and launch server:
```shell
msys modules serve
```

## Capabilities

Legend:

| Symbol | Meaning                              |
| ------ | ------------------------------------ |
| ✅     | finished                             |
| 🔜     | working on implementation            |
| 🟦     | planned                              |


### Core

| Capability                           | Status |
| ------------------------------------ | ------ |
| Types                                | ✅     |
| Connectables                         | ✅     |
| Module                               | ✅     |
| Extensions                           | 🔜     |
| API                                  | 🔜     |

### Server

| Capability                           | Status |
| ------------------------------------ | ------ |
| create, save and load                | 🟦     |
| change                               | 🟦     |
