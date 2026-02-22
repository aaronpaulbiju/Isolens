# IsoLens Gateway Curl Guide

Short descriptions with example curl commands for all endpoints.

Defaults used in these examples:
- `dry_run=false`
- `raise_on_error=true`

## Ping

Health check for the gateway.

```bash
curl -s http://127.0.0.1:6969/api/ping
```

## Version

Return the current gateway version.

```bash
curl -s http://127.0.0.1:6969/api/version
```

## List VMs

List all registered VirtualBox VMs.

```bash
curl -s "http://127.0.0.1:6969/api/vms?dry_run=false&raise_on_error=true"
```

## List Running VMs

List currently running VMs.

```bash
curl -s "http://127.0.0.1:6969/api/vms/running?dry_run=false&raise_on_error=true"
```

## VM Info

Show information about a VM.

```bash
curl -s -X POST http://127.0.0.1:6969/api/vms/info \
  -H 'Content-Type: application/json' \
  -d '{"vm":"TestVM","machinereadable":true,"dry_run":false,"raise_on_error":true}'
```

## Start VM

Start a VM (optionally headless).

```bash
curl -s -X POST http://127.0.0.1:6969/api/vms/start \
  -H 'Content-Type: application/json' \
  -d '{"vm":"TestVM","headless":true,"dry_run":false,"raise_on_error":true}'
```

## Power Off VM

Force power off a VM.

```bash
curl -s -X POST http://127.0.0.1:6969/api/vms/poweroff \
  -H 'Content-Type: application/json' \
  -d '{"vm":"TestVM","dry_run":false,"raise_on_error":true}'
```

## Save State

Save VM state to disk.

```bash
curl -s -X POST http://127.0.0.1:6969/api/vms/savestate \
  -H 'Content-Type: application/json' \
  -d '{"vm":"TestVM","dry_run":false,"raise_on_error":true}'
```

## Pause VM

Pause VM execution.

```bash
curl -s -X POST http://127.0.0.1:6969/api/vms/pause \
  -H 'Content-Type: application/json' \
  -d '{"vm":"TestVM","dry_run":false,"raise_on_error":true}'
```

## Resume VM

Resume a paused VM.

```bash
curl -s -X POST http://127.0.0.1:6969/api/vms/resume \
  -H 'Content-Type: application/json' \
  -d '{"vm":"TestVM","dry_run":false,"raise_on_error":true}'
```

## Reset VM

Hard reset a VM.

```bash
curl -s -X POST http://127.0.0.1:6969/api/vms/reset \
  -H 'Content-Type: application/json' \
  -d '{"vm":"TestVM","dry_run":false,"raise_on_error":true}'
```

## Shutdown VM

Graceful shutdown (use `force=true` for forced shutdown).

```bash
curl -s -X POST "http://127.0.0.1:6969/api/vms/shutdown?force=false" \
  -H 'Content-Type: application/json' \
  -d '{"vm":"TestVM","dry_run":false,"raise_on_error":true}'
```

## Snapshot Take

Create a snapshot for a VM.

```bash
curl -s -X POST http://127.0.0.1:6969/api/vms/snapshot/take \
  -H 'Content-Type: application/json' \
  -d '{"vm":"TestVM","name":"Baseline","dry_run":false,"raise_on_error":true}'
```

## Snapshot Restore

Restore a named snapshot.

```bash
curl -s -X POST http://127.0.0.1:6969/api/vms/snapshot/restore \
  -H 'Content-Type: application/json' \
  -d '{"vm":"TestVM","name":"Baseline","dry_run":false,"raise_on_error":true}'
```

## Snapshot Restore Current

Restore the current snapshot.

```bash
curl -s -X POST http://127.0.0.1:6969/api/vms/snapshot/restore-current \
  -H 'Content-Type: application/json' \
  -d '{"vm":"TestVM","dry_run":false,"raise_on_error":true}'
```
