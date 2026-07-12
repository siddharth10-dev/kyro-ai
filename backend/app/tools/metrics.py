from app.tools.metrics_tool import get_metrics as get_metrics_tool

def get_metrics(service_name: str) -> dict:
    try:
        return get_metrics_tool.invoke({"service_name": service_name})
    except Exception:
        return {
            "latency": "unknown",
            "errors": "unknown"
        }
