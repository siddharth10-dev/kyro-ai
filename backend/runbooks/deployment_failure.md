# Deployment Configuration Failure Runbook

## Symptoms
- Service crashing immediately on startup (CrashLoopBackOff).
- Environment variable misconfigurations or bad flag simulation.
- Log entries showing: "high latency simulation set to True", "simulating database error", or "error simulation enabled".
- Latest git commit introduced configuration changes that broke startup.

## Recovery Steps
1. Identify the latest deployment commit from Git logs.
2. Check for simulation flags (e.g., `high_latency`, `database_error`, `payment_failure`) in the latest commit or configuration files.
3. Revert or disable the simulation configuration (e.g., POST to simulation config endpoints with `enable=false` or disable=true).
4. Redeploy the last known stable commit if configuration fixes do not resolve the issue.
