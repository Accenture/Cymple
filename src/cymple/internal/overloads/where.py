from typing import Any



def where_literal(self, statement: str, **kwargs):
    filt = ' WHERE ' + statement
    return WhereAvailable(self.query + filt)

def where_multiple(self, filters: dict, comparison_operator: str = '=', boolean_operator: str = ' AND ', **kwargs):
    filt = ' WHERE ' + Properties(filters).to_str(comparison_operator, boolean_operator, **kwargs)
    return WhereAvailable(self.query + filt)

def where(self, name: str, comparison_operator: str, value: Any, **kwargs):
    return self.where_multiple({name: value}, comparison_operator, **kwargs)
