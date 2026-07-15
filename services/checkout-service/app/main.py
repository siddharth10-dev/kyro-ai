import os
import time
import logging
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from app.database import check_connection, save_order
from app.payment import process_payment
from prometheus_client import Gauge

db_health = Gauge("db_health_status", "Database connection status", multiprocess_mode="livesum")
payment_health = Gauge("payment_gateway_status", "Payment gateway status", multiprocess_mode="livesum")
cpu_usage = Gauge("simulated_cpu_usage_percent", "Simulated CPU usage", multiprocess_mode="livesum")
memory_usage = Gauge("simulated_memory_usage_percent", "Simulated Memory usage", multiprocess_mode="livesum")
disk_usage = Gauge("simulated_disk_usage_percent", "Simulated Disk usage", multiprocess_mode="livesum")

# Initialize defaults
db_health.set(1)
payment_health.set(1)
cpu_usage.set(20)
memory_usage.set(40)
disk_usage.set(50)
# Set up logs folder and log path
log_dir = "/var/log/kyro"
try:
    os.makedirs(log_dir, exist_ok=True)
except Exception:
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "checkout.log")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file, mode="a")
    ]
)
logger = logging.getLogger("checkout-service")

# Simulation states
simulation_state = {
    "database_error": False,
    "high_latency": False,
    "payment_failure": False
}

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Checkout Service")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrument the app and expose /metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    logger.info("Accessing root endpoint")
    return {"message": "Welcome to Checkout Service"}

@app.get("/health")
def health_check():
    logger.info("Accessing health check")
    if simulation_state["database_error"]:
        logger.error("Health check failed: Database connection down")
        raise HTTPException(status_code=500, detail="Database connection down")
    return {"status": "healthy"}

@app.post("/checkout")
def checkout(payload: dict = None):
    logger.info("Checkout request received")
    
    if simulation_state["high_latency"]:
        logger.warning("Simulating high latency: sleeping for 5 seconds")
        time.sleep(5)
        
    try:
        check_connection(simulation_state["database_error"])
    except Exception as e:
        logger.error(f"Checkout database error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    try:
        process_payment(99.99, simulation_state["payment_failure"])
    except Exception as e:
        logger.error(f"Checkout payment error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    try:
        save_order("ord_12345", simulation_state["database_error"])
    except Exception as e:
        logger.error(f"Checkout database save error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    logger.info("Checkout successfully completed")
    return {"status": "success", "message": "Payment successful"}

@app.post("/simulate/database-error")
def simulate_database_error(enable: bool = True):
    simulation_state["database_error"] = enable
    db_health.set(0 if enable else 1)
    logger.warning(f"Database error simulation set to {enable}")
    return {"message": f"Database error simulation set to {enable}"}

@app.post("/simulate/high-latency")
def simulate_high_latency(enable: bool = True):
    simulation_state["high_latency"] = enable
    logger.warning(f"High latency simulation set to {enable}")
    return {"message": f"High latency simulation set to {enable}"}

@app.post("/simulate/payment-failure")
def simulate_payment_failure(enable: bool = True):
    simulation_state["payment_failure"] = enable
    payment_health.set(0 if enable else 1)
    logger.warning(f"Payment failure simulation set to {enable}")
    return {"message": f"Payment failure simulation set to {enable}"}

@app.post("/simulate/cpu-spike")
def simulate_cpu_spike(enable: bool = True):
    cpu_usage.set(95 if enable else 20)
    logger.warning(f"CPU spike simulation set to {enable}")
    return {"message": f"CPU spike simulation set to {enable}"}

@app.post("/simulate/memory-leak")
def simulate_memory_leak(enable: bool = True):
    memory_usage.set(90 if enable else 40)
    logger.warning(f"Memory leak simulation set to {enable}")
    return {"message": f"Memory leak simulation set to {enable}"}

@app.post("/simulate/disk-full")
def simulate_disk_full(enable: bool = True):
    disk_usage.set(100 if enable else 50)
    logger.warning(f"Disk full simulation set to {enable}")
    return {"message": f"Disk full simulation set to {enable}"}
