
def return_literal(self, literal: str):
    ret = f' RETURN {literal}'

    return Query(self.query + ret)


def return_mapping(self, mappings):
    if not isinstance(mappings, list):
        mappings = [mappings]

    ret = ' RETURN ' + \
        ', '.join(
            f'{mapping[0]} as {mapping[1]}' if mapping[1] else mapping[0].replace(".", "_")
            for mapping in mappings)

    return Query(self.query + ret)
