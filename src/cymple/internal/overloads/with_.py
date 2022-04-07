def with_(self, variables: str):
    return WithAvailable(self.query + f' WITH {variables}')
