from dataclasses import dataclass


@dataclass
class Relations:
    has_cloud_object: str = "has_cloud_object"
    has_service: str = "has_service"
    has_finding_type: str = "has_finding_type"
    has_diagnosed_cloud_object: str = "has_diagnosed_cloud_object"
    has_finding: str = "has_finding"
    has_cve: str = "has_cve"
    has_reference: str = "has_reference"
