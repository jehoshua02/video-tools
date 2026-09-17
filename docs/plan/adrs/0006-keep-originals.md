# 0006. Keep originals; skip when target mp4 exists

## Status
Accepted

## Context
Converting `foo.mkv` produces `foo.mp4`. If the original stays, a re-run would
convert it again unless skip rules cover it. Extends [[0005-v1-deliverable-batch-mp4-conversion]].

## Decision
- Never delete or move the original.
- Output goes next to the original as `<stem>.mp4`.
- Skip a file when it is itself `.mp4`, or when `<stem>.mp4` already exists.

## Consequences
- Re-runs are no-ops for converted files.
- Disk use grows (both copies kept); user cleans up manually.
- Name clash: `foo.mkv` and `foo.avi` both map to `foo.mp4`; the second is skipped.
