import logging

logger = logging.getLogger("checkout-service")

def check_connection(simulate_error: bool):
    if simulate_error:
        logger.error("Database connection attempt failed: connection timeout")
        raise Exception("Database connection timeout")
    logger.info("Database connection verified successfully")

def save_order(order_id: str, simulate_error: bool):
    if simulate_error:
        logger.error(f"Failed to save order {order_id}: database connection timeout")
        raise Exception("Database connection timeout")
    logger.info(f"Order {order_id} saved successfully to database")
