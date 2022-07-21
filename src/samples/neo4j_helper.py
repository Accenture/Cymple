from typing import Callable, Dict, List
from neo4j import Driver
import logging

logging.basicConfig(level=logging.INFO)


class Neo4jDbSession:
    """Context manager for a neo4j DB session."""

    def __init__(self, driver: Driver, db_name: str):
        self._db_name = db_name
        self._driver = driver

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self) -> None:
        """Close the driver ."""
        self._driver.close()

    def read_transaction(self, transaction_function: Callable, query: str, parameters: Dict = None) -> List[Dict]:
        """Perform a Read transaction on the database.

        Args:
            transaction_function (Callable): a function to be executed as a transaction on the DB
            query (str): The actual query to be run
            parameters (Dict, optional): Additional parameters to be used to run the query. Defaults to None.

        Returns:
            List[Dict]: A list of dictionary-represented objects as obtained by running the transaction
        """
        with self._driver.session(database=self._db_name) as session:
            return session.read_transaction(transaction_function, query=query, parameters=parameters)

    def write_transaction(self, transaction_function: Callable, query: str, parameters: Dict = None) -> List[Dict]:
        """Perform a Write transaction on the database .

        Args:
            transaction_function (Callable): a function to be executed as a transaction on the DB
            query (str): The actual query to be run
            parameters (Dict, optional): Additional parameters to be used to run the query. Defaults to None.

        Returns:
            List[Dict]: A list of dictionary-represented objects as obtained by running the transaction
        """
        with self._driver.session(database=self._db_name) as session:
            return session.write_transaction(transaction_function, query=query, parameters=parameters)


class Neo4jQueryHelper():
    """A helper class for running (Cypher) queries on a neo4j DB."""

    @staticmethod
    def run_query(t_x, query, parameters=None) -> List[Dict]:
        """Transaction function to run a query against the database.

        Returns:
            List[Dict]: A list of dictionary-represented objects as obtained by running the query
        """
        res = t_x.run(query, parameters=parameters)
        return res.data()

    def __init__(self, session: Neo4jDbSession) -> None:
        self.dbs = session

    def read(self, query: str, parameters: Dict = None) -> List[Dict]:
        """Run the given query against the database and returns the result as a Read operation.

        Args:
            query (str): a Cypher query to be run
            parameters (Dict, optional): Additional parameters to be used to run the query. Defaults to None.

        Returns:
            List[Dict]: A list of dictionary-represented objects as obtained by running the query
        """
        logging.info('In %s, executing query: %s', self.read.__name__, query)
        return self.dbs.read_transaction(self.run_query, query, parameters)

    def write(self, query: str, parameters: Dict = None) -> List[Dict]:
        """Run the given query against the database and returns the result as a Write operation.

        Args:
            query (str): a Cypher query to be run
            parameters (Dict, optional): Additional parameters to be used to run the query. Defaults to None.

        Returns:
            List[Dict]: A list of dictionary-represented objects as obtained by running the query
        """
        logging.info('In %s, executing query: %s', self.write.__name__, query)
        return self.dbs.write_transaction(self.run_query, query, parameters)
