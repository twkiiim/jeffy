import functools
from typing import Callable

from jeffy.encoding import Encoding
from jeffy.encoding.json import JsonEncoding
from jeffy.validator import NoneValidator, Validator


class SnsHandlerMixin(object):
    """SNS event handler decorators."""

    def sns(
        self,
        encoding: Encoding = JsonEncoding(),
        validator: Validator = NoneValidator()
    ) -> Callable:
        """
        Decorator for SNS event.

        Automatically divide 'Records' for making it easy to treat it
        inside main process of Lambda.

        Usage::
            >>> from jeffy.framework import get_app
            >>> app = get_app()
            >>> @app.handlers.sns()
            ... def handler(event, context):
            ...     return event['body']['foo']
        """
        def _sns(func: Callable):           # type: ignore
            @functools.wraps(func)
            def wrapper(event, context):    # type: ignore
                ret = []
                for record in event['Records']:
                    message = encoding.decode(record['Sns']['Message'].encode('utf-8'))
                    validator.validate(message)
                    self.capture_correlation_id(message)
                try:
                    self.app.logger.info(message)
                    result = func(message, context)
                    self.app.logger.info(result)
                    ret.append(result)
                except Exception as e:
                    self.app.logger.exception(e)
                    raise e
                return ret
            return wrapper
        return _sns

    def sns_raw(
        self,
        encoding: Encoding = JsonEncoding(),
        validator: Validator = NoneValidator()
    ) -> Callable:
        """
        Decorator for SNS raw event (with all metadatas).

        Automatically divide 'Records' and pass the record to main process of Lambda.

        Usage::
            >>> from jeffy.framework import get_app
            >>> app = get_app()
            >>> @app.handlers.sns_raw()
            ... def handler(event, context):
            ...     return event['Sns']['Message']
        """
        def _sns_raw(func: Callable):     # type: ignore
            @functools.wraps(func)
            def wrapper(event, context):            # type: ignore
                ret = []
                for record in event['Records']:
                    message = encoding.decode(record['Sns']['Message'].encode('utf-8'))
                    validator.validate(message)
                    self.capture_correlation_id(message)
                    record['Sns']['Message'] = message
                try:
                    self.app.logger.info(message)
                    result = func(record, context)
                    self.app.logger.info(result)
                    ret.append(result)
                except Exception as e:
                    self.app.logger.exception(e)
                    raise e
                return ret
            return wrapper
        return _sns_raw
