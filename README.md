# MSYS
> A Framework for modular Systems

[![pip](https://img.shields.io/pypi/v/msys.svg?maxAge=3600)](https://pypi.org/project/msys/)
![workflow](https://github.com/willi-z/msys/actions/workflows/ci.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/willi-z/msys/branch/main/graph/badge.svg?token=CG4DIOZZ6C)](https://codecov.io/gh/willi-z/msys)
[![Documentation Status](https://readthedocs.org/projects/msys-docs/badge/?version=latest)](https://msys-docs.readthedocs.io/en/latest/?badge=latest)

## Testing
till `pip 21.3`:
```
pip install --use-feature=in-tree-build -e .
```
`pip 21.3+`:
```
pip install -e .
```

```
coverage run --source=src -m pytest
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
| Inputs and Outputs                   | ✅     |
| Module                               | ✅     |
| Processor                            | ✅     |
| Expression Parser                    | ✅     |
| Optimizer                            | 🔜     |
| API                                  | 🔜     |


### Modules

| Capability                           | Status |
| ------------------------------------ | ------ |
| Plugin system                        | ✅     |
| Math Module                          | ✅     |
| Processor                            | 🔜     |
| HTML Module                          | 🟦     |
| SQL Module                           | 🟦     |

### Types

| Capability                           | Status |
| ------------------------------------ | ------ |
| Vector                               | ✅     |
| File                                 | 🟦     |

### Optimizers

| Capability                           | Status |
| ------------------------------------ | ------ |
| Evolutionary Optimisation            | 🟦     |

### Server

| Capability                           | Status |
| ------------------------------------ | ------ |
| create, save and load                | 🟦     |
| change                               | 🟦     |

### Documentation

| Capability                           | Status |
| ------------------------------------ | ------ |
| Installation                         | 🟦     |
| Configuration                        | 🟦     |
| Core                                 | 🟦     |
| Modules                              | 🟦     |
| Optimisation                         | 🟦     |
| Server and API                       | 🟦     |