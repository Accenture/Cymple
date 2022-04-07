
def return_single(self, ref_name: str, returned_name: str = None):
    ret = ' RETURN ' + (f'{ref_name} as {returned_name}' if returned_name else ref_name)

    return Query(self.query + ret)


def return_multiple(self, mappings):
    if isinstance(mappings, Mapping):
        return self.return_single(mappings.ref_name, mappings.returned_name)

    ret = ' RETURN ' + \
        ', '.join(
            f'{mapping.ref_name} as {mapping.returned_name}' if mapping.returned_name else mapping.ref_name
            for mapping in mappings)

    return Query(self.query + ret)
