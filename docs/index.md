# MDD
>modular design and development

![workflow](https://github.com/willi-z/mdd/actions/workflows/ci.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/willi-z/mdd/branch/main/graph/badge.svg?token=CG4DIOZZ6C)](https://codecov.io/gh/willi-z/mdd)
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