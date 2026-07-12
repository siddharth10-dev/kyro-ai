from app.tools.logs_tool import get_logs as get_logs_tool

def get_logs(service_name: str) -> list[str]:
    try:
        return get_logs_tool.invoke({"service_name": service_name})
    except Exception as e:
        return [f"Error getting logs: {str(e)}"]
