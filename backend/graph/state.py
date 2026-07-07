from typing import TypedDict, Dict, Any

class IncidentState(TypedDict):
    incident: Any
    classification: Dict[str, Any]
    investigation: Dict[str, Any]
    root_cause: Dict[str, Any]
    runbook: Dict[str, Any]
    recommendation: Dict[str, Any]
