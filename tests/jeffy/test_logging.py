import json
import logging
import os
import sys

from jeffy.logging import (
    ContextLogger,
    JsonFormatter,
    generate_correlation_id,
    get_default_logger)

import pytest


@pytest.fixture
def json_formatter():
    """Get JsonFormatter class."""
    return JsonFormatter()


@pytest.fixture
def context_logger():
    """Get ContextLogger class."""
    return ContextLogger('jeffy-test')


class DummyRecord:
    """Dummy LogRecord class."""

    pass


class TestJsonFormatter(object):
    """JsonFormatter test."""

    def test_format(self, json_formatter):
        """It can get formatted log text."""
        record = DummyRecord()
        record.created = 1
        record.msecs = 1
        record.exc_info = sys.exc_info()
        record.stack_info = 'stack_info'
        record.msg = 123
        assert json_formatter.format(record) == json.dumps({
            'created': '1970-01-01 00:00:01,001',
            "msecs": 1,
            'exc_info': 'NoneType: None',
            'stack_info': 'stack_info',
            'msg': '123'
        })


class TestContextLogger(object):
    """ContextLogger test."""

    def test_update_context(self, context_logger):
        """It can update the log context."""
        context_logger.update_context({'foo': 'bar'})
        assert context_logger.context == {
            'aws_region': os.environ.get('AWS_REGION') or os.environ.get('AWS_DEFAULT_REGION'),
            'function_name': os.environ.get('AWS_LAMBDA_FUNCTION_NAME'),
            'function_version': os.environ.get('AWS_LAMBDA_FUNCTION_VERSION'),
            'function_memory_size': os.environ.get('AWS_LAMBDA_FUNCTION_MEMORY_SIZE'),
            'log_group_name': os.environ.get('AWS_LAMBDA_LOG_GROUP_NAME'),
            'log_stream_name': os.environ.get('AWS_LAMBDA_LOG_STREAM_NAME'),
            'foo': 'bar'
        }

    def test_makeRecord(self, context_logger):
        """It can make the context added log record."""
        assert isinstance(context_logger.makeRecord(
            name='foo',
            level=logging.INFO,
            fn='bar',
            lno=123,
            msg='qux',
            args=(1, 2, 3),
            exc_info=None), logging.LogRecord)


def test_get_default_logger():
    """It can get the default logger."""
    assert isinstance(get_default_logger(), ContextLogger)


def test_generate_correlation_id():
    """It can get the new correlation_id."""
    assert isinstance(generate_correlation_id(), str)
