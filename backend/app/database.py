import os
import logging
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/sentinel")

Base = declarative_base()

class IncidentRecord(Base):
    __tablename__ = 'incidents'
    
    id = Column(Integer, primary_key=True)
    service = Column(String(100))
    message = Column(Text)
    severity = Column(String(50))
    category = Column(String(100))
    priority = Column(String(50))
    summary = Column(Text)
    investigation = Column(JSON)
    root_cause = Column(JSON)
    runbook = Column(JSON)
    recommendation = Column(JSON)
    timeline = Column(JSON)
    status = Column(String(50), default="pending_approval")
    communication = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

engine = None
SessionLocal = None

def init_db():
    global engine, SessionLocal
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        logging.info("PostgreSQL database initialized and tables created.")
    except Exception as e:
        engine = None
        SessionLocal = None
        logging.error(f"Failed to initialize database: {e}")


def save_incident(incident_data: dict) -> int:
    global SessionLocal
    if SessionLocal is None:
        init_db()
    if SessionLocal is None:
        logging.error("SessionLocal is not initialized. Cannot save incident.")
        return None
        
    session = SessionLocal()
    try:
        record = IncidentRecord(
            service=incident_data["incident"].service,
            message=incident_data["incident"].message,
            severity=incident_data["incident"].severity,
            category=incident_data["classification"].get("category", ""),
            priority=incident_data["classification"].get("priority", ""),
            summary=incident_data["classification"].get("summary", ""),
            investigation=incident_data["investigation"],
            root_cause=incident_data["root_cause"],
            runbook=incident_data["runbook"],
            recommendation=incident_data["recommendation"],
            timeline=incident_data.get("timeline", []),
            status=incident_data.get("status", "pending_approval")
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        logging.info(f"Successfully saved incident {record.id} to PostgreSQL database.")
        return record.id
    except Exception as e:
        logging.error(f"Error saving incident to DB: {e}")
        return None
    finally:
        session.close()

def update_incident_status(incident_id: int, status: str, communication_data: dict = None, timeline: list = None) -> dict:
    global SessionLocal
    if SessionLocal is None:
        init_db()
    if SessionLocal is None:
        logging.error("SessionLocal is not initialized. Cannot update incident.")
        return None

    session = SessionLocal()
    try:
        record = session.query(IncidentRecord).filter(IncidentRecord.id == incident_id).first()
        if not record:
            logging.error(f"Incident with ID {incident_id} not found.")
            return None
        
        record.status = status
        # If status is resolving or approved, add timestamp
        if status in ["resolved", "approved"]:
            record.resolved_at = datetime.datetime.utcnow()
            
        if communication_data is not None:
            record.communication = communication_data

        if timeline is not None:
            record.timeline = timeline
            
        session.commit()
        logging.info(f"Successfully updated incident {incident_id} to status {status}.")
        return {
            "id": record.id,
            "status": record.status,
            "resolved_at": record.resolved_at.isoformat() if record.resolved_at else None,
            "communication": record.communication,
            "timeline": record.timeline
        }
    except Exception as e:
        logging.error(f"Error updating incident status: {e}")
        return None

    finally:
        session.close()


def get_all_incidents():
    global SessionLocal
    if SessionLocal is None:
        init_db()
    if SessionLocal is None:
        return []
        
    session = SessionLocal()
    try:
        records = session.query(IncidentRecord).order_by(IncidentRecord.created_at.desc()).all()
        results = []
        for r in records:
            results.append({
                "id": r.id,
                "service": r.service,
                "message": r.message,
                "severity": r.severity,
                "classification": {
                    "category": r.category,
                    "priority": r.priority,
                    "summary": r.summary
                },
                "investigation": r.investigation,
                "root_cause": r.root_cause,
                "runbook": r.runbook,
                "recommendation": r.recommendation,
                "timeline": r.timeline,
                "status": r.status,
                "communication": r.communication,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "resolved_at": r.resolved_at.isoformat() if r.resolved_at else None
            })
        return results
    except Exception as e:
        logging.error(f"Error retrieving incidents from DB: {e}")
        return []
    finally:
        session.close()

def get_incident_by_id(incident_id: int) -> dict:
    global SessionLocal
    if SessionLocal is None:
        init_db()
    if SessionLocal is None:
        return None
        
    session = SessionLocal()
    try:
        r = session.query(IncidentRecord).filter(IncidentRecord.id == incident_id).first()
        if not r:
            return None
        return {
            "id": r.id,
            "service": r.service,
            "message": r.message,
            "severity": r.severity,
            "classification": {
                "category": r.category,
                "priority": r.priority,
                "summary": r.summary
            },
            "investigation": r.investigation,
            "root_cause": r.root_cause,
            "runbook": r.runbook,
            "recommendation": r.recommendation,
            "timeline": r.timeline,
            "status": r.status,
            "communication": r.communication,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "resolved_at": r.resolved_at.isoformat() if r.resolved_at else None
        }
    except Exception as e:
        logging.error(f"Error retrieving incident {incident_id} from DB: {e}")
        return None
    finally:
        session.close()

