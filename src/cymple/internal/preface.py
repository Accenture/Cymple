
class Query():
    """A general query-descripting class ."""

    def __init__(self, query):
        """Initialize the query object."""
        self.query = query

    def __str__(self) -> str:
        """Implement the str() operator for the query builder."""
        return self.query.strip()

    def __add__(self, other):
        """Implement the + operator for the query builder."""
        return Query(self.query.strip() + ' ' + other.query.strip())

    def __iadd__(self, other):
        """Implement the += operator for the query builder."""
        self.query = self.query.strip() + ' ' + other.query.strip()
        return self

    def get(self):
        """Get the final query string ."""
        return str(self)
