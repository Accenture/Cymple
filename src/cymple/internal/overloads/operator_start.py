def operator_start(self, operator: str, ref_name: str = None, args: str = None):
    result_name = '' if ref_name is None else f'{ref_name} = '
    arguments = '' if args is None else f' {args}'

    return OperatorStartAvailable(self.query + f' {result_name}{operator}({arguments}')
