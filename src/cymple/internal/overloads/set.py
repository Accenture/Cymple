

def set(self, properties: dict):
    query = self.query + ' SET ' + Properties(properties).to_str("=", ", ")
    
    if isinstance(self, NodeAfterMergeAvailable) or isinstance(self, OnCreateAvailable) or isinstance(self, OnMatchAvailable) or isinstance(self, SetAfterMergeAvailable):
        return SetAfterMergeAvailable(query)

    return SetAvailable(query)
