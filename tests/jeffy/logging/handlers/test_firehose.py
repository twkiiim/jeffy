from jeffy.logging import JsonFormatter
from jeffy.logging.handlers.firehose import KinesisFirehoseHandler

import pytest


@pytest.fixture
def kinesis_firehose_handler():
    """Get KinesisFirehoseHandler object."""
    h = KinesisFirehoseHandler()
    h.setFormatter(JsonFormatter())
    return h


class DummyRecord:
    """Dummy LogRecord class."""

    pass


class TestKinesisFirehoseHandler(object):
    """KinesisFirehoseHandler test."""

    def test_emit(self, kinesis_firehose_handler):
        """It can emit log record."""
        assert kinesis_firehose_handler.emit(DummyRecord()) is None
