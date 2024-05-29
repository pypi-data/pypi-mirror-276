## ARRIMPUTER 1.3.0

[![license](https://img.shields.io/badge/MIT-License?label=license)](https://mit-license.org/)
[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/AlphaPrime7/Imputer)
[![Awesome
Badges](https://img.shields.io/badge/badges-awesome-green.svg)](https://github.com/Naereen/badges)
[![Demandez moi n’importe quoi
!](https://img.shields.io/badge/Demandez%20moi-n'%20importe%20quoi-1abc9c.svg)](mailto:awesome.tingwei@outlook.com)
[![](https://img.shields.io/badge/follow%20me%20on-LinkedIn-green.svg)](https://www.linkedin.com/in/tingwei-adeck)

## What is it?

A machine learning algorithm/package for integer imputation into arrays. Integers are imputed and the cost difference is calculated to determine which integer yields the optimum cost reduction.

The package is designed for experimental purposes as there are possibilities of its application on data frames and other important projects that might need such a feature.

## Installation

```shell
pip install arrimputer
```
## Examples

### Base Use
```python
from ArrImputer import *
test_arr = [0,1,2,3,4,5]
get_optimum_integer(test_arr)
``` 

### Advanced Use
```python
from ArrImputer import *
test_arr = [0,1,2,3,4,5]
get_optimum_integer(test_arr,max_tries=1000)
``` 

## Code of Conduct

Everyone interacting in the project's codebases, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

## Reporting issues

Report issues to me at <awesome.tingwei@outlook.com>.