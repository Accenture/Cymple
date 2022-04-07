class QueryBuilder(QueryStartAvailable):
    """The Query Builder's initial interface."""

    def __init__(self) -> None:
        """Initialize a query builder."""
        super().__init__('')

    def reset(self):
        """Reset the query to an empty string."""
        self.query = ''
        return self
