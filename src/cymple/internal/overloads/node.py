from .typedefs import Properties


def node(self, labels=None, ref_name: str = None, properties: Properties = None):
    if not labels:
        labels_string = ''
    elif isinstance(labels, str):
        labels_string = f': {labels}'
    else:
        labels_string = f': {": ".join(labels).strip()}'

    if not properties:
        property_string = ''
    else:
        property_string = f' {{{str(Properties(properties))}}}'

    ref_name = ref_name or ''

    if not (self.query.endswith('-') or self.query.endswith('>') or self.query.endswith('<')):
        self.query += ' '

    if isinstance(self, MergeAvailable):
        return NodeAfterMergeAvailable(self.query + f'({ref_name}{labels_string}{property_string})')

    return NodeAvailable(self.query + f'({ref_name}{labels_string}{property_string})')
