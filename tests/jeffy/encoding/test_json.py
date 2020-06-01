import json

from jeffy.encoding import DecodeError
from jeffy.encoding.json import JsonEncoding

import pytest


@pytest.fixture
def json_encoding():
    """Get JsonFormatter class."""
    return JsonEncoding()


class TestJsonEncoding(object):
    """JsonEncoding test."""

    def test_encode(self, json_encoding):
        """It can get bytes object."""
        assert json_encoding.encode({'foo': 'bar'}) == json.dumps({'foo': 'bar'}).encode('utf-8')

    def test_decode(self, json_encoding):
        """It can get decoded object."""
        assert json_encoding.decode(json.dumps({'foo': 'bar'}).encode('utf-8')) == {'foo': 'bar'}

    def test_decode_error(self, json_encoding):
        """It can catch DecodeError."""
        with pytest.raises(DecodeError):
            json_encoding.decode('bar'.encode('utf-8'))
