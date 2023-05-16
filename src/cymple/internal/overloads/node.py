


def node(self, labels=None, ref_name: str = None, properties: dict = None, **kwargs):
    if not labels:
        labels_string = ''
    elif isinstance(labels, str):
        labels_string = f': {labels}'
    else:
        labels_string = f': {": ".join(labels).strip()}'

    if not properties:
        property_string = ''
    else:
        property_string = f' {{{Properties(properties).to_str(**kwargs)}}}'

    ref_name = ref_name or ''

    query = self.query
    if not (query.endswith('-') or query.endswith('>') or query.endswith('<')):
        query += ' '

    query += f'({ref_name}{labels_string}{property_string})'
    
    if isinstance(self, MergeAvailable):
        return NodeAfterMergeAvailable(query)

    return NodeAvailable(query)
