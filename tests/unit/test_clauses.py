import pytest
from cymple import QueryBuilder as Qb
from cymple.typedefs import Mapping


expected = {
    '_RESET_': Qb().reset(),
    'CALL': Qb().call(),
    'CASE WHEN': Qb().match().node(ref_name='n').with_('n').case_when({'n.name': 'Bob'}, 'true', 'false', 'my_boolean'),
    'DELETE': Qb().match().node(ref_name='n').delete('n'),
    'DETACH DELETE': Qb().match().node(ref_name='n').detach_delete('n'),
    'WHERE (single)': Qb().match().node(ref_name='n').where('n.name', '=', 'value'),
    'WHERE (multiple)': Qb().match().node(ref_name='n').where_multiple({'n.name': 'value', 'n.age': 20}),
    'MATCH': Qb().match(),
    'MATCH OPTIONAL': Qb().match_optional(),
    'MERGE': Qb().merge(),
    'NODE': Qb().match().node(['label1', 'label2'], 'node', {'name': 'Bob'}),
    'NODE MERGE': Qb().merge().node(labels=['label1', 'label2'], ref_name='n', properties={'name': 'Bob'}).related_to().node(ref_name='m'),
    'OPERATOR': Qb().call().operator_start('SHORTESTPATH', 'p', '(:A)-[*]-(:B)').operator_end(),
    'RELATION (forawrd)': Qb().match().node().related_to().node(),
    'RELATION (backward)': Qb().match().node().related_from().node(),
    'RELATION (unidirectional)': Qb().match().node().related().node(),
    'RELATION (variable length)': Qb().match().node().related_variable_len('*1..2').node(),
    'RELATION (variable length, empty)': Qb().match().node().related_variable_len('').node(),
    'RETURN (single)': Qb().match().node(ref_name='n').return_single('n'),
    'RETURN (multiple)': Qb().match().node(ref_name='n').return_multiple(Mapping('n.name', 'name')),
    'RETURN (multiple, list)': Qb().match().node(ref_name='n').return_multiple([Mapping('n.name', 'name'), Mapping('n.age', 'age')]),
    'SET': Qb().merge().node(ref_name='n').set({'n.name': 'Alice'}),
    'ON CREATE': Qb().merge().node(ref_name='n').on_create().set({'n.name': 'Bob'}),
    'ON MATCH': Qb().merge().node(ref_name='n').on_match().set({'n.name': 'Bob'}),
    'UNWIND': Qb().match().node(ref_name='n').with_('n').unwind('n'),
    'WITH': Qb().match().node(ref_name='a').with_('a,b'),
    'YIELD': Qb().call().operator_start('SHORTESTPATH', 'p', '(:A)-[*]-(:B)').operator_end().yield_(Mapping('length(p)', 'len')),
    'YIELD (list)': Qb().call().operator_start('SHORTESTPATH', 'p', '(:A)-[*]-(:B)').operator_end().yield_([Mapping('length(p)', 'len'), Mapping('relationships(p)', 'rels')]),
}

actual = {
    '_RESET_': '',
    'CALL': 'CALL',
    'CASE WHEN': 'MATCH (n) WITH n CASE WHEN n.name = "Bob" THEN true ELSE false END as my_boolean',
    'DELETE': 'MATCH (n) DELETE n',
    'DETACH DELETE': 'MATCH (n) DETACH DELETE n',
    'WHERE (single)': 'MATCH (n) WHERE n.name = "value"',
    'WHERE (multiple)': 'MATCH (n) WHERE n.name = "value" AND n.age = 20',
    'MATCH': 'MATCH',
    'MATCH OPTIONAL': 'OPTIONAL MATCH',
    'MERGE': 'MERGE',
    'NODE': 'MATCH (node: label1: label2 {name : "Bob"})',
    'NODE MERGE': 'MERGE (n: label1: label2 {name : "Bob"})-->(m)',
    'OPERATOR': 'CALL p = SHORTESTPATH((:A)-[*]-(:B))',
    'RELATION (forawrd)': 'MATCH ()-->()',
    'RELATION (backward)': 'MATCH ()<--()',
    'RELATION (unidirectional)': 'MATCH ()--()',
    'RELATION (variable length)': 'MATCH ()-[*1..2]-()',
    'RELATION (variable length, empty)': 'MATCH ()--()',
    'RETURN (single)': 'MATCH (n) RETURN n',
    'RETURN (multiple)': 'MATCH (n) RETURN n.name as name',
    'RETURN (multiple, list)': 'MATCH (n) RETURN n.name as name, n.age as age',
    'SET': 'MERGE (n) SET n.name = "Alice"',
    'ON CREATE': 'MERGE (n) ON CREATE SET n.name = "Bob"',
    'ON MATCH': 'MERGE (n) ON MATCH SET n.name = "Bob"',
    'UNWIND': 'MATCH (n) WITH n UNWIND n',
    'WITH': 'MATCH (a) WITH a,b',
    'YIELD': 'CALL p = SHORTESTPATH((:A)-[*]-(:B)) YIELD length(p) as len',
    'YIELD (list)': 'CALL p = SHORTESTPATH((:A)-[*]-(:B)) YIELD length(p) as len, relationships(p) as rels',
}


@pytest.mark.parametrize('clause', actual)
def test_case(clause):
    assert str(expected[clause]) == actual[clause]
