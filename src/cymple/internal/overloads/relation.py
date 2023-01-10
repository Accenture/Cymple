


def related(self, label: str, ref_name: str = None, properties: dict = None):
    return RelationAvailable(self.query + self._directed_relation('none', label, ref_name, properties))


def related_to(self, label: str, ref_name: str = None, properties: str = {}):
    return RelationAvailable(self.query + self._directed_relation('forward', label, ref_name, properties))


def related_from(self, label: str, ref_name: str = None, properties: str = {}):
    return RelationAvailable(self.query + self._directed_relation('backward', label, ref_name, properties))


def related_variable_len(self, min_hops: int = -1, max_hops: int = -1):
    min_hops_str = '' if min_hops == -1 else str(min_hops)
    max_hops_str = '' if max_hops == -1 else str(max_hops)

    relation_length = '*' if min_hops == -1 and max_hops == -1 else (f'*{min_hops_str}'if min_hops == max_hops  else f'*{min_hops_str}..{max_hops_str}')

    if relation_length:
        realtion_str = f'[{relation_length}]'
    else:
        realtion_str = ''

    return RelationAvailable(self.query + f'-{realtion_str}-')


def _directed_relation(self, direction: str, label: str, ref_name: str = None, properties: str = {}):
    relation_type = '' if label is None else f': {label}'
    relation_ref_name = '' if ref_name is None else f'{ref_name}'
    relation_properties = f' {{{str(Properties(properties))}}}' if properties else ''

    if relation_ref_name or relation_type:
        realtion_str = f'[{relation_ref_name}{relation_type}{relation_properties}]'
    else:
        realtion_str = ''

    if direction == 'forward':
        return f'-{realtion_str}->'
    if direction == 'backward':
        return f'<-{realtion_str}-'

    return f'-{realtion_str}-'


__all__ = ['related', 'related_to', 'related_from', '_directed_relation']
