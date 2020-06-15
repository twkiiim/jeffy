from jeffy.sdk import SdkBase

import pytest


@pytest.fixture
def sdk_base():
    """Get SdkBase object."""
    return SdkBase()


class TestSdkBase():
    """Jeffy SDK base class test."""

    def test_convert_to_encoded_data_with_new_id(self, sdk_base, mocker):
        """It can get converted data with new correlation id."""
        sdk_base.app.correlation_id = ''
        mocker.patch('uuid.uuid4').return_value = 'bar'
        assert sdk_base.convert_to_encoded_data(data='foo', correlation_id='') == {
            'message': 'foo',
            'correlation_id': 'bar'
        }

    def test_convert_to_encoded_data_with_specified_id(self, sdk_base, mocker):
        """It can get converted data  with specified correlation id."""
        sdk_base.app.correlation_id = ''
        assert sdk_base.convert_to_encoded_data(data='foo', correlation_id='buz') == {
            'message': 'foo',
            'correlation_id': 'buz'
        }

    def test_convert_to_encoded_data_with_saved_id(self, sdk_base, mocker):
        """It can get converted data  with saved correlation id."""
        sdk_base.app.correlation_id = 'qux'
        assert sdk_base.convert_to_encoded_data(data='foo', correlation_id='') == {
            'message': 'foo',
            'correlation_id': 'qux'
        }
