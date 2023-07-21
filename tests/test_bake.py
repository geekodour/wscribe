import logging

import pytest

from bake import kitchen

L = logging.getLogger(__name__)


def test_example_assert_and_logger():
    L.info(__name__)
    L.warning("eggs warning")
    L.error("eggs error")
    L.critical("eggs critical")
    assert kitchen.do_something() == 22


class TestExampleClass:
    """
    functions(tests) inside classes in test files get unique instance of the
    class. So we get test isolation.
    """

    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "capitalize")


@pytest.fixture
def example_fixture():
    """
    - To use a fixture, we must pass it as an argument to the test function
    - fixtures are funcs that can create data/doubles/setup system state etc.
      - yield can be used for teardowns. For order safety, prefer atomic fixtures
    - pytest --fixtures -v : Lists all available fixtures including ones defined my me
    """
    return 1


def test_example_with_fixture(example_fixture):
    assert example_fixture == 1


@pytest.mark.parametrize(
    "some_text",
    [
        "",
        "a",
        "Bob",
        "Never odd or even",
        "Do geese see God?",
    ],
)
def test_example_parametrize(some_text):
    """
    parametarized markers useful when u have different inputs for the same
    kind of test. (naive way is to have all these in one test, but that way
    you're not isolating the test cases)
    """
    assert some_text == some_text


def test_example_pytest_raises():
    """
    - when assertions are not enough, pytest has pytest.raises
    - pytest.raises
      - can be used as a context manager w with
      - better for cases where you are testing exceptions your own code
      - For documenting unfixed bugs/deps bugs, use @pytest.mark.xfail
    """
    with pytest.raises(RuntimeError):

        def recurse_me():
            recurse_me()

        recurse_me()
