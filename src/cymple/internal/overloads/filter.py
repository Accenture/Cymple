from typing import Any
from .typedefs import Properties


def where_multiple(self, filters: Properties, comparison_operator: str = '=', boolean_operator: str = ' AND '):
    filt = ' WHERE ' + Properties(filters).to_str(comparison_operator, boolean_operator)
    return WhereAvailable(self.query + filt)


def where(self, name: str, comparison_operator: str, value: Any):
    return self.where_multiple({name: value}, comparison_operator)
