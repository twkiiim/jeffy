import io

from jeffy.framework import get_app

app = get_app()


@app.handlers.common()
def common_example(event, context):
    """Common handler example."""
    return event


@app.handlers.s3()
def s3_example(event, context):
    """Common handler example."""
    return event


def test_common():
    """Common handler test."""
    assert common_example({'foo': 'bar'}, {}) == {'foo': 'bar'}


def test_s3(mocker):
    """S3 handler test."""
    m = mocker.Mock()
    m.get_object = mocker.Mock(return_value={
        'Metadata': {'foo': 'bar'},
        'Body': io.StringIO('buz')
    })
    s3m = mocker.Mock()
    s3m.get_resource = mocker.Mock(return_value=m)
    mocker.patch('jeffy.sdk.s3.S3').return_value = s3m
    assert s3_example({'Records': [
        {'s3': {
            'bucket': {'name': 'bucket_name'},
            'object': {'key': 'object_key'}
        }}
    ]}, {}) == [{
        'key': 'object_key',
        'bucket_name': 'bucket_name',
        'body': 'buz',
        'metadata': {'foo': 'bar'}
    }]
