import os
from typing import Union


environ_bak = dict(os.environ)


def pytest_sessionstart(session: 'Session') -> None:
    """Called after the ``Session`` object has been created and before performing collection
    and entering the run test loop.

    :param pytest.Session session: The pytest session object.
    """


def pytest_sessionfinish(
    session: 'Session', exitstatus: Union[int, 'ExitCode']
) -> None:
    """Called after whole test run finished, right before returning the exit status to the system.

    :param pytest.Session session: The pytest session object.
    :param int exitstatus: The status which pytest will return to the system.
    """
