import pytest
import logging
from core.runtime.runtime_logger import UmbraLogger, get_logger


def test_get_logger_returns_logger():
    logger = get_logger("test_umbra")
    assert isinstance(logger, logging.Logger)


def test_get_logger_same_instance():
    l1 = get_logger("singleton_test")
    l2 = get_logger("singleton_test")
    assert l1 is l2


def test_umbra_logger_info(capsys):
    logger = UmbraLogger("test_info")
    logger.info("test message")


def test_umbra_logger_warning():
    logger = UmbraLogger("test_warn")
    logger.warning("test warning")


def test_umbra_logger_error():
    logger = UmbraLogger("test_error")
    logger.error("test error")


def test_umbra_logger_debug():
    logger = UmbraLogger("test_debug")
    logger.debug("test debug")


def test_umbra_logger_critical():
    logger = UmbraLogger("test_critical")
    logger.critical("test critical")


def test_umbra_logger_has_handlers():
    logger = UmbraLogger("test_handlers")
    assert len(logger._logger.handlers) >= 1