import os
import requests
from langchain_core.tools import tool

LOKI_URL = os.getenv("LOKI_URL", "http://localhost:3100")

@tool
def get_logs(service_name: str) -> list[str]:
    """Get recent logs for a service to debug issues from Loki."""
    service = service_name.lower()
    
    # Map service name to Loki job label
    job_label = "checkout-service" if "checkout" in service or "payment" in service else service
    
    try:
        url = LOKI_URL
        # Try checking Loki readiness
        try:
            requests.get(f"{url}/ready", timeout=1)
        except Exception:
            url = "http://loki:3100" if "localhost" in LOKI_URL else "http://localhost:3100"
            
        # Query Loki
        query = f'{{job="{job_label}"}}'
        params = {
            "query": query,
            "limit": 50,
            "direction": "BACKWARD"
        }
        res = requests.get(f"{url}/loki/api/v1/query_range", params=params, timeout=2).json()
        
        logs_list = []
        if res.get("status") == "success":
            results = res.get("data", {}).get("result", [])
            for stream in results:
                for val in stream.get("values", []):
                    # Each val is [timestamp_ns, log_line]
                    logs_list.append(val[1])
                    
        if logs_list:
            # Reverse to get chronological order (since we queried BACKWARD)
            logs_list.reverse()
            return logs_list
    except Exception:
        pass
        
    # --- Fallback: Direct Local File Read ---
    try:
        # Check standard mapped paths
        possible_paths = [
            "/var/log/kyro/checkout.log",
            "../services/checkout-service/logs/checkout.log",
            "./services/checkout-service/logs/checkout.log",
            "./logs/checkout.log",
            "../logs/checkout.log",
            "../../logs/checkout.log"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    lines = f.readlines()
                    # Return the last 30 lines
                    return [line.strip() for line in lines[-30:] if line.strip()]
    except Exception as e:
        return [f"Log retrieval failed: {str(e)}"]
        
    return ["No logs found in Loki or log files."]
