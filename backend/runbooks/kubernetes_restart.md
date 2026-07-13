# Kubernetes Pod CrashLoopBackOff Runbook

## Symptoms
- Pods failing readiness/liveness checks and going into CrashLoopBackOff state.
- Container restart count increasing in Kubernetes dashboard or CLI.
- Logs showing uncaught initialization exceptions, database connection failures, or port bind errors on startup.

## Recovery Steps
1. Check pod events using `kubectl describe pod <pod-name>` to identify why it is restarting.
2. Inspect container termination messages and logs of the previous container instance (`kubectl logs --previous`).
3. Verify that database or downstream dependencies are fully initialized and reachable during startup.
4. Check readiness and liveness probe configuration thresholds to ensure startup time is not exceeding probe timeouts.
