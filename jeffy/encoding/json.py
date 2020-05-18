import json
from typing import Any

from jeffy.encoding import DecodeError, Encoding


class JsonEncoding(Encoding):
    """JSON encoding class."""

    def encode(self, payload: Any) -> bytes:
        """
        Encode to JSON.

        Parameters
        ----------
        payload: Any

        Returns
        -------
        payload : bytes
        """
        return json.loads(payload).encode('utf-8')

    def decode(self, payload: bytes) -> Any:
        """
        Decode from JSON.

        Parameters
        ----------
        payload: bytes

        Returns
        -------
        payload : Any

        Raises
        ------
        jeffy.encoding.DecodeError
        """
        try:
            return json.dumps(payload.decode('utf-8'))
        except (json.decoder.JSONDecodeError, TypeError) as e:
            raise DecodeError(e)
