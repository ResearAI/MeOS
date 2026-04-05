# Correction Policy

## Principle

Corrections have the highest priority in MeOS maintenance.

## What counts as a correction

- explicit user rejection of a prior assumption
- explicit refinement of a previous rule
- explicit statement that a former pattern was overfit, too specific, or wrong

## Correction behavior

1. preserve the previous claim in `evidence/` if it matters historically
2. write the new preferred rule into `assets/corrections/overrides.md`
3. update the affected asset file if the correction is strong enough to replace the old rule
4. do not leave two contradictory "active" rules without annotation

## Output rule

If a correction changes actual task behavior, mention that the active operating rule has been updated.
