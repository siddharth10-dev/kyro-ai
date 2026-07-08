from langchain_core.tools import tool

@tool
def get_logs(service_name: str) -> list[str]:
    """Get recent logs for a service to debug issues."""
    service = service_name.lower()
    if "payment" in service:
        return ["Payment gateway timeout"]
    elif "auth" in service:
        return ["ERROR: Invalid token validation", "Authentication failures increased"]
    return ["No logs found"]
