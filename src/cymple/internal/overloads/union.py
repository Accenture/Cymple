def union(self):
    return UnionAvailable(self.query + f' UNION')


def union_all(self):
    return UnionAvailable(self.query + f' UNION ALL')