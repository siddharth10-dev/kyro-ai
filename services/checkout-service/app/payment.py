import logging

logger = logging.getLogger("checkout-service")

def process_payment(amount: float, simulate_error: bool):
    if simulate_error:
        logger.error(f"Payment processing failed for amount ${amount}: Gateway timeout")
        raise Exception("Payment gateway timeout")
    logger.info(f"Payment of ${amount} processed successfully via gateway")
