from pydantic import BaseModel

class Incident(BaseModel):
    service: str
    message: str
    severity: str
