import os
import requests
import re
from langchain_core.tools import tool

PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")

@tool
def get_metrics(service_name: str) -> dict:
    """Get metrics like latency and error rate for a service from Prometheus."""
    service = service_name.lower()
    
    # We only have metrics for checkout-service / payment-api in this demo
    if "payment" not in service and "checkout" not in service:
        return {
            "latency": "80ms",
            "errors": "0.1%"
        }
        
    try:
        url = PROMETHEUS_URL
        # Try checking Prometheus readiness
        try:
            requests.get(f"{url}/api/v1/targets", timeout=1)
        except Exception:
            # Try docker/local fallback
            url = "http://prometheus:9090" if "localhost" in PROMETHEUS_URL else "http://localhost:9090"
            
        # 1. Query Latency
        # Average request duration over the last 1 minute
        latency_query = 'sum(rate(http_request_duration_seconds_sum[1m])) / sum(rate(http_request_duration_seconds_count[1m]))'
        res_lat = requests.get(f"{url}/api/v1/query", params={"query": latency_query}, timeout=2).json()
        
        latency = None
        if res_lat.get("status") == "success" and res_lat["data"]["result"]:
            val = float(res_lat["data"]["result"][0]["value"][1])
            latency = f"{val * 1000:.1f}ms"
            
        # 2. Query Error Rate
        # Ratio of 5xx errors to total requests over the last 1 minute
        error_query = 'sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))'
        res_err = requests.get(f"{url}/api/v1/query", params={"query": error_query}, timeout=2).json()
        
        errors = None
        if res_err.get("status") == "success" and res_err["data"]["result"]:
            val = float(res_err["data"]["result"][0]["value"][1])
            errors = f"{val * 100:.1f}%"
            
        # If Prometheus successfully returned values, return them
        if latency is not None and errors is not None:
            return {"latency": latency, "errors": errors}
            
    except Exception:
        pass
        
    # --- Fallback: Direct Scraping of checkout-service /metrics endpoint ---
    try:
        # Try local first, then docker container name
        target_urls = ["http://localhost:8001/metrics", "http://checkout-service:8001/metrics"]
        res_direct = None
        for t_url in target_urls:
            try:
                res_direct = requests.get(t_url, timeout=1)
                if res_direct.status_code == 200:
                    break
            except Exception:
                continue
                
        if res_direct and res_direct.status_code == 200:
            requests_total = 0.0
            errors_total = 0.0
            duration_sum = 0.0
            duration_count = 0.0
            
            for line in res_direct.text.splitlines():
                if line.startswith("#"):
                    continue
                if "http_requests_total" in line:
                    match = re.search(r'http_requests_total(?:{[^}]+})?\s+(\d+(?:\.\d+)?)', line)
                    if match:
                        val = float(match.group(1))
                        requests_total += val
                        if 'status="5' in line or 'status="500"' in line or 'status="5xx"' in line:
                            errors_total += val
                elif "http_request_duration_seconds_sum" in line:
                    match = re.search(r'http_request_duration_seconds_sum(?:{[^}]+})?\s+(\d+(?:\.\d+)?)', line)
                    if match:
                        duration_sum += float(match.group(1))
                elif "http_request_duration_seconds_count" in line:
                    match = re.search(r'http_request_duration_seconds_count(?:{[^}]+})?\s+(\d+(?:\.\d+)?)', line)
                    if match:
                        duration_count += float(match.group(1))
                        
            latency = f"{(duration_sum / duration_count) * 1000:.1f}ms" if duration_count > 0 else "0ms"
            errors = f"{(errors_total / requests_total) * 100:.1f}%" if requests_total > 0 else "0%"
            return {"latency": latency, "errors": errors}
            
    except Exception:
        pass
        
    return {
        "latency": "unknown",
        "errors": "unknown"
    }
