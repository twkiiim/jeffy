from jeffy.framework import get_app

app = get_app()


@app.handlers.common()
def common_example(event, context):
    """Common handler example."""
    return(event)


def test_common():
    """Common handler test."""
    assert common_example({'foo': 'bar'}, {}) == {'foo': 'bar'}
