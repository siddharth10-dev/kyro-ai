class RootCauseAgent:

    def analyze(self, investigation):

        logs = investigation.get("logs", [])
        metrics = investigation.get("metrics", {})

        root_cause = "Unknown issue detected"
        confidence = 0.50
        reasoning = []

        for log in logs:
            if "Database connection timeout" in log:
                root_cause = (
                    "Database connectivity issue causing service failures"
                )
                confidence = 0.90
                reasoning.append(
                    "Database timeout errors found in application logs"
                )

        latency = metrics.get("latency", "0ms")
        try:
            latency_value = int(latency.replace("ms", ""))
        except ValueError:
            latency_value = 0

        if latency_value > 2000:
            reasoning.append(
                "Service latency exceeded safe threshold"
            )
            confidence += 0.05

        return {
            "root_cause": root_cause,
            "confidence": min(confidence, 1.0),
            "reasoning": reasoning
        }
