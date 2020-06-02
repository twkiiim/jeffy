from jeffy.encoding.bytes import BytesEncoding

import pytest


@pytest.fixture
def bytes_encoding():
    """Get BytesEncoding class."""
    return BytesEncoding()


class TestBytesEncoding(object):
    """BytesEncoding test."""

    def test_encode(self, bytes_encoding):
        """It can get bytes object."""
        assert bytes_encoding.encode(bytes(123)) == bytes(123)

    def test_decode(self, bytes_encoding):
        """It can get bytes object."""
        assert bytes_encoding.encode(bytes(123)) == bytes(123)
