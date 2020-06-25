import logging

import boto3


class KinesisFirehoseHandler(logging.Handler):
    """Amazon Kinesis Firehose logging handler."""

    def __init__(self, *args, **kwargs):    # type: ignore
        super(KinesisFirehoseHandler, self).__init__(
            level=kwargs.pop('level', logging.NOTSET))
        self.stream_name = kwargs.pop('stream_name', None)
        self.client = boto3.client('firehose', **kwargs)

    def emit(self, record):     # type: ignore
        """Emit log record."""
        try:
            self.client.put_record(
                DeliveryStreamName=self.stream_name,
                Record={'Data': self.format(record)})
        except Exception:
            self.handleError(record)
