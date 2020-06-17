from jeffy.validator import ValidationError
from jeffy.validator.jsonschema import JsonSchemaValidator

import pytest


@pytest.fixture
def jsonschema_validator():
    """Get JsonSchemaValidator class."""
    return JsonSchemaValidator(schema={
        'type': 'object',
        'properties': {
            'message': {'type': 'string'}}})


class TestJsonSchemaValidator(object):
    """JSON scheme validator test."""

    def test_validate(self, jsonschema_validator):
        """It can validate use json scheme."""
        assert jsonschema_validator.validate({'message': 'foo'}) is None

    def test_validate_error(self, jsonschema_validator):
        """It raises ValidationError."""
        with pytest.raises(ValidationError):
            jsonschema_validator.validate({'message': 123})
