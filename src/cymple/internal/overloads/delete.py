def detach_delete(self, ref_name: str):
    ret = f' DETACH DELETE {ref_name}'
    return DeleteAvailable(self.query + ret)


def delete(self, ref_name: str):
    ret = f' DELETE {ref_name}'
    return DeleteAvailable(self.query + ret)
