import botocore

from jeffy.sdk.s3 import S3

import pytest


@pytest.fixture
def s3():
    """Get S3 object."""
    return S3()


class TestS3(object):
    """Kinesis test."""

    def test_get_resource(self, s3, mocker):
        """It can get s3 client."""
        assert isinstance(s3.get_resource(), botocore.client.BaseClient)

    def test_upload_file(self, s3, mocker):
        """It can upload correlation id added file."""
        m = mocker.Mock()
        m.upload_file = mocker.Mock(return_value='foo')
        mocker.patch.object(s3, 'get_resource', return_value=m)
        s3.app.correlation_id = 'correlation_id'
        assert s3.upload_file(
            file_path='/foo/bar.txt',
            bucket_name='bucket_name',
            key='key'
        ) is None
        m.upload_file.assert_called_with(
            Filename='/foo/bar.txt',
            Bucket='bucket_name',
            Key='key',
            ExtraArgs={
                'Metadata': {
                    s3.app.correlation_attr_name: 'correlation_id'
                }
            }
        )
