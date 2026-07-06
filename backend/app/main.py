from fastapi import FastAPI
import uvicorn
from schemas.incident import Incident
from agents.alert_agent import AlertAgent
from agents.investigen import InvestigationAgent
from agents.root_cause_agent import RootCauseAgent
from agents.runbook_agent import RunbookAgent
from agents.recommendation_agent import RecommendationAgent

alert_agent = AlertAgent()
investigation_agent = InvestigationAgent()
root_cause_agent = RootCauseAgent()
runbook_agent = RunbookAgent()
recommendation_agent = RecommendationAgent()

class SentinelAI(FastAPI):
    def __init__(self):
        super().__init__()
        self.title = "Sentinel AI"
        self.version = "1.0.0"

app = SentinelAI()

@app.get("/health")
def read_root():
    return {"status" : "UP"}

@app.post("/incident")
def log_incident(incident: Incident):

    result = alert_agent.classify(incident)
    investigation_result = investigation_agent.investigate(incident)
    root_cause_result = root_cause_agent.analyze(investigation_result)
    runbook_result = runbook_agent.retrieve(root_cause_result)

    return {
        "status": "classified",
        "analysis": result,
        "investigation": investigation_result,
        "root_cause": root_cause_result,
        "runbook": runbook_result,
        "recommendation": recommendation_agent.recommend(
            root_cause_result,
            runbook_result
        )
    }







if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)