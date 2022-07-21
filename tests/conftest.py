from pytest import fixture


def pytest_addoption(parser):
    try:
        parser.addoption('--e2e', action='store_true', default=False)
        parser.addoption('--neo4j_user', action='store', default=None)
        parser.addoption('--neo4j_password', action='store', default=None)
    except Exception as ex:
        print(ex)
    
@fixture(scope='session')
def is_run_e2e(pytestconfig) -> bool:
    return pytestconfig.getoption('e2e')
    
@fixture(scope='session')
def neo4j_user(pytestconfig) -> bool:
    return pytestconfig.getoption('neo4j_user')
    
@fixture(scope='session')
def neo4j_password(pytestconfig) -> bool:
    return pytestconfig.getoption('neo4j_password')
