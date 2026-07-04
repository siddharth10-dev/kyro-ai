from fastapi import FastAPI
import uvicorn
from schemas.incident import Incident
from agents.alert_agent import AlertAgent
from agents.investigen import InvestigationAgent
alert_agent = AlertAgent()
investigation_agent = InvestigationAgent()

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

    return {
        "status": "classified",
        "analysis": result,
        "investigation": investigation_agent.investigate(incident)
    }






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)