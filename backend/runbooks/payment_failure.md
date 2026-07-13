# Payment Gateway Failure Runbook

## Symptoms
- Payment transactions returning 5xx or API timeouts during checkout.
- Log entries showing: "payment gateway timeout", "Stripe API error", "Failed payment authorization", or "unreachable service".
- Checkout-service throws network errors or gateway timeout status codes.

## Recovery Steps
1. Check status page of the third-party payment provider (e.g., Stripe, PayPal, Braintree).
2. Verify API keys, client secrets, and environment configurations are valid and not expired.
3. Adjust request timeout limits and retry backoff configurations in checkout-service.
4. Failover to backup payment gateway provider if primary remains offline.
