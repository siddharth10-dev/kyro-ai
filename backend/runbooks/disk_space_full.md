# Disk Space Full Runbook

## Symptoms
- Service unable to write files, output logs, or process database transactions.
- Exception thrown in logs: "No space left on device" or "disk write failure".
- Alert indicating container or host root volume disk usage > 90%.

## Recovery Steps
1. Run `df -h` on the container or host to verify volume utilization.
2. Check log directory sizes and delete uncompressed old log archives.
3. Check log rotation rules (`logrotate`) and ensure log compression is enabled.
4. Clean up temporary files, unused Docker images/volumes (`docker system prune`), or expand volume capacity.
