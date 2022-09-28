from cymple import QueryBuilder
from samples.neo4j_helper import Neo4jDbSession, Neo4jQueryHelper
from samples.neo4j_config import uri as neo4j_uri, db_name as neo4j_db

helper: Neo4jQueryHelper
builder: QueryBuilder

label = 'Movie'
property = 'name'
reference = 'node'


def init(neo4j_user, neo4j_password):
    """Init this module by creating a session to the (neo4j) DB, creating a helper for running queries and a query builder"""
    from neo4j import GraphDatabase

    global helper
    global builder

    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
    session = Neo4jDbSession(driver=driver, db_name=neo4j_db)
    helper = Neo4jQueryHelper(session)
    builder = QueryBuilder()


def read_movie_node(movie_name: str):
    """Create a query for reading a node labeled 'Movie', with name given in movie_name"""
    builder.reset()
    query = str(builder
                .match()
                .node(labels=label, ref_name=reference, properties={property: movie_name})
                .return_mapping((f'{reference}.{property}', property)))
    results = helper.read(query)
    return results[0].get(property) if results else None


def write_movie_node(movie_name: str):
    """Create a query for creating a node labeled 'Movie', with name given in movie_name"""
    builder.reset()
    query = str(builder
                .merge()
                .node(labels=label, ref_name=reference, properties={property: movie_name})
                .return_mapping((f'{reference}.{property}', property)))
    results = helper.write(query)
    return results[0].get(property) if results else None
