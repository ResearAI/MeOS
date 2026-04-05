# Extraction SOP

## Goal

Convert local history into stable, reusable operating assets without overfitting to noise.

## Procedure

1. Identify the source type.
2. Extract only high-signal candidate facts.
3. Classify each candidate into one of:
   - work
   - thought style
   - workflow
   - principles
   - taste
   - knowledge
   - preferences
   - corrections
4. Decide whether the candidate belongs in:
   - `evidence/`
   - `assets/`
5. Record confidence and source linkage.

## Transcript-aware extraction

When the source is a conversation or agent transcript, do not just summarize content.
Extract this triple:

1. user requirement or correction
2. assistant behavior or output pattern
3. user reaction:
   - accepted
   - corrected
   - redirected
   - unresolved

This is critical because stable operating rules often come from:

- repeated user corrections
- repeated approval of a certain answer shape
- repeated rejection of a certain framing mistake

## High-signal extraction patterns

- explicit constraints
- repeated decision rules
- repeated workflow sequences
- repeated correction patterns
- stable acceptance or rejection criteria
- durable writing or UI taste
- explicit audit output formats
- explicit acceptance gates such as throughput, batch size, page count, or experiment count
- repeated cross-layer requirements such as frontend/backend consistency

## Low-signal patterns

- one-off emotional phrasing
- context-specific project details
- temporary urgency language
- tool chatter without reusable lesson
- isolated casual approval with no reusable content
- private identifiers that do not change future task behavior

## Default stance

Be conservative.
It is better to keep a fact in `evidence/` than to promote a false rule into `assets/`.

## Promotion bias by source type

- explicit user instruction: high promotion priority
- explicit user correction: highest promotion priority
- repeated accepted pattern: medium promotion priority
- assistant-only narration with no user response: low promotion priority
- project-specific runtime detail: evidence-first, promote only if cross-project reusable
