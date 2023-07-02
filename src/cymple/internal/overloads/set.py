from typing import Union


def set(self, properties: Union[str, dict], escape_values: bool = True):
    if isinstance(properties, dict):
        _properties = Properties(properties).to_str("=", ", ", escape_values)
    else:
        _properties = str(properties)
    
    query = self.query + ' SET ' + _properties
    
    if isinstance(self, NodeAfterMergeAvailable) or isinstance(self, OnCreateAvailable) or isinstance(self, OnMatchAvailable) or isinstance(self, SetAfterMergeAvailable):
        return SetAfterMergeAvailable(query)

    return SetAvailable(query)
