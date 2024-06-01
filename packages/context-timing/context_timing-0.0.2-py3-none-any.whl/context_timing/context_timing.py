from contextlib import AbstractContextManager
from logging import getLogger
from time import perf_counter_ns
from typing import Callable

_timing_logger = getLogger(__file__)
_DEFAULT_LOG = _timing_logger.info


def set_log_func(func: Callable[[str], None]):
    """
    Set default log function for all follow-up contexts.
    :param func:
    :return:
    """
    global _DEFAULT_LOG
    _DEFAULT_LOG = func


class measure_time(AbstractContextManager):
    """
    Provides a simple context to keep track of time
    """

    def __init__(self, name: str = "", log_func: Callable[[str], None] = None):
        self._log_func = log_func if log_func else _DEFAULT_LOG
        self._name = f" {name}" if name else ""
        self._start_time = None
        self._elapsed_time = None

    def __enter__(self):
        self._start_time = perf_counter_ns()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._elapsed_time = (perf_counter_ns() - self._start_time) / 1e9
        self.print()

    def print(self) -> None:
        """
        Print in seconds if above 1s, else in ms. Outputs to the log function.
        :return:
        """
        elapsed_time_unit = "s"
        elapsed_time = self.elapsed

        if elapsed_time < 1:
            elapsed_time *= 1000
            elapsed_time_unit = "ms"

        if self._log_func:
            log_message = (
                f"Context{self._name} - "
                f"time elapsed since entry {elapsed_time:.3f} {elapsed_time_unit}"
            )
            try:
                self._log_func(log_message)
            except:  # noqa: E722
                pass

    @property
    def elapsed(self) -> float:
        """
        Returns time elapsed since entering the context, in seconds.
        :return:
        """
        if self._elapsed_time is None:
            return (perf_counter_ns() - self._start_time) / 1e9
        return self._elapsed_time
