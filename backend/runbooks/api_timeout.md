# Downstream API Timeout Runbook

## Symptoms
- Requests to external APIs returning 504 Gateway Timeout or HTTP 408 Request Timeout.
- Thread pools or connection pools exhausted due to requests blocking on downstream I/O.
- Log traces showing timeouts to third-party endpoints (e.g., identity, shipping, messaging).

## Recovery Steps
1. Check DNS resolution and network path (using ping/traceroute) to the downstream API host.
2. Implement circuit breakers (e.g., Hystrix or Resilience4j) to fail fast when downstream is unhealthy.
3. Reduce HTTP client read and connect timeouts to prevent hogging application threads.
4. Consult status pages of the external provider or contact their support team.
