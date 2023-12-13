from tastebudz import create_app

def test_config():
    # Make sure we can add testing flag in config:
    assert not create_app().app.testing
    assert create_app({"TESTING": True}).app.testing