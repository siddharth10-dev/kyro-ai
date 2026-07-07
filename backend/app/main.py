from fastapi import FastAPI
import uvicorn
from app.schemas.incident import Incident
from graph.workflow import sentinel_graph

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
    initial_state = {
        "incident": incident,
        "classification": {},
        "investigation": {},
        "root_cause": {},
        "runbook": {},
        "recommendation": {}
    }
    result = sentinel_graph.invoke(initial_state)
    return {
        "status": "completed",
        "result": result
    }







if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)