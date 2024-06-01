import builtins
import logging
from time import sleep
from unittest import mock

from context_timing.context_timing import measure_time, set_log_func


def test_print():
    logging.basicConfig(level=logging.INFO)

    with mock.patch.object(builtins, "print") as m:
        set_log_func(print)
        with measure_time():
            sleep(0.1)
        m.assert_called_once()

    with mock.patch.object(logging, "info") as m:
        set_log_func(logging.info)
        with measure_time():
            sleep(0.1)
        m.assert_called_once()

    logger = logging.getLogger()
    with mock.patch.object(logger, "info") as m:
        set_log_func(logger.info)
        with measure_time():
            sleep(0.1)
        m.assert_called_once()


def test_elapsed():
    with measure_time() as m:
        sleep_time = 1
        sleep(sleep_time)
        assert abs(m.elapsed - sleep_time) < 0.05
        m.print()
