# CPU Throttling Runbook

## Symptoms
- High response latency and long request queue lengths.
- CPU throttle percentage metrics showing non-zero values in container group metrics.
- High thread contention or context switching rates in APM traces.

## Recovery Steps
1. Verify container CPU limit and CPU shares configurations in container manifest or `docker-compose.yml`.
2. Increase container CPU limits to allow burst capacity during high traffic events.
3. Check application threads for resource contention, locks, or heavy infinite loops.
4. Move non-blocking, compute-heavy tasks to asynchronous background queues (e.g. Celery, Redis).
