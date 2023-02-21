"""Cymple's API type definitions."""
from collections import namedtuple
from typing import Any, List
from dataclasses import dataclass

Mapping = namedtuple('Mapping', ['ref_name', 'returned_name'], defaults=(None, None))


class Properties(dict):
    """A dict class storing a set of properties."""

    @staticmethod
    def _escape(string: str) -> str:
        res = string.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace('\r', '\\r').replace('\n', '\\n')
        return res

    @staticmethod
    def _format_value(value: Any, escape: bool) -> Any:
        # Assigning a dict to a property is not supported by a neo4j graph
        # if isinstance(value, dict):
        #     return str({sub_key: self._format_value(sub_value) for sub_key, sub_value in value.items()})
        if escape and isinstance(value, str):
            return f'"{Properties._escape(value)}"'
        if value is None:
            return 'null'
        
        return value

    def to_str(self, comparison_operator: str = ':', boolean_operator: str = ', ', escape: bool = True) -> str:
        """Convert this Properties dicionarty to a serialied string suitable for a cypher query"""
        pairs = [f'{key} {comparison_operator} {Properties._format_value(value, escape)}' for key, value in self.items()]
        res = boolean_operator.join(pairs)
        return res

    def __str__(self) -> str:
        return self.to_str()
