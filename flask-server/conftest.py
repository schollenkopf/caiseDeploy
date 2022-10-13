import pytest
import app.control as control


@pytest.fixture
def example_control():
    return control.Control()