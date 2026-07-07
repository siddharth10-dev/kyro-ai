class RootCauseAgent:


    def analyze(self, investigation):


        logs = investigation["logs"]

        metrics = investigation["metrics"]


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

        latency_value = int(
            latency.replace("ms","")
        )


        if latency_value > 2000:

            reasoning.append(
                "Service latency exceeded safe threshold"
            )

            confidence += 0.05



        return {

            "root_cause": root_cause,

            "confidence": min(confidence,1),

            "reasoning": reasoning

        }