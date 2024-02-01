# content of conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--test-size", action="store", type=int, default=3, help="Specify the test size")

@pytest.fixture
def test_size(request):
    return request.config.getoption("--test-size")
