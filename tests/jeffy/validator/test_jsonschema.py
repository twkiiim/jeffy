from jeffy.validator import ValidationError
from jeffy.validator.jsonschema import JsonSchemeValidator

import pytest


@pytest.fixture
def jsonschema_validator():
    """Get JsonSchemeValidator class."""
    return JsonSchemeValidator(scheme={
        'type': 'object',
        'properties': {
            'message': {'type': 'string'}}})


class TestJsonSchemeValidator(object):
    """JSON scheme validator test."""

    def test_validate(self, jsonschema_validator):
        """It can validate use json scheme."""
        assert jsonschema_validator.validate({'message': 'foo'}) is None

    def test_validate_error(self, jsonschema_validator):
        """It raises ValidationError."""
        with pytest.raises(ValidationError):
            jsonschema_validator.validate({'message': 123})
