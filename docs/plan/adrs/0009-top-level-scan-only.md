# 0009. Scan top-level folder only

## Status
Accepted

## Context
Need to decide whether the batch scan descends into subfolders.

## Decision
Scan only the files directly inside the given folder. No recursion.

## Consequences
- Predictable, limited blast radius.
- Nested folders need separate runs; a `--recursive` flag can come later.
