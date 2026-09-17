# 0003. Local CLI distribution only

## Status
Accepted

## Context
Need to decide how far to invest in packaging/distribution for v1.

## Decision
Run from source / local install only. No PyPI publish, no container image for v1.

## Consequences
- No packaging/release pipeline needed yet.
- Revisit if the tool needs to be shared beyond the author's own machine(s).
