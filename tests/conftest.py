import os
from dotenv import dotenv_values
from pathlib import Path
from typing import Union


environ_bak = dict(os.environ)


def set_test_environ():
    env_file_path = Path(__file__).parent.parent / 'config' / 'test.env'
    test_env = dotenv_values(env_file_path)
    os.environ.update(test_env)


def restore_environ():
    os.environ.clear()
    os.environ.update(environ_bak)


def pytest_sessionstart(session: 'Session') -> None:
    """Called after the ``Session`` object has been created and before performing collection
    and entering the run test loop.

    :param pytest.Session session: The pytest session object.
    """
    set_test_environ()


def pytest_sessionfinish(
    session: 'Session', exitstatus: Union[int, 'ExitCode']
) -> None:
    """Called after whole test run finished, right before returning the exit status to the system.

    :param pytest.Session session: The pytest session object.
    :param int exitstatus: The status which pytest will return to the system.
    """
    restore_environ()
