# Memory Leak and Out-Of-Memory (OOM) Runbook

## Symptoms
- Service heap size monotonically increasing over time.
- Container terminated with OOMKilled status (Exit code 137).
- Log lines containing: "java.lang.OutOfMemoryError", "Fatal error: Allowed memory size exhausted", or "JavaScript heap out of memory".

## Recovery Steps
1. Inspect JVM/Node/Python memory metrics for a steady upward trend without flattening.
2. Trigger a heap dump of the running process for memory profiling.
3. Restart the service container to temporarily reclaim memory and restore service.
4. Analyze recent code changes for unclosed streams, static cache accumulation, or event listener leaks.
