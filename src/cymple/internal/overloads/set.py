

def set(self, properties: dict, escape_values: bool = True):
    query = self.query + ' SET ' + Properties(properties).to_str("=", ", ", escape_values)
    
    if isinstance(self, NodeAfterMergeAvailable) or isinstance(self, OnCreateAvailable) or isinstance(self, OnMatchAvailable) or isinstance(self, SetAfterMergeAvailable):
        return SetAfterMergeAvailable(query)

    return SetAvailable(query)
