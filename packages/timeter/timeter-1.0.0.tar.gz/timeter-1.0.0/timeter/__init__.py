"""A handy set of tools to measure your code execution time"""

from __future__ import annotations

import logging
import time
from functools import wraps
from typing import Any, Callable, Dict, Tuple, Literal, Union

__version__ = '1.0.0'
__all__ = ['timeter', 'timeter_decorator', 'Timer']
__author__ = 'SyberiaK <syberiakey@gmail.com>'

LogLevel = Union[Literal['ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG'], int]
Args = Tuple[Any, ...]
Kwargs = Dict[str, Any]

logger = logging.getLogger(__name__)

LOG_CONTEXT_FORMAT_SPEC_DEFAULT = 'The codeblock of "{timer_name}" timer executed for {time_elapsed} seconds'
LOG_FUNCTION_FORMAT_SPEC_DEFAULT = ('Function "{func_name}({args_kwargs})" '
                                    'executed {number_times} for {time_elapsed} seconds')


def _format_output_log(timer: Timer, format_spec: str,
                       func_name: str = None, args: Args = None, kwargs: Kwargs = None,
                       number: int = None) -> str:
    format_values = {
        'timer_name': timer.name,
        'time_elapsed': timer.time_elapsed,
    }
    args_kwargs = ''

    if func_name:
        format_values['func_name'] = func_name
    if args:
        args_repr = repr(args)
        format_values['args'] = args_repr
        args_kwargs += args_repr[1:-1]
    if kwargs:
        kwargs_repr = ', '.join(f'{str(k)}={repr(v)}' for k, v in kwargs.items())
        format_values['kwargs'] = '{' + kwargs_repr + '}'
        if args_kwargs:
            args_kwargs += ', '
        args_kwargs += kwargs_repr[1:-1]
    if number:
        format_values['number'] = number
        format_values['number_times'] = 'once' if number == 1 else f'{number} times'
    if args_kwargs:
        format_values['args_kwargs'] = args_kwargs

    formatted_str = format_spec.format_map(format_values)

    return formatted_str


def get_logging_level_name(level: str | int) -> int:
    if isinstance(level, str):
        return logging.getLevelName(level)

    return level


def timeter(
        func: Callable,
        /,
        args: Args = None,
        kwargs: Kwargs = None,
        number: int = 1,
        *,
        verbose: bool = True,
        logging_level: LogLevel = 'INFO',
        format_spec: str = LOG_FUNCTION_FORMAT_SPEC_DEFAULT
) -> Timer:
    """
    Plain function to measure a function's execution time.
    Returns a :class:`Timer` object used for measurement. You can use it to extract some useful time information.

    By default, logs the result with :module:`logging` module. Set ``verbose`` to ``False`` to turn it off.
    ``format_spec`` is being used in the logger built in the lib and supports
    various formatting keys to display useful information, such as "{timer_name}",
    "{func_name}", "{args_kwargs}", "{args}", "{kwargs}", "{number}" and "{number_times}".
    """

    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    with Timer(func.__name__, verbose=False, logging_level=logging_level, log_format_spec=format_spec) as t:
        for _ in range(number):
            func(*args, **kwargs)

    if verbose:
        t.log_measurement(func, args, kwargs, number)

    return t


def timeter_decorator(
        _func: Callable = None,
        /, *,
        logging_level: LogLevel = 'INFO',
        format_spec: str = LOG_FUNCTION_FORMAT_SPEC_DEFAULT
):
    """
    Decorator to measure an attached function's execution time every time it gets called.
    Always logs the result in ``sys.stdout`` since we can't return any useful time information while using a decorator.

    ``format_spec`` is being used in the logger built in the lib and supports
    various formatting keys to display useful information, such as "{timer_name}",
    "{func_name}", "{args_kwargs}", "{args}", "{kwargs}", "{number}" and "{number_times}".
    """

    def decorator(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            with Timer(func.__name__, verbose=False, logging_level=logging_level, log_format_spec=format_spec) as t:
                v = func(*args, **kwargs)

            t.log_measurement(func, args, kwargs)
            return v

        return inner

    if _func is None:  # called with parens (``timeter_decorator()``)
        return decorator

    return decorator(_func)  # called with no parens (``timeter_decorator``)


class Timer:
    """Provides a context manager for time measurements, as well as some other useful methods."""

    _time_func: Callable[[], float] = time.perf_counter

    def __init__(self, name: str, *, verbose: bool = True,
                 log_format_spec: str = LOG_CONTEXT_FORMAT_SPEC_DEFAULT, logging_level: LogLevel = 'INFO'):
        self.name = name
        self.startup_time: float | None = None
        self.end_time: float | None = None
        self.verbose = verbose
        self.log_format_spec = log_format_spec
        self.logging_level = get_logging_level_name(logging_level)

    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}(startup_time={self.startup_time}, '
                f'end_time={self.end_time}, time_elapsed={self.time_elapsed})')

    def __enter__(self) -> Timer:
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @property
    def started(self) -> bool:
        return self.startup_time is not None

    @property
    def finished(self) -> bool:
        return self.started and self.end_time is not None

    @property
    def time_elapsed(self) -> float:
        if self.finished:
            return self.end_time - self.startup_time
        if self.started:
            return self._time_func() - self.startup_time
        return 0

    def start(self):
        self.startup_time = self._time_func()

    def stop(self):
        self.end_time = self._time_func()
        if self.verbose:
            self.log_measurement()

    def log_measurement(self, func: Callable[..., ...] | None = None, args: Args = None, kwargs: Kwargs = None,
                        number: int = 1):
        if func is None:  # assume calling from context manager
            output_log = _format_output_log(self, self.log_format_spec)
        else:
            output_log = _format_output_log(self, self.log_format_spec, func.__name__, args, kwargs, number)

        logger.log(self.logging_level, output_log)
