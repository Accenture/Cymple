from cymple import QueryBuilder

from ..data.onto_types.labels import Labels
from ..data.onto_types.properties import Properties
from ..data.onto_types.relations import Relations


def cypher_get_all_findings():
    output_mapping = [('n', 'n')]
    query = QueryBuilder().match().node(Labels.Finding, 'n').return_mapping(output_mapping).get()
    return query


def cypher_get_findings():
    output_mapping = [(f'f.{Properties.has_id}', 'id'),
                      (f't.{Properties.has_probability}', 'probability'),
                      (f't.{Properties.has_severity}', 'severity'),
                      (f'ct.{Properties.has_id}', 'cve')]

    query = (QueryBuilder().match()
             .node(Labels.Finding, 'f')
             .related_to(Relations.has_finding_type)
             .node(Labels.FindingType, 't')
             .related_to(Relations.has_cve)
             .node(Labels.CVEType, 'ct')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_services():
    output_mapping = [(f's.{Properties.has_id}', 'id'),
                      (f's.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(Labels.ServiceType, 's')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_identities():
    output_mapping = [(f'i.{Properties.has_id}', 'id'),
                      (f'i.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(Labels.Identity, 'i')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_business_applications():
    output_mapping = [(f'a.{Properties.has_id}', 'id'),
                      (f'a.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(Labels.Application, 'a')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_finding_detailed(finding_id):
    output_mapping = [(f'f.{Properties.has_id}', 'id'),
                      (f't.{Properties.has_probability}', 'probability'),
                      (f't.{Properties.has_severity}', 'severity'),
                      (f'ct.{Properties.has_id}', 'cve'),
                      (f't.{Properties.has_description}', 'description'),
                      (f't.{Properties.has_attack_scenario}', 'attack_scenario'),
                      (f't.recommendation', 'recommendations')]

    query = (QueryBuilder().match()
             .node(Labels.Finding, 'f', {Properties.has_id: finding_id})
             .related_to(Relations.has_finding_type)
             .node(Labels.FindingType, 't')
             .related_to(Relations.has_cve)
             .node(Labels.CVEType, 'ct')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_business_application(application_id):
    output_mapping = [(f'a.{Properties.has_id}', 'id'),
                      (f'a.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(Labels.Application, 'a', {Properties.has_id: application_id})
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_references_for_finding(finding_id):
    output_mapping = [(f'r.{Properties.has_description}', 'reference')]

    query = (QueryBuilder().match()
             .node(Labels.Finding, None, {Properties.has_id: finding_id})
             .related_to(Relations.has_reference)
             .node(Labels.ReferenceType, 'r')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_applications_for_finding(finding_id):
    output_mapping = [(f'a.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(Labels.Finding, None, {Properties.has_id: finding_id})
             .related_to(Relations.has_cloud_object)
             .node(Labels.Application, 'a')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_finding_type_details_per_id(id):
    output_mapping = [(f'collect(t.{Properties.has_severity})', 'severities'),
                      (f'collect(t.{Properties.has_probability})', 'probabilities')]

    query = (QueryBuilder().match()
             .node(Labels.FindingType, 't')
             .related_from(Relations.has_finding_type)
             .node(Labels.Finding)
             .related_to(Relations.has_cloud_object)
             .node(Labels.CloudObject)
             .related_to(Relations.has_service)
             .node(None, None, {Properties.has_id: id})
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_finding_details_for_application(application_id):
    output_mapping = [(f'f.{Properties.has_id}', 'id'),
                      (f't.{Properties.has_probability}', 'probability'),
                      (f't.{Properties.has_severity}', 'severity'),
                      (f'ct.{Properties.has_id}', 'cve')]

    query = (QueryBuilder().match()
             .node(Labels.Application, None, {Properties.has_id: application_id})
             .related_to(Relations.has_cloud_object)
             .node(Labels.CloudObject)
             .related_from(Relations.has_cloud_object)
             .node(Labels.Finding, 'f')
             .related_to(Relations.has_finding_type)
             .node(Labels.FindingType, 't')
             .related_to(Relations.has_cve)
             .node(Labels.CVEType, 'ct')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_get_service_details_for_application(application_id):
    output_mapping = [(f's.{Properties.has_id}', 'id'),
                      (f's.{Properties.has_name}', 'name')]

    query = (QueryBuilder().match()
             .node(Labels.Application, None, {Properties.has_id: application_id})
             .related_to(Relations.has_cloud_object)
             .node(Labels.CloudObject)
             .related_to(Relations.has_service)
             .node(Labels.ServiceType, 's')
             .return_mapping(output_mapping)
             .get())

    return query


def cypher_match_set_id(service_id):
    query = (QueryBuilder().match()
             .node(Labels.ServiceType, 's')
             .set({Properties.has_id: service_id})
             .return_literal('s')
             .get())

    return query


def cypher_merge_on_match(service_id):
    query = (QueryBuilder().merge()
             .node(Labels.ServiceType, 's')
             .on_match()
             .set({Properties.has_id: service_id})
             .return_literal('s')
             .get())

    return query


def cypher_relationship_properties(service_id):
    query = (QueryBuilder().match()
             .node(Labels.Application)
             .related_to(Relations.has_cloud_object)
             .node(Labels.CloudObject)
             .related_to(Relations.has_service, properties={Properties.has_id: service_id})
             .node(Labels.ServiceType, 's', {Properties.has_id: service_id})
             .return_literal('s')
             .get())

    return query


def test_cypher_get_all_findings():
    expected_query = f'MATCH (n: {Labels.Finding}) RETURN n as n'
    actual_query = cypher_get_all_findings()
    assert actual_query == expected_query


def test_cypher_get_findings():
    expected_query = (
        f'MATCH (f: {Labels.Finding})-[: {Relations.has_finding_type}]->'
        f'(t: {Labels.FindingType})-[: {Relations.has_cve}]->(ct: {Labels.CVEType}) '
        f'RETURN f.{Properties.has_id} as id, t.{Properties.has_probability} as probability, '
        f't.{Properties.has_severity} as severity, ct.{Properties.has_id} as cve')
    actual_query = cypher_get_findings()
    assert actual_query == expected_query


def test_cypher_get_services():
    expected_query = (f'MATCH (s: {Labels.ServiceType}) '
                      f'RETURN s.{Properties.has_id} as id, s.{Properties.has_name} as name')
    actual_query = cypher_get_services()
    assert actual_query == expected_query


def test_cypher_get_business_applications():
    expected_query = (f'MATCH (a: {Labels.Application}) '
                      f'RETURN a.{Properties.has_id} as id, a.{Properties.has_name} as name')
    actual_query = cypher_get_business_applications()
    assert actual_query == expected_query


def test_cypher_get_finding_detailed():
    finding_id = 'THAT_is_MOCK_id'

    expected_query = (
        f'MATCH (f: {Labels.Finding} {{{Properties.has_id} : "{finding_id}"}})-'
        f'[: {Relations.has_finding_type}]->(t: {Labels.FindingType})'
        f'-[: {Relations.has_cve}]->(ct: {Labels.CVEType}) '
        f'RETURN f.{Properties.has_id} as id, '
        f't.{Properties.has_probability} as probability, '
        f't.{Properties.has_severity} as severity, ct.{Properties.has_id} as cve, '
        f't.{Properties.has_description} as description, '
        f't.{Properties.has_attack_scenario} as attack_scenario, t.recommendation as recommendations')

    actual_query = cypher_get_finding_detailed(finding_id)
    assert actual_query == expected_query


def test_cypher_get_business_application():
    application_id = 'THAT_is_MOCK_id'
    expected_query = (f'MATCH (a: {Labels.Application} {{{Properties.has_id} : "{application_id}"}}) '
                      f'RETURN a.{Properties.has_id} as id, a.{Properties.has_name} as name')
    actual_query = cypher_get_business_application(application_id)
    assert actual_query == expected_query


def test_cypher_get_references_for_finding():
    finding_id = 'THAT_is_MOCK_id'

    expected_query = (f'MATCH (: {Labels.Finding} {{{Properties.has_id} : "{finding_id}"}})'
                      f'-[: {Relations.has_reference}]->(r: {Labels.ReferenceType}) '
                      f'RETURN r.{Properties.has_description} as reference')

    actual_query = cypher_get_references_for_finding(finding_id)
    assert actual_query == expected_query


def test_cypher_get_applications_for_finding():
    finding_id = 'THAT_is_MOCK_id'

    expected_query = (
        f'MATCH (: {Labels.Finding} {{{Properties.has_id} : "{finding_id}"}})'
        f'-[: {Relations.has_cloud_object}]->(a: {Labels.Application}) '
        f'RETURN a.{Properties.has_name} as name')

    actual_query = cypher_get_applications_for_finding(finding_id)
    assert actual_query == expected_query


def test_cypher_get_finding_type_details_for_service():
    service_id = 'THAT_is_MOCK_id'

    expected_query = (
        f'MATCH (t: {Labels.FindingType})<-[: {Relations.has_finding_type}]-'
        f'(: {Labels.Finding})-[: {Relations.has_cloud_object}]->'
        f'(: {Labels.CloudObject})-[: {Relations.has_service}]->( {{{Properties.has_id} : "{service_id}"}}) '
        f'RETURN collect(t.{Properties.has_severity}) as severities, '
        f'collect(t.{Properties.has_probability}) as probabilities')

    actual_query = cypher_get_finding_type_details_per_id(service_id)
    assert actual_query == expected_query


def test_cypher_match_set_id():
    service_id = 'THAT_is_MOCK_id'

    expected_query = f'MATCH (s: {Labels.ServiceType}) SET {Properties.has_id} = "{service_id}" RETURN s'

    actual_query = cypher_match_set_id(service_id)
    assert actual_query == expected_query


def test_cypher_merge_on_match():
    service_id = 'THAT_is_MOCK_id'

    expected_query = f'MERGE (s: {Labels.ServiceType}) ON MATCH SET {Properties.has_id} = "{service_id}" RETURN s'

    actual_query = cypher_merge_on_match(service_id)
    assert actual_query == expected_query


def test_cypher_relationship_properties():
    service_id = 'THAT_is_MOCK_id'

    expected_query = (
        f'MATCH (: {Labels.Application})-[: {Relations.has_cloud_object}]->'
        f'(: {Labels.CloudObject})-[: {Relations.has_service} {{{Properties.has_id} : "{service_id}"}}]->'
        f'(s: {Labels.ServiceType} {{{Properties.has_id} : "{service_id}"}}) RETURN s')

    actual_query = cypher_relationship_properties(service_id)
    assert actual_query == expected_query

def test_cypher_query_add():
    service_id = 'THAT_is_MOCK_id'

    expected_query = (
        f'MATCH (: {Labels.Application})-[: {Relations.has_cloud_object}]->'
        f'(: {Labels.CloudObject})-[: {Relations.has_service} {{{Properties.has_id} : "{service_id}"}}]->'
        f'(s: {Labels.ServiceType} {{{Properties.has_id} : "{service_id}"}}) WITH s MATCH (s) RETURN s')

    actual_query1 = (QueryBuilder().match()
                    .node(Labels.Application)
                    .related_to(Relations.has_cloud_object)
                    .node(Labels.CloudObject)
                    .related_to(Relations.has_service, properties={Properties.has_id: service_id})
                    .node(Labels.ServiceType, 's', {Properties.has_id: service_id})
                    .with_('s'))
    actual_query2 = (QueryBuilder().match()
                    .node(ref_name='s')
                    .return_literal('s'))

    actual_query = str(actual_query1 + actual_query2)
    assert actual_query == expected_query
    
    actual_query1 += actual_query2
    actual_query = str(actual_query1)
    assert actual_query == expected_query

def test_cypher_set_unescaped_after_merge():
    service_id = '1'

    expected_query = (
        f'MERGE (n: {Labels.Application} {{name : "test"}}) '
        f'ON CREATE SET n.{Properties.has_id} = "{service_id}" '
        f'ON MATCH SET n.{Properties.has_id} = n.has_id + "1" '
        f'RETURN n')

    actual_query = (QueryBuilder()
             .merge()
             .node(Labels.Application, 'n', {'name': 'test'})
             .on_create().set({f'n.{Properties.has_id}': service_id})
             .on_match().set({f'n.{Properties.has_id}': f'n.{Properties.has_id} + "1"'}, escape_values=False)
             .return_literal('n')
             .get())

    print(expected_query)

    assert actual_query == expected_query
