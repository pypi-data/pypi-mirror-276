# timeter

[![PyPI release]][pypi]
[![Python supported versions]][pypi]
[![License]](./LICENSE)

`timeter` is a simple package with a handy set of tools to measure your code execution time.
Having a plain function, a decorator and a context manager, it becomes easier to "timeit" in specific scenarios.

```python
import functools
import logging
import operator

import timeter

logging.basicConfig(level=logging.INFO,  # don't forget to setup logging!
                    format='[{levelname}] {message}',
                    style='{')


def mult(*numbers: float) -> float:
    return functools.reduce(operator.mul, numbers, 1)


@timeter.timeter_decorator(format_spec='Computed factorial of {args} for {time_elapsed} seconds')
def factorial(n: int) -> int:
    return int(mult(*(range(2, n + 1))))


def pow(n: float, power: int, /) -> float:  # warning: incredibly slow
    return mult(*([n] * power))


timeter.timeter(mult, (2, 3, 4),
                number=10)  # [INFO] Function "mult(2, 3, 4)" executed 10 times for 6.999999999646178e-06 seconds
factorial(6)  # [INFO] Computed factorial of (6,) for 2.300000000003688e-06 seconds

n, power = 2, 2 ** 18
with timeter.Timer('math time', verbose=False) as t:
    pow(n, power)

print(f'Started at {t.startup_time=}')  # Started at t.startup_time=0.0384101
print(f'Finished at {t.end_time=}')  # Finished at t.end_time=1.1512166
print(f'{t.time_elapsed} seconds to compute pow({n}, {power})')  # 1.1128065 seconds to compute pow(2, 262144)
```

## Install

```
pip install timeter
```

## Usage

`timeter` contains three pieces:

- `timeter` function to measure execution time for a single function:

```python
timeter.timeter(mult, (2, 3, 4),
                number=10)  # [INFO] Function "mult(2, 3, 4)" executed 10 times for 6.999999999646178e-06 
```

- `timeter_decorator` to measure each function's call execution time:

```python
@timeter.timeter_decorator(format_spec='Computed factorial of {args} for {time_elapsed} seconds')
def factorial(n: int) -> int: ...
```

- `Timer` class supporting context manager:

```python
with timeter.Timer('math time', verbose=False, logging_level='DEBUG') as t:
    pow(n, power)
```

By default, the result is being print out into `sys.stdout`. Hence,
you need to set up some basic logging with `logging` module to see the results.
However, you can set `verbose` argument to `False` (except in `timeter_decorator`)
to manipulate the resulted data by yourself.

You can also change how results get printed by changing `format_spec`.
See code documentation to see available format values!

## P.S.

This library is pretty experimental and may have a questionable API.
If you have any suggestions - please leave them in issues.

[pypi]: https://pypi.org/project/timeter/

[PyPI Release]: https://img.shields.io/pypi/v/timeter.svg?label=pypi&color=green

[Python supported versions]: https://img.shields.io/pypi/pyversions/timeter.svg?label=%20&logo=python&logoColor=white

[License]: https://img.shields.io/pypi/l/timeter.svg?style=flat&label=license

