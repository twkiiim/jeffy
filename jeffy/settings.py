import logging
from typing import List

from jeffy.logging import ContextLogger
from jeffy.logging import JsonFormatter


class Logging(object):
    """Logging setting class."""

    def __init__(
        self,
        logger: logging.Logger = ContextLogger('jeffy'),    # type: ignore
        handlers: List[logging.Handler] = [logging.StreamHandler()],
        log_level: int = logging.INFO,
        correlation_attr_name: str = 'correlation_id'
    ):
        """
        Create new logging setting.

        Parameters
        ----------
        logger: logging.Logger
            Logger
        log_level: int = logging.INFO
            Log level
        correlation_attr_name: str = 'correlation_id'
            The attribute name of log records for correlation
        """
        f = JsonFormatter()
        for h in handlers:
            h.setFormatter(f)
            logger.addHandler(h)
        logger.setLevel(log_level)
        self.logger = logger
        self.correlation_attr_name = correlation_attr_name


class RestApi(object):
    """REST API setting class."""

    def __init__(
        self,
        correlation_id_header: str = 'x-jeffy-correlation-id'
    ):
        """
        Create new http api setting.

        Parameters
        ----------
        correlation_id_header: str
            The name of correlation id header
        """
        self.correlation_id_header = correlation_id_header
