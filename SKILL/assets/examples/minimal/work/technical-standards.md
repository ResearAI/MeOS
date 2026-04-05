# Technical Standards

## Architecture

- Identify the real source of truth before patching a visible symptom.
- Prefer one convergent system over several overlapping partial systems.

## Verification

- Do not call an implementation done until the real acceptance gate is checked.
- Separate source edits from live-behavior verification.

## Acceptance Gates

- If the user asked about one concrete runtime parameter, verify that parameter directly.
- If only control files changed, say so plainly and do not present that as a new measured result.
