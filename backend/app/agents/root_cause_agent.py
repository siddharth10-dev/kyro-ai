class RootCauseAgent:
    def analyze(self, investigation: dict) -> str:
        logs = investigation.get("logs", [])
        metrics = investigation.get("metrics", {})

        # Check logs for known issues
        for log in logs:
            log_lower = log.lower()
            if "database connection timeout" in log_lower or "database timeout" in log_lower:
                return "Database connection timeout; database might be overloaded."
            if "database" in log_lower:
                return "Database issue detected."
            if "invalid token" in log_lower or "authentication" in log_lower:
                return "Authentication/Authorization failures; invalid or expired security credentials."
            if "500 internal server error" in log_lower:
                return "Uncaught backend exception causing 500 Internal Server Error."

        # Check metrics for performance-based root causes
        cpu = metrics.get("cpu", "")
        latency = metrics.get("latency", "")
        if cpu and cpu.endswith("%"):
            try:
                cpu_val = int(cpu.replace("%", ""))
                if cpu_val > 90:
                    return f"Resource saturation: High CPU utilization ({cpu})."
            except ValueError:
                pass

        if latency and latency.endswith("ms"):
            try:
                latency_val = int(latency.replace("ms", ""))
                if latency_val > 2000:
                    return f"Degraded performance: Service latency is high ({latency})."
            except ValueError:
                pass

        return "Undetermined root cause. Further manual investigation required."
