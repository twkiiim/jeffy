import json

import botocore

from jeffy.sdk.kinesis import Kinesis

import pytest


@pytest.fixture
def kinesis():
    """Get Kinesis object."""
    return Kinesis()


class TestKinesis(object):
    """Kinesis test."""

    def test_get_resource(self, kinesis, mocker):
        """It can get kinesis client."""
        assert isinstance(kinesis.get_resource(), botocore.client.BaseClient)

    def test_put_record(self, kinesis, mocker):
        """It can put correlation id added record."""
        m = mocker.Mock()
        m.put_record = mocker.Mock(return_value='foo')
        mocker.patch.object(kinesis, 'get_resource', return_value=m)
        kinesis.app.correlation_attr_name = 'correlation_id'
        kinesis.app.correlation_id = 'bar'
        assert kinesis.put_record(
            stream_name='stream_name',
            data={'buz': 'qux'},
            partition_key='partition_key'
        ) == 'foo'
        m.put_record.assert_called_with(
            StreamName='stream_name',
            Data=json.dumps({
                'buz': 'qux',
                kinesis.app.correlation_attr_name: 'bar'
            }).encode('utf-8'),
            PartitionKey='partition_key'
        )
