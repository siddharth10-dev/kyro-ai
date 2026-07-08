from langchain_core.tools import tool

@tool
def get_deployment_info(service_name: str) -> dict:
    """Get recent deployment status and metadata for a service."""
    return {
        "status": "success",
        "deployed_at": "2026-07-08T18:00:00Z"
    }
