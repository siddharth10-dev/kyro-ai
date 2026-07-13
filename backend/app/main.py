import datetime
import logging
from fastapi import FastAPI, HTTPException
import uvicorn

from app.schemas.incident import Incident
from graph.workflow import sentinel_graph
from app.database import (
    init_db,
    save_incident,
    get_all_incidents,
    get_incident_by_id,
    update_incident_status
)
from app.agents.communication_agent import CommunicationAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi.middleware.cors import CORSMiddleware

class SentinelAI(FastAPI):
    def __init__(self):
        super().__init__()
        self.title = "Sentinel AI"
        self.version = "1.0.0"

app = SentinelAI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

communication_agent = CommunicationAgent()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def read_root():
    return {"status": "UP"}

@app.post("/incident")
def log_incident(incident: Incident):
    initial_state = {
        "incident": incident,
        "classification": {},
        "investigation": {},
        "root_cause": {},
        "runbook": {},
        "recommendation": {},
        "timeline": []
    }
    
    # Run the graph workflow
    result = sentinel_graph.invoke(initial_state)
    
    # Set status to pending_approval on creation
    result["status"] = "pending_approval"
    
    # Add timeline event indicating waiting for human action
    timeline = list(result.get("timeline", []))
    time_str = datetime.datetime.now().strftime("%H:%M")
    timeline.append(f"{time_str} Waiting for human approval")
    result["timeline"] = timeline
    
    # Save the incident with the pending status
    db_id = save_incident(result)
    
    return {
        "status": "pending_approval",
        "incident_id": db_id,
        "result": {
            "incident": {
                "service": result["incident"].service,
                "message": result["incident"].message,
                "severity": result["incident"].severity
            },
            "classification": result["classification"],
            "investigation": result["investigation"],
            "root_cause": result["root_cause"],
            "runbook": result["runbook"],
            "recommendation": result["recommendation"],
            "timeline": result["timeline"],
            "status": "pending_approval"
        }
    }

@app.get("/incidents")
def list_incidents():
    return get_all_incidents()

@app.get("/incidents/{incident_id}")
def get_incident(incident_id: int):
    incident = get_incident_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@app.post("/incidents/{incident_id}/approve")
def approve_incident(incident_id: int):
    # Fetch incident
    incident_dict = get_incident_by_id(incident_id)
    if not incident_dict:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    if incident_dict["status"] != "pending_approval":
        raise HTTPException(
            status_code=400,
            detail=f"Incident is in status '{incident_dict['status']}', expected 'pending_approval'."
        )
        
    # Generate communication reports
    try:
        communication_reports = communication_agent.generate_reports(incident_dict)
    except Exception as e:
        logger.error(f"Error generating communication reports: {e}")
        communication_reports = {
            "incident_report": f"# Incident Report\n\nFailed to generate report automatically.",
            "executive_summary": "Failed to generate executive summary.",
            "slack_message": "🚨 *Incident resolution approved*."
        }
        
    # Update timeline
    timeline = list(incident_dict.get("timeline", []))
    time_str = datetime.datetime.now().strftime("%H:%M")
    timeline.append(f"{time_str} Recommendation approved by human")
    timeline.append(f"{time_str} Communication reports generated")
    
    # Update status to resolved
    updated = update_incident_status(
        incident_id=incident_id,
        status="resolved",
        communication_data=communication_reports,
        timeline=timeline
    )
    
    return {
        "status": "resolved",
        "message": "Incident approved and resolved successfully.",
        "incident_id": incident_id,
        "communication": communication_reports,
        "timeline": timeline
    }

@app.post("/incidents/{incident_id}/reject")
def reject_incident(incident_id: int):
    # Fetch incident
    incident_dict = get_incident_by_id(incident_id)
    if not incident_dict:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    if incident_dict["status"] != "pending_approval":
        raise HTTPException(
            status_code=400,
            detail=f"Incident is in status '{incident_dict['status']}', expected 'pending_approval'."
        )
        
    # Update timeline
    timeline = list(incident_dict.get("timeline", []))
    time_str = datetime.datetime.now().strftime("%H:%M")
    timeline.append(f"{time_str} Recommendation rejected by human")
    
    # Update status to rejected
    updated = update_incident_status(
        incident_id=incident_id,
        status="rejected",
        timeline=timeline
    )
    
    return {
        "status": "rejected",
        "message": "Incident recommendation rejected.",
        "incident_id": incident_id,
        "timeline": timeline
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)