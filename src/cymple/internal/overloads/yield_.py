def yield_(self, mappings):
    if not isinstance(mappings, list):
        mappings = [mappings]
    
    query = ' YIELD ' + \
        ', '.join(f'{mapping[0]} AS '
                  f'{mapping[1] if mapping[1] else mapping[0].replace(".", "_")}'
                  for mapping in mappings)
    return YieldAvailable(self.query + query)
