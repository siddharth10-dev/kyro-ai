from app.tools.logs import get_logs
from app.tools.metrics import get_metrics


class InvestigationAgent:


    def investigate(self, incident):


        logs = get_logs(
            incident.service
        )


        metrics = get_metrics(
            incident.service
        )


        return {

            "service":
            incident.service,


            "logs":
            logs,


            "metrics":
            metrics
        }