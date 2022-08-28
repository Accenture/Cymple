
from typing import Any, Dict, List
from cymple.builder import QueryBuilder



def get_all_nodes_by_label(labels: List[str], node_name: str = 'n'):
    return (QueryBuilder()
            .match()
            .node(labels=labels, ref_name=node_name)
            .return_single(ref_name=node_name)
            )


def get_all_nodes_by_label_and_properties(labels: List[str], properties: Dict[str, Any], node_name: str = 'n'):
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
            .node(labels=dst_node_labels, ref_name=dst_node_name)
            .return_single(ref_name=dst_node_name)
            )


def get_all_nodes_related_by_fixed_num_of_hops(src_node_labels: List[str], dst_node_labels: List[str], num_hops: int, dst_node_name: str = 'd'):
    return (QueryBuilder()
            .match()
            .node(labels=src_node_labels)
            .related_variable_len(min_hops=num_hops, max_hops=num_hops)
            .node(labels=dst_node_labels, ref_name=dst_node_name)
            .return_single(ref_name=dst_node_name)
            )


def get_all_nodes_related_by_varying_num_of_hops(src_node_labels: List[str], dst_node_labels: List[str], min_hops: int, max_hops: int, dst_node_name: str = 'd'):
    return (QueryBuilder()
            .match()
            .node(labels=src_node_labels)
            .related_variable_len(min_hops=min_hops, max_hops=max_hops)
            .node(labels=dst_node_labels, ref_name=dst_node_name)
            .return_single(ref_name=dst_node_name)
            )


def get_nodes_with_pagination(node_labels: List[str], node_name: str = 'n', offset: int = 0, limit: int = -1):
    raise NotImplementedError()


def create_node(node_labels: List[str]):
    raise NotImplementedError()


def merge_node(node_labels: List[str], properties: Dict[str, Any] = None):
    return (QueryBuilder()
            .merge()
            .node(labels=node_labels, properties=properties)
            )


def create_relationship(relationship_type: str):
    raise NotImplementedError()


def merge_relationship(relationship_type: str, properties: Dict[str, Any] = None, src_node_labels: List[str] = None, 
                        dst_node_labels: List[str] = None, src_node_properties: Dict[str, Any] = None, dst_node_properties: Dict[str, Any] = None):
    return (QueryBuilder()
            .match()
            .node(labels=src_node_labels, properties=src_node_properties, ref_name='src')
            .match()
            .node(labels=dst_node_labels, properties=dst_node_properties, ref_name='dst')
            .merge()
            .node(ref_name='src')
            .related_to(label=relationship_type, properties=properties)
            .node(ref_name='dst')
            )
