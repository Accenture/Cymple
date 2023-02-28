def call(self, procedure: str):
    ret = f" CALL {procedure}"
    return CallAvailable(self.query + ret)
