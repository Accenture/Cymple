def yield_(self, mappings):
    if not isinstance(mappings, list):
        mappings = [mappings]
    query = ' YIELD ' + \
        ', '.join(f'{mapping.ref_name} as '
                  f'{mapping.returned_name if mapping.returned_name else mapping.ref_name.replace(".", "_")}'
                  for mapping in mappings)
    return YieldAvailable(self.query + query)
