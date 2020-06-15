import json

import botocore

from jeffy.sdk.sqs import Sqs

import pytest


@pytest.fixture
def sqs():
    """Get SQS object."""
    return Sqs()


class TestSqs(object):
    """Kinesis test."""

    def test_get_resource(self, sqs, mocker):
        """It can get sqs client."""
        assert isinstance(sqs.get_resource(), botocore.client.BaseClient)

    def test_send_message(self, sqs, mocker):
        """It can put correlation id added message."""
        m = mocker.Mock()
        m.send_message = mocker.Mock(return_value='foo')
        mocker.patch.object(sqs, 'get_resource', return_value=m)
        sqs.app.correlation_attr_name = 'correlation_id'
        sqs.app.correlation_id = 'bar'
        assert sqs.send_message(
            message={'buz': 'qux'},
            queue_url='queue_url',
        ) == 'foo'
        m.send_message.assert_called_with(
            QueueUrl='queue_url',
            MessageBody=json.dumps({
                'buz': 'qux',
                'correlation_id': 'bar'
            })
        )
