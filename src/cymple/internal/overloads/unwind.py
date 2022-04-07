def unwind(self, variables: str):
    return UnwindAvailable(self.query + f' UNWIND {variables}')
