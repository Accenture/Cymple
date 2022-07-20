import pytest
from src.samples import basic


rendered = {
    # Read Operations #
    basic.get_all_nodes_by_label.__name__:
        basic.get_all_nodes_by_label(labels='Movie', node_name='n'),
    basic.get_all_nodes_by_label_and_properties.__name__:
        basic.get_all_nodes_by_label_and_properties(labels='Movie', properties={'name': 'The Matrix'}, node_name='n'),
    basic.get_all_paths.__name__:
        basic.get_all_paths(src_node_labels='Movie', dst_node_labels='Director', relationship_type='has_directed', path_name='path'),
    basic.get_all_nodes_related_to_nodes.__name__:
        basic.get_all_nodes_related_to_nodes(src_node_labels='Movie', dst_node_labels='Director', relationship_type='has_directed', dst_node_name='director'),
    basic.get_all_nodes_related_by_fixed_num_of_hops.__name__:
        basic.get_all_nodes_related_by_fixed_num_of_hops(src_node_labels='Movie', dst_node_labels='Director', num_hops=2, dst_node_name='director'),
    basic.get_all_nodes_related_by_varying_num_of_hops.__name__:
        basic.get_all_nodes_related_by_varying_num_of_hops(src_node_labels='Movie', dst_node_labels='Director', min_hops=1, max_hops=3, dst_node_name='director'),
    # Write Operations #
    basic.merge_node.__name__:
        basic.merge_node(node_labels='Movie', properties={'name': 'The Matrix Revolutions'}),
    basic.merge_relationship.__name__:
        basic.merge_relationship(relationship_type='has_sequel', src_node_labels='Movie', src_node_properties={'name': 'The Matrix'}, 
                                dst_node_labels='Movie', dst_node_properties={'name': 'The Matrix Revolutions'}),
}

expected = {
    basic.get_all_nodes_by_label.__name__: 
        'MATCH (n: Movie) RETURN n',
    basic.get_all_nodes_by_label_and_properties.__name__: 
        'MATCH (n: Movie {name : "The Matrix"}) RETURN n',
    basic.get_all_paths.__name__: 
        'MATCH path = ( (: Movie)-[: has_directed]-(: Director) ) RETURN path',
    basic.get_all_nodes_related_to_nodes.__name__: 
        'MATCH (: Movie)-[: has_directed]-(director: Director) RETURN director',
    basic.get_all_nodes_related_by_fixed_num_of_hops.__name__: 
        'MATCH (: Movie)-[*2]-(director: Director) RETURN director',
    basic.get_all_nodes_related_by_varying_num_of_hops.__name__: 
        'MATCH (: Movie)-[*1..3]-(director: Director) RETURN director',
    basic.merge_node.__name__: 
        'MERGE (: Movie {name : "The Matrix Revolutions"})',
    basic.merge_relationship.__name__: 
        'MATCH (src: Movie {name : "The Matrix"}) MATCH (dst: Movie {name : "The Matrix Revolutions"}) MERGE (src)-[: has_sequel]->(dst)',
}


@pytest.mark.parametrize('clause', expected)
def test_samples(clause: str):
    assert str(rendered[clause]) == expected[clause]
