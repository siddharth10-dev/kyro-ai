class AlertAgent:

    def classify(self, incident):

        message = incident.message.lower()

        if "500" in message:
            category = "backend-error"

        elif "latency" in message:
            category = "performance"

        elif "database" in message:
            category = "database"

        else:
            category = "unknown"


        if incident.severity.lower() == "critical":
            priority = "P1"

        elif incident.severity.lower() == "high":
            priority = "P2"

        else:
            priority = "P3"


        return {
            "service": incident.service,
            "category": category,
            "priority": priority
        }