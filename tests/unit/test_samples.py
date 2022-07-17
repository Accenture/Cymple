import pytest
from src.samples import basic


rendered = {
    basic.get_all_nodes_by_label.__name__:
        basic.get_all_nodes_by_label(labels='Movie', node_name='n'),
    basic.get_all_nodes_by_label_and_property.__name__:
        basic.get_all_nodes_by_label_and_property(labels='Movie', properties={'name': 'The Matrix'}, node_name='n'),
    basic.get_all_paths.__name__:
        basic.get_all_paths(src_node_labels='Movie', dst_node_labels='Director', relationship_type='has_directed', path_name='path'),
    basic.get_all_nodes_related_to_nodes.__name__:
        basic.get_all_nodes_related_to_nodes(src_node_labels='Movie', dst_node_labels='Director', relationship_type='has_directed', dst_node_name='director')
}

expected = {
    basic.get_all_nodes_by_label.__name__: 
        'MATCH (n: Movie) RETURN n',
    basic.get_all_nodes_by_label_and_property.__name__: 
        'MATCH (n: Movie {name : "The Matrix"}) RETURN n',
    basic.get_all_paths.__name__: 
        'MATCH path = ( (: Movie)-[: has_directed]-(: Director) ) RETURN path',
    basic.get_all_nodes_related_to_nodes.__name__: 
        'MATCH (: Movie)-[: has_directed]-(director: Director) RETURN director'
}


@pytest.mark.parametrize('clause', expected)
def test_samples(clause: str):
    assert str(rendered[clause]) == expected[clause]
