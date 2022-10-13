import pytest


import src.app.controller.control as control

@pytest.fixture
def example_control():
    return control.Control()
