from langchain_core.tools import tool

@tool
def get_metrics(service_name: str) -> dict:
    """Get metrics like latency and error rate for a service."""
    service = service_name.lower()
    if "payment" in service:
        return {
            "latency": "3200ms",
            "errors": "15%"
        }
    return {
        "latency": "80ms",
        "errors": "0.1%"
    }
