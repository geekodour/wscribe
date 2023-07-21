import pytest


@pytest.fixture(scope="module")
def some_connection():
    """
    - This fixture is defined per module (by default is per func)
    - we can parameterize this fixture w "params". Fixture will be executed for
      each param.
    - optional arg: "request"
    """
    return "connection"


@pytest.fixture
def make_customer_record():
    """
    Factories as fixture
    """

    def _make_customer_record(name):
        return {"name": name, "orders": []}

    return _make_customer_record
