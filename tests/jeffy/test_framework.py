from jeffy import framework


def test_get_app():
    """It can get Jeffy object."""
    assert isinstance(
        framework.get_app(),
        framework.Jeffy)
