"""This is the Cymple query builder module."""

# pylint: disable=R0901
# pylint: disable=R0903
# pylint: disable=W0102
from typing import List
from .typedefs import Mapping, Properties


class Query():
    """A general query-descripting class ."""

    def __init__(self, query):
        """Initialize the query object."""
        self.query = query

    def __str__(self) -> str:
        """Implement the str() operator for the query builder."""
        return self.query.strip()

    def __add__(self, other):
        """Implement the + operator for the query builder."""
        return Query(self.query.strip() + ' ' + other.query.strip())

    def __iadd__(self, other):
        """Implement the += operator for the query builder."""
        self.query = self.query.strip() + ' ' + other.query.strip()
        return self

    def get(self):
        """Get the final query string ."""
        return str(self)


class QueryStart(Query):
    """A class for representing a "QUERY START" clause."""


class Call(Query):
    """A class for representing a "CALL" clause."""

    def call(self):
        """Concatenate the "CALL" clause.

        :return: A Query object with a query that contains the new clause.
        :rtype: CallAvailable
        """
        return CallAvailable(self.query + ' CALL')


class CaseWhen(Query):
    """A class for representing a "CASE WHEN" clause."""

    def case_when(self, filters: Properties, on_true: str, on_false: str, ref_name: str, comparison_operator: str = "=", boolean_operator: str = "AND"):
        """Concatenate a CASE WHEN clause to the query, created from a list of given property filters.

        :param filters: A Properties object that represents the set of properties to be filtered
        :type filters: Properties
        :param on_true: The query to run when the predicate is true
        :type on_true: str
        :param on_false: The query to run when the predicate is false
        :type on_false: str
        :param ref_name: The name which is used to refer to the newly filtered object
        :type ref_name: str
        :param comparison_operator: A string operator, according to which the comparison between property values is
            done, e.g. for "=", we get: property.name = property.value, defaults to "="
        :type comparison_operator: str
        :param boolean_operator: The boolean operator to apply between predicates, defaults to "AND"
        :type boolean_operator: str

        :return: A Query object with a query that contains the new clause.
        :rtype: CaseWhenAvailable
        """
        filt = ' CASE WHEN ' + Properties(filters).to_str(comparison_operator, boolean_operator)
        filt += f' THEN {on_true} ELSE {on_false} END as {ref_name}'
        return CaseWhenAvailable(self.query + filt)


class Delete(Query):
    """A class for representing a "DELETE" clause."""

    def delete(self, ref_name: str):
        """Concatenate a DELETE clause for a referenced instance from the DB.

        :param ref_name: The reference name to be used for the delete operation
        :type ref_name: str

        :return: A Query object with a query that contains the new clause.
        :rtype: DeleteAvailable
        """
        ret = f' DELETE {ref_name}'
        return Query(self.query + ret)

    def detach_delete(self, ref_name: str):
        """Concatenate a DETACH DELETE clause for a referenced instance from the DB.

        :param ref_name: The reference name to be used for the delete operation
        :type ref_name: str

        :return: A Query object with a query that contains the new clause.
        :rtype: DeleteAvailable
        """
        ret = f' DETACH DELETE {ref_name}'
        return Query(self.query + ret)


class Where(Query):
    """A class for representing a "WHERE" clause."""

    def where(self, name: str, comparison_operator: str, value: str):
        """Concatenate a WHERE clause to the query, created as {name} {comparison_operator} {value}. E.g. x = 'abc'.

        :param name: The name of the object which is to be used in the comparison
        :type name: str
        :param comparison_operator: A string operator, according to which the comparison between compared object and
            the {value} is done, e.g. for "=", we get: {name} = {value}
        :type comparison_operator: str
        :param value: The value which is compared against
        :type value: str

        :return: A Query object with a query that contains the new clause.
        :rtype: WhereAvailable
        """
        return self.where_multiple({name: value}, comparison_operator)

    def where_multiple(self, filters: Properties, comparison_operator: str = "=", boolean_operator: str = ' AND '):
        """Concatenate a WHERE clause to the query, created from a list of given property filters.

        :param filters: A Properties object that represents the set of properties to be filtered
        :type filters: Properties
        :param comparison_operator: A string operator, according to which the comparison between property values is
            done, e.g. for "=", we get: property.name = property.value, defaults to "="
        :type comparison_operator: str
        :param boolean_operator: The boolean operator to apply between predicates, defaults to ' AND '
        :type boolean_operator: str

        :return: A Query object with a query that contains the new clause.
        :rtype: WhereAvailable
        """
        filt = ' WHERE ' + Properties(filters).to_str(comparison_operator, boolean_operator)
        return WhereAvailable(self.query + filt)


class Match(Query):
    """A class for representing a "MATCH" clause."""

    def match(self):
        """Concatenate the "MATCH" clause.

        :return: A Query object with a query that contains the new clause.
        :rtype: MatchAvailable
        """
        return MatchAvailable(self.query + ' MATCH')

    def match_optional(self):
        """Concatenate the "MATCH" clause.

        :return: A Query object with a query that contains the new clause.
        :rtype: MatchAvailable
        """
        return MatchAvailable(self.query + ' OPTIONAL MATCH ')


class Merge(Query):
    """A class for representing a "MERGE" clause."""

    def merge(self):
        """Concatenate the "MERGE" clause.

        :return: A Query object with a query that contains the new clause.
        :rtype: MergeAvailable
        """
        return MergeAvailable(self.query + ' MERGE')


class Node(Query):
    """A class for representing a "NODE" clause."""

    def node(self, labels: List[str] = None, ref_name: str = None, properties: Properties = None):
        """Concatenate a graph Node, which may be filtered using any label/s and/or property/properties.

        :param labels: The neo4j label (or list of labels) for that node, defaults to None
        :type labels: List[str]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A Properties object that represents the set of properties by which the nodes are filtered,
            defaults to None
        :type properties: Properties

        :return: A Query object with a query that contains the new clause.
        :rtype: NodeAvailable
        """
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


class NodeAfterMerge(Query):
    """A class for representing a "NODE AFTER MERGE" clause."""

    def node(self, labels: List[str] = None, ref_name: str = None, properties: Properties = None):
        """Concatenate a graph Node, which may be filtered using any label/s and/or property/properties.

        :param labels: The neo4j label (or list of labels) for that node, defaults to None
        :type labels: List[str]
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A Properties object that represents the set of properties by which the nodes are filtered,
            defaults to None
        :type properties: Properties

        :return: A Query object with a query that contains the new clause.
        :rtype: NodeAfterMergeAvailable
        """
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


class OnCreate(Query):
    """A class for representing a "ON CREATE" clause."""

    def on_create(self):
        """Concatenate the "ON CREATE" clause.

        :return: A Query object with a query that contains the new clause.
        :rtype: OnCreateAvailable
        """
        return OnCreateAvailable(self.query + ' ON CREATE')


class OnMatch(Query):
    """A class for representing a "ON MATCH" clause."""

    def on_match(self):
        """Concatenate the "ON MATCH" clause.

        :return: A Query object with a query that contains the new clause.
        :rtype: OnMatchAvailable
        """
        return OnMatchAvailable(self.query + ' ON MATCH')


class OperatorEnd(Query):
    """A class for representing a "OPERATOR END" clause."""

    def operator_end(self):
        """Concatenate the "OPERATOR END" clause.

        :return: A Query object with a query that contains the new clause.
        :rtype: OperatorEndAvailable
        """
        return OperatorEndAvailable(self.query + ' )')


class OperatorStart(Query):
    """A class for representing a "OPERATOR START" clause."""

    def operator_start(self, operator: str, ref_name: str = None, args: Properties = None):
        """Concatenate an operator (e.g. ShortestPath), where its result may be given a name for future reference.

        :param operator: The neo4j operator to be used (e.g. ShortestPath)
        :type operator: str
        :param ref_name: A reference name of the result, to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param args: A string of arguments, to be passed to the operator function, defaults to None
        :type args: Properties

        :return: A Query object with a query that contains the new clause.
        :rtype: OperatorStartAvailable
        """
        result_name = '' if ref_name is None else f'{ref_name} = '
        arguments = '' if args is None else f' {args}'

        return OperatorStartAvailable(self.query + f' {result_name}{operator}({arguments}')


class Relation(Query):
    """A class for representing a "RELATION" clause."""

    def related(self, label: str = None, ref_name: str = None, properties: Properties = None):
        """Concatenate an undirectional (i.e. --) graph Relationship, which may be filtered.

        :param label: The relationship label (type) in the DB, defaults to None
        :type label: str
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A Properties object that represents the set of properties by which the relationship is
            filtered, defaults to None
        :type properties: Properties

        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAvailable
        """
        return RelationAvailable(self.query + self._directed_relation('none', label, ref_name, properties))

    def related_to(self, label: str = None, ref_name: str = None, properties: Properties = {}):
        """Concatenate a forward (i.e. -->) graph Relationship, which may be filtered.

        :param label: The relationship label (type) in the DB, defaults to None
        :type label: str
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A Properties object that represents the set of properties by which the relationship is
            filtered, defaults to {}
        :type properties: Properties

        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAvailable
        """
        return RelationAvailable(self.query + self._directed_relation('forward', label, ref_name, properties))

    def related_from(self, label: str = None, ref_name: str = None, properties: Properties = {}):
        """Concatenate a backward (i.e. <--) graph Relationship, which may be filtered.

        :param label: The relationship label (type) in the DB, defaults to None
        :type label: str
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A Properties object that represents the set of properties by which the relationship is
            filtered, defaults to {}
        :type properties: Properties

        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAvailable
        """
        return RelationAvailable(self.query + self._directed_relation('backward', label, ref_name, properties))

    def related_variable_len(self, min_hops: int = -1, max_hops: int = -1):
        """Concatenate a uni-directional graph Relationship, with a variable path length.

        :param min_hops: The minimal desired number of hops (set -1 for maximum boundary only), defaults to -1
        :type min_hops: int
        :param max_hops: The maximal desired number of hops (set -1 for minimal boundary only), defaults to -1
        :type max_hops: int

        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAvailable
        """
        min_hops_str = '' if min_hops == -1 else str(min_hops)
        max_hops_str = '' if max_hops == -1 else str(max_hops)

        relation_length = '*' if min_hops == -1 and max_hops == - \
            1 else (f'*{min_hops_str}'if min_hops == max_hops else f'*{min_hops_str}..{max_hops_str}')

        if relation_length:
            realtion_str = f'[{relation_length}]'
        else:
            realtion_str = ''

        return RelationAvailable(self.query + f'-{realtion_str}-')

    def _directed_relation(self, direction: str, label: str, ref_name: str = None, properties: Properties = {}):
        """Concatenate a graph Relationship (private method).

        :param direction: The relationship direction, can one of 'forward', 'backward' - otherwise unidirectional
        :type direction: str
        :param label: The relationship label (type) in the DB
        :type label: str
        :param ref_name: A reference name to be used later in the rest of the query, defaults to None
        :type ref_name: str
        :param properties: A Properties object that represents the set of properties by which the relationship is
            filtered, defaults to {}
        :type properties: Properties

        :return: A Query object with a query that contains the new clause.
        :rtype: RelationAvailable
        """
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


class Return(Query):
    """A class for representing a "RETURN" clause."""

    def return_single(self, ref_name: str, returned_name: str = None):
        """Concatenate a return statement for a single object.

        :param ref_name: A reference name to be used to identify the name of the object as was defined earlier in the
            query
        :type ref_name: str
        :param returned_name: The returned name of the object. If none provided, the returned name is {ref_name},
            defaults to None
        :type returned_name: str

        :return: A Query object with a query that contains the new clause.
        :rtype: ReturnAvailable
        """
        ret = ' RETURN ' + (f'{ref_name} as {returned_name}' if returned_name else ref_name)

        return Query(self.query + ret)

    def return_multiple(self, mappings: List[Mapping]):
        """Concatenate a return statement for mutiple objects.

        :param mappings: The mapping (or a list of mappings) of db property names to code names, to be returned
        :type mappings: List[Mapping]

        :return: A Query object with a query that contains the new clause.
        :rtype: ReturnAvailable
        """
        if isinstance(mappings, Mapping):
            return self.return_single(mappings.ref_name, mappings.returned_name)

        ret = ' RETURN ' + \
            ', '.join(
                f'{mapping.ref_name} as {mapping.returned_name}' if mapping.returned_name else mapping.ref_name
                for mapping in mappings)

        return Query(self.query + ret)


class Set(Query):
    """A class for representing a "SET" clause."""

    def set(self, properties: Properties):
        """Concatenate a SET clause, using the given properties map.

        :param properties: The properties dictionary that will be used to set the properties with their corresponding
            values
        :type properties: Properties

        :return: A Query object with a query that contains the new clause.
        :rtype: SetAvailable
        """
        return SetAvailable(self.query + ' SET ' + Properties(properties).to_str("=", ", "))


class Unwind(Query):
    """A class for representing a "UNWIND" clause."""

    def unwind(self, variables: str):
        """Concatenate an UNWIND clause, keeping one or more variables given in 'variables' arg.

        :param variables: A string refering to previously obtained variables, comma seperated
        :type variables: str

        :return: A Query object with a query that contains the new clause.
        :rtype: UnwindAvailable
        """
        return UnwindAvailable(self.query + f' UNWIND {variables}')


class With(Query):
    """A class for representing a "WITH" clause."""

    def with_(self, variables: str):
        """Concatenate a WITH clause, keeping one or more variables given in 'variables' arg.

        :param variables: A string refering to previously obtained variables, comma seperated
        :type variables: str

        :return: A Query object with a query that contains the new clause.
        :rtype: WithAvailable
        """
        return WithAvailable(self.query + f' WITH {variables}')


class Yield(Query):
    """A class for representing a "YIELD" clause."""

    def yield_(self, mappings: List[Mapping]):
        """Concatenate a YIELD cluase, to yield a list of Mappings.

        :param mappings: The list of mappings of db properties names to code names, to be yielded
        :type mappings: List[Mapping]

        :return: A Query object with a query that contains the new clause.
        :rtype: YieldAvailable
        """
        if not isinstance(mappings, list):
            mappings = [mappings]
        query = ' YIELD ' + \
            ', '.join(f'{mapping.ref_name} as '
                      f'{mapping.returned_name if mapping.returned_name else mapping.ref_name.replace(".", "_")}'
                      for mapping in mappings)
        return YieldAvailable(self.query + query)


class QueryStartAvailable(Match, Merge, Call):
    """A class decorator declares a QueryStart is available in the current query."""


class CallAvailable(Node, Return, OperatorStart):
    """A class decorator declares a Call is available in the current query."""


class CaseWhenAvailable(QueryStartAvailable, With, Unwind, Where, CaseWhen, Return):
    """A class decorator declares a CaseWhen is available in the current query."""


class DeleteAvailable(Query):
    """A class decorator declares a Delete is available in the current query."""


class WhereAvailable(Return, Delete, With, Where, OperatorStart, QueryStartAvailable):
    """A class decorator declares a Where is available in the current query."""


class MatchAvailable(Node, Return, OperatorStart):
    """A class decorator declares a Match is available in the current query."""


class MergeAvailable(NodeAfterMerge, Return, OperatorStart):
    """A class decorator declares a Merge is available in the current query."""


class NodeAvailable(Relation, Return, Delete, With, Where, OperatorStart, OperatorEnd, Set, QueryStartAvailable):
    """A class decorator declares a Node is available in the current query."""


class NodeAfterMergeAvailable(Relation, Return, Delete, With, Where, OperatorStart, OperatorEnd, Set, OnCreate, OnMatch, QueryStartAvailable):
    """A class decorator declares a NodeAfterMerge is available in the current query."""


class OnCreateAvailable(Set, OperatorStart):
    """A class decorator declares a OnCreate is available in the current query."""


class OnMatchAvailable(Set, OperatorStart):
    """A class decorator declares a OnMatch is available in the current query."""


class OperatorEndAvailable(QueryStartAvailable, Yield, With, Return):
    """A class decorator declares a OperatorEnd is available in the current query."""


class OperatorStartAvailable(QueryStartAvailable, Node, With, OperatorEnd):
    """A class decorator declares a OperatorStart is available in the current query."""


class RelationAvailable(Node):
    """A class decorator declares a Relation is available in the current query."""


class ReturnAvailable(QueryStartAvailable, With, Unwind, Return):
    """A class decorator declares a Return is available in the current query."""


class SetAvailable(QueryStartAvailable, With, Unwind, Return):
    """A class decorator declares a Set is available in the current query."""


class UnwindAvailable(QueryStartAvailable, With, Unwind, Return):
    """A class decorator declares a Unwind is available in the current query."""


class WithAvailable(QueryStartAvailable, With, Unwind, Where, CaseWhen, Return):
    """A class decorator declares a With is available in the current query."""


class YieldAvailable(QueryStartAvailable, Node, With):
    """A class decorator declares a Yield is available in the current query."""


class QueryBuilder(QueryStartAvailable):
    """The Query Builder's initial interface."""

    def __init__(self) -> None:
        """Initialize a query builder."""
        super().__init__('')

    def reset(self):
        """Reset the query to an empty string."""
        self.query = ''
        return self
