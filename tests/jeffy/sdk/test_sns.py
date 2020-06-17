import json

import botocore

from jeffy.sdk.sns import Sns

import pytest


@pytest.fixture
def sns():
    """Get Sns object."""
    return Sns()


class TestSns(object):
    """Kinesis test."""

    def test_get_resource(self, sns, mocker):
        """It can get sns client."""
        assert isinstance(sns.get_resource(), botocore.client.BaseClient)

    def test_publish(self, sns, mocker):
        """It can publish correlation id added message."""
        m = mocker.Mock()
        m.publish = mocker.Mock(return_value='foo')
        mocker.patch.object(sns, 'get_resource', return_value=m)
        sns.app.correlation_attr_name = 'correlation_id'
        sns.app.correlation_id = 'bar'
        assert sns.publish(
            message={'buz': 'qux'},
            topic_arn='topic_arn',
            subject='subject'
        ) == 'foo'
        m.publish.assert_called_with(
            TopicArn='topic_arn',
            Message=json.dumps({
                'buz': 'qux',
                'correlation_id': 'bar'
            }),
            Subject='subject'
        )
