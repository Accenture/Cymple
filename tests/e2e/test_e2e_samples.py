import pytest
from samples import neo4j_e2e


def test_neo4j_sample(is_run_e2e, neo4j_user, neo4j_password):
    if not is_run_e2e:
        pytest.skip('Use "pytest --e2e --neo4j_user <username> --neo4j_password <password>" to run this!')

    movie_name = 'The Matrix'

    neo4j_e2e.init(neo4j_user=neo4j_user, neo4j_password=neo4j_password)
    assert neo4j_e2e.write_movie_node(movie_name) == movie_name
    assert neo4j_e2e.read_movie_node(movie_name) == movie_name
