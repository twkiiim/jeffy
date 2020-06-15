from typing import Any

from jeffy import framework
from jeffy.encoding import Encoding
from jeffy.encoding.bytes import BytesEncoding


class SdkBase():
    """Jeffy SDK base class."""

    def __init__(self, encoding: Encoding = BytesEncoding()):
        """
        Initialize Jeffy SDK.

        Parameters
        ----------
        encoding: jeffy.encoding.Encoding
        """
        self.app = framework.get_app()
        self.encoding = encoding

    def convert_to_encoded_data(self, data: Any, correlation_id: str) -> bytes:
        """
        Convert the event payload data to encoded Jeffy format data.

        Parameters
        ----------
        data: Any
        correlation_id: str
        """
        if not isinstance(data, dict):
            data = {'message': data}
        if correlation_id == '':
            data[self.app.correlation_attr_name] = self.app.correlation_id
        else:
            data[self.app.correlation_attr_name] = correlation_id
        return self.encoding.encode(data)
