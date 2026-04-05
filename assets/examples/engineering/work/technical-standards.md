# Technical Standards

## System Design

- Every important runtime object should have a stable identifier or query path.
- Prompt, skill, tool surface, and UI should describe the same workflow.
- UI must not invent semantics that the backend cannot justify.

## Engineering Quality

- Installation and startup scripts are part of the product, not afterthoughts.
- Frontend and backend changes must be checked together when the behavior spans both layers.

## Verification

- Verify the actual rendered component or running bundle, not only the edited file.
- Distinguish source correctness from deployment correctness.
