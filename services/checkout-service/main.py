from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Checkout Service")

# Instrument application and expose /metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to Checkout Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/checkout")
def checkout():
    # Initially: payment successful
    # Later you'll intentionally break it (e.g. raise Exception("Database connection timeout"))
    return {"status": "success", "message": "Payment successful"}
