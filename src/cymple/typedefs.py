"""Cymple's API type definitions."""
from typing import NamedTuple, Any


class Mapping(NamedTuple):
    """Mapping between property name in neo4j db and the name used in code."""

    ref_name: str
    returned_name: str = None


class Properties(dict):
    """A dict class storing a set of properties."""

    @staticmethod
    def _escape(string: str) -> str:
        res = string.replace('"', '\\"').replace("'", "\\'")
        return res

    @staticmethod
    def _format_value(value: Any) -> Any:
        # Assigning a dict to a property is not supported by a neo4j graph
        # if isinstance(value, dict):
        #     return str({sub_key: self._format_value(sub_value) for sub_key, sub_value in value.items()})
        if isinstance(value, str):
            return f'"{Properties._escape(value)}"'
        if value is None:
            return 'null'
        
        return value

    def to_str(self, comparison_operator: str = ':', boolean_operator: str = ', ') -> str:
        """Convert this Properties dicionarty to a serialied string suitable for a cypher query"""
        pairs = [f'{key} {comparison_operator} {Properties._format_value(value)}' for key, value in self.items()]
        res = boolean_operator.join(pairs)
        return res

    def __str__(self) -> str:
        return self.to_str()
