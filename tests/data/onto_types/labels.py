from dataclasses import dataclass


@dataclass
class Labels:
    Application: str = "Application"
    CVEType: str = "CVEType"
    CloudObject: str = "CloudObject"
    Finding: str = "Finding"
    FindingScan: str = "FindingScan"
    FindingSourceType: str = "FindingSourceType"
    FindingType: str = "FindingType"
    ReferenceType: str = "ReferenceType"
    ServiceType: str = "ServiceType"
