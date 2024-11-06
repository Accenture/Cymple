import pytest
from cymple import QueryBuilder

qb = QueryBuilder()

rendered = {
    'CASE_1': qb.reset().match().node(ref_name='p', labels='Person').return_mapping([('p.name', 'name'), ('CASE p.age WHEN 18 THEN "Young Adult" WHEN 65 THEN "Senior" ELSE "Adult" END', 'ageCategory')]),
    'CASE_2': qb.reset().match().node(ref_name='p', labels='Person').return_mapping([('p.name', 'name'), ('CASE WHEN p.age < 18 THEN "Minor" WHEN p.age >= 18 AND p.age < 65 THEN "Adult" ELSE "Senior" END', 'ageGroup')]),
    'CASE_3': qb.reset().match().node(ref_name='p', labels='Person').set({'p.category': 'CASE WHEN p.age < 18 THEN "Minor" WHEN p.age >= 18 AND p.age < 65 THEN "Adult" ELSE "Senior" END'}, escape_values=False).return_literal('p'),
    'CASE_4': qb.reset().match().node(ref_name='p', labels='Person').with_('p,').case(when_then_mapping={"\"America\"": "\"US\"", "\"North America\"": "\"Canada\""}, default_result="\"Other\"", results_ref='region', test_expression='p.country').return_literal('p.name, region'),
    'CASE_5': qb.reset().match().node(ref_name='p', labels='Person').return_mapping([('p.name', 'name'), ('CASE WHEN p.age < 18 THEN CASE p.age WHEN 0 THEN "Newborn" ELSE "Child" END WHEN p.age < 65 THEN "Adult" ELSE "Senior" END', 'lifeStage')]),
    'CASE_6': qb.reset().match().node(ref_name='p', labels='Person').return_mapping([('COUNT(CASE WHEN p.age < 18 THEN 1 END)', 'minors'), ('COUNT(CASE WHEN p.age >= 18 AND p.age < 65 THEN 1 END)', 'adults'), ('COUNT(CASE WHEN p.age >= 65 THEN 1 END)', 'seniors')]),
    'CASE_7': qb.reset().match().node(ref_name='p', labels='Person').where_literal('CASE WHEN p.age < 18 THEN false ELSE true END').return_literal('p'),
    'CASE_8': qb.reset().match().node(ref_name='p', labels='Person').return_mapping([('p.name', 'name'), ('p.age', 'age')]).order_by('CASE WHEN p.age < 18 THEN 1 WHEN p.age >= 18 AND p.age < 65 THEN 2 ELSE 3 END'),
    'CASE_9': qb.reset().match().node(ref_name='p', labels='Person').return_mapping([('p.name', 'name'), ('p.age', 'age'), ('CASE WHEN p.age < 18 THEN "Young " + p.name WHEN p.age >= 65 THEN "Senior " + p.name ELSE "Adult " + p.name END', 'titledName')])
}

expected = {
    'CASE_1': 'MATCH (p: Person) RETURN p.name AS name, CASE p.age WHEN 18 THEN "Young Adult" WHEN 65 THEN "Senior" ELSE "Adult" END AS ageCategory',
    'CASE_2': 'MATCH (p: Person) RETURN p.name AS name, CASE WHEN p.age < 18 THEN "Minor" WHEN p.age >= 18 AND p.age < 65 THEN "Adult" ELSE "Senior" END AS ageGroup',
    'CASE_3': 'MATCH (p: Person) SET p.category = CASE WHEN p.age < 18 THEN "Minor" WHEN p.age >= 18 AND p.age < 65 THEN "Adult" ELSE "Senior" END RETURN p',
    'CASE_4': 'MATCH (p: Person) WITH p, CASE p.country WHEN "US" THEN "America" WHEN "Canada" THEN "North America" ELSE "Other" END AS region RETURN p.name, region',
    'CASE_5': 'MATCH (p: Person) RETURN p.name AS name, CASE WHEN p.age < 18 THEN CASE p.age WHEN 0 THEN "Newborn" ELSE "Child" END WHEN p.age < 65 THEN "Adult" ELSE "Senior" END AS lifeStage',
    'CASE_6': 'MATCH (p: Person) RETURN COUNT(CASE WHEN p.age < 18 THEN 1 END) AS minors, COUNT(CASE WHEN p.age >= 18 AND p.age < 65 THEN 1 END) AS adults, COUNT(CASE WHEN p.age >= 65 THEN 1 END) AS seniors',
    'CASE_7': 'MATCH (p: Person) WHERE CASE WHEN p.age < 18 THEN false ELSE true END RETURN p',
    'CASE_8': 'MATCH (p: Person) RETURN p.name AS name, p.age AS age ORDER BY CASE WHEN p.age < 18 THEN 1 WHEN p.age >= 18 AND p.age < 65 THEN 2 ELSE 3 END ASC',
    'CASE_9': 'MATCH (p: Person) RETURN p.name AS name, p.age AS age, CASE WHEN p.age < 18 THEN "Young " + p.name WHEN p.age >= 65 THEN "Senior " + p.name ELSE "Adult " + p.name END AS titledName'
}


@pytest.mark.parametrize('clause', expected)
def test_samples(clause: str):
    assert str(rendered[clause]) == expected[clause]
