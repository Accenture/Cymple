
from typing import Any, Dict, List
from cymple.builder import QueryBuilder

def get_all_nodes_by_label(labels: List[str], node_name: str = 'n'):
    return (QueryBuilder()
            .match()
            .node(labels=labels, ref_name=node_name)
            .return_single(ref_name=node_name)
            )

def get_all_nodes_by_label_and_property(labels: List[str], properties: Dict[str, Any], node_name: str = 'n'):
    return (QueryBuilder()
            .match()
            .node(labels=labels, ref_name=node_name, properties=properties)
            .return_single(ref_name=node_name)
            )

def get_all_paths(src_node_labels: List[str], dst_node_labels: List[str], relationship_type: str, path_name: str = 'p'):
    return (QueryBuilder()
            .match()
            .operator_start(operator='', ref_name=path_name)
            .node(labels=src_node_labels)
            .related(label=relationship_type)
            .node(labels=dst_node_labels)
            .operator_end()
            .return_single(ref_name=path_name)
            )

def get_all_nodes_related_to_nodes(src_node_labels: List[str], dst_node_labels: List[str], relationship_type: str, dst_node_name: str = 'd'):
    return (QueryBuilder()
            .match()
            .node(labels=src_node_labels)
            .related(label=relationship_type)
            .node(labels=dst_node_labels, ref_name = dst_node_name)
            .return_single(ref_name=dst_node_name)
            )
