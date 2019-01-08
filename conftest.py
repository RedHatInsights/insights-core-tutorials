# This is configuration file for pytest.
# Pytest first searches this file before running unit tests.

# Enable logging output in stderr for failing tests.
import logging


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False, help="run slow tests")
    parser.addoption("--appdebug", action="store_true", default=False, help="debug loggging")
    parser.addoption("--smokey", action="store_true", default=False, help="run tests fast")


def pytest_configure(config):
    level = logging.DEBUG if config.getoption("--appdebug") else logging.ERROR
    logging.basicConfig(level=level)
