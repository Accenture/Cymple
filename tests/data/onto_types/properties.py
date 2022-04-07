from dataclasses import dataclass


@dataclass
class Properties:
    has_id: str = "has_id"
    has_name: str = "has_name"
    has_probability: str = "has_probability"
    has_severity: str = "has_severity"
    has_description: str = "has_description"
    has_attack_scenario: str = "has_attack_scenario"
