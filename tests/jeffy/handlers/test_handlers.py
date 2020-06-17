import base64
import json

from jeffy import framework
from jeffy.encoding import DecodeError
from jeffy.settings import Logging, RestApi

import pytest


@pytest.fixture
def handlers():
    """Get Handlers class."""
    app = framework.get_app(
        logging=Logging(correlation_attr_name='foo'),
        rest_api=RestApi(correlation_id_header='x-bar-id'))
    return app.handlers


class TestHandlers(object):
    """Handlers test."""

    def test_capture_correlation_id(self, handlers):
        """It can get correlation id by http header."""
        assert handlers.capture_correlation_id({
            'aaa': 'bbb',
            'ccc': 'ddd'
        }) not in ['bbb', 'ddd']

    def test_capture_correlation_id_by_attr_name(self, handlers):
        """It can get correlation id by attribute name."""
        assert handlers.capture_correlation_id({
            'foo': 'bar',
            'buz': 'qux'
        }) == 'bar'

    def test_capture_correlation_id_by_header(self, handlers):
        """It can get correlation id by http header name."""
        assert handlers.capture_correlation_id({
            'headers': {
                'x-foo-id': 'bar',
                'x-bar-id': 'qux'
            }
        }) == 'qux'

    def test_dynamodb_streams(self, handlers, mocker):
        """It can process dynamodb stream events."""
        mock = mocker.Mock(return_value='foo')
        dynamodb_streams = handlers.dynamodb_streams()
        _dynamodb_streams = dynamodb_streams(mock)
        assert _dynamodb_streams(
            {'Records': [{'dynamodb': {'buz': 'qux'}}]},
            None
        ) == ['foo']

    def test_dynamodb_streams_error(self, handlers, mocker):
        """It raises a exception."""
        mock = mocker.Mock(side_effect=Exception('foo'))
        dynamodb_streams = handlers.dynamodb_streams()
        _dynamodb_streams = dynamodb_streams(mock)
        with pytest.raises(Exception):
            _dynamodb_streams({'Records': [{'dynamodb': {'buz': 'qux'}}]}, None)

    def test_kinesis_streams(self, handlers, mocker):
        """It can process kinesis stream events."""
        mock = mocker.Mock(return_value='foo')
        kinesis_streams = handlers.kinesis_streams()
        _kinesis_streams = kinesis_streams(mock)
        assert _kinesis_streams(
            {'Records': [{'kinesis': {'data': base64.b64encode(json.dumps({'bar': 'buz'}).encode('utf-8'))}}]},
            None
        ) == ['foo']

    def test_kinesis_streams_error(self, handlers, mocker):
        """It raises a exception."""
        mock = mocker.Mock(side_effect=Exception('foo'))
        kinesis_streams = handlers.kinesis_streams()
        _kinesis_streams = kinesis_streams(mock)
        with pytest.raises(Exception):
            _kinesis_streams(
                {'Records': [{'kinesis': {'data': base64.b64encode(json.dumps({'bar': 'buz'}).encode('utf-8'))}}]},
                None)

    def test_sqs(self, handlers, mocker):
        """It can process sqs events."""
        mock = mocker.Mock(return_value='foo')
        sqs = handlers.sqs()
        _sqs = sqs(mock)
        assert _sqs(
            {'Records': [{'body': json.dumps({'bar': 'buz'})}]},
            None
        ) == ['foo']

    def test_sqs_error(self, handlers, mocker):
        """It raises a exception."""
        mock = mocker.Mock(side_effect=Exception('foo'))
        sqs = handlers.sqs()
        _sqs = sqs(mock)
        with pytest.raises(Exception):
            _sqs({'Records': [{'body': json.dumps({'bar': 'buz'})}]}, None)

    def test_sns(self, handlers, mocker):
        """It can process sns events."""
        mock = mocker.Mock(return_value='foo')
        sns = handlers.sns()
        _sns = sns(mock)
        assert _sns(
            {'Records': [{'Sns': {'Message': json.dumps({'bar': 'buz'})}}]},
            None
        ) == ['foo']

    def test_sns_error(self, handlers, mocker):
        """It raises a exception."""
        mock = mocker.Mock(side_effect=Exception('foo'))
        sns = handlers.sns()
        _sns = sns(mock)
        with pytest.raises(Exception):
            _sns({'Records': [{'Sns': {'Message': json.dumps({'bar': 'buz'})}}]}, None)

    def test_schedule(self, handlers, mocker):
        """It can process sns events."""
        mock = mocker.Mock(return_value='foo')
        schedule = handlers.schedule()
        _schedule = schedule(mock)
        assert _schedule({'bar': 'buz'}, None) == 'foo'

    def test_schedule_error(self, handlers, mocker):
        """It raises a exception."""
        mock = mocker.Mock(side_effect=Exception('foo'))
        schedule = handlers.schedule()
        _schedule = schedule(mock)
        with pytest.raises(Exception):
            _schedule({'bar': 'buz'}, None)

    def test_s3(self, handlers, mocker):
        """It can process s3 events."""
        mock = mocker.Mock(return_value='foo')
        s3 = handlers.s3()
        _s3 = s3(mock)
        mocker.patch('jeffy.sdk.s3.S3')
        assert _s3(
            {'Records': [
                {'s3': {
                    'bucket': {'name': 'bar'},
                    'object': {'key': 'buz'}
                }}
            ]},
            None
        ) == ['foo']

    def test_s3_error(self, handlers, mocker):
        """It raises a exception."""
        mock = mocker.Mock(side_effect=Exception('foo'))
        s3 = handlers.s3()
        _s3 = s3(mock)
        with pytest.raises(Exception):
            _s3({
                'Records': [
                    {'s3': {
                        'bucket': {'name': 'bar'},
                        'object': {'key': 'buz'}
                    }}
                ]}, None)

    def test_rest_api(self, handlers, mocker):
        """It can process rest api events."""
        mock = mocker.Mock(return_value={'headers': {'foo': 'bar'}})
        rest_api = handlers.rest_api()
        _rest_api = rest_api(mock)
        assert _rest_api(
            {
                'headers': {'foo': 'bar', 'x-bar-id': 'correlation_id'},
                'body': json.dumps({'buz': 'qux'})
            },
            None
        ) == {'headers': {'foo': 'bar', 'x-bar-id': 'correlation_id'}}

    def test_rest_api_error(self, handlers, mocker):
        """It raises a exception."""
        mock = mocker.Mock(side_effect=Exception('foo'))
        rest_api = handlers.rest_api()
        _rest_api = rest_api(mock)
        with pytest.raises(Exception):
            _rest_api(
                {
                    'headers': {'foo': 'bar', 'x-bar-id': 'correlation_id'},
                    'body': json.dumps({'buz': 'qux'})
                }, None)

    def test_rest_api_400(self, handlers, mocker):
        """If it raises DecodeError then it return 400 status."""
        mock = mocker.Mock(side_effect=DecodeError('foo'))
        rest_api = handlers.rest_api()
        _rest_api = rest_api(mock)
        assert _rest_api(
            {
                'statusCode': 400,
                'headers': {'foo': 'bar', 'x-bar-id': 'correlation_id'},
                'body': 'buz'
            },
            None
        ) == {
            'statusCode': 400,
            'headers': {'x-bar-id': 'correlation_id'},
            'body': json.dumps({'error_message': 'Expecting value: line 1 column 1 (char 0)'})
        }

    def test_common(self, handlers, mocker):
        """It can process common events."""
        mock = mocker.Mock(return_value='foo')
        common = handlers.common()
        _common = common(mock)
        assert _common({'bar': 'buz'}, None) == 'foo'

    def test_common_error(self, handlers, mocker):
        """It raises a exception."""
        mock = mocker.Mock(side_effect=Exception('foo'))
        common = handlers.common()
        _common = common(mock)
        with pytest.raises(Exception):
            _common({'bar': 'buz'}, None)
