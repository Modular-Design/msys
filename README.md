# mdd
modular design and development

# Testing
till `pip 21.3`:
```
pip install --use-feature=in-tree-build .
pytest
```
`pip 21.3+`:
```
pip install .
pytest
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
| SQL Module                           | 🟦     |


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