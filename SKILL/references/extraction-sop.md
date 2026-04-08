# Extraction SOP

## Goal

Convert local history into stable, reusable operating assets and person-level claims without overfitting to noise.

## Procedure

1. Identify the source type.
2. Extract only high-signal candidate facts.
3. Classify each candidate into an asset family when relevant:
   - work
   - thought style
   - workflow
   - principles
   - taste
   - knowledge
   - preferences
   - corrections
4. Also classify each candidate into a person-graph dimension:
   - role
   - interest
   - preference
   - behavior
   - workflow
   - principle
   - constraint
   - knowledge
   - taste
5. Decide whether the candidate belongs in:
   - `evidence/`
   - stable claim only
   - stable claim plus `assets/`
6. Normalize the candidate into a reusable claim shape.
7. Record confidence, scope, and source linkage.

## Owner-centric claim extraction

When extracting for the person graph, prioritize questions like:

1. what does this reveal about the owner?
2. would this change how a future agent should work?
3. is this global or task-scoped?
4. is this explicit, corrected, repeated, or merely inferred?

Prefer claim forms such as:

- `owner --prefers--> concise_actionable_output`
- `owner --avoids--> long_prefatory_explanations`
- `owner --values--> evidence_first_reasoning`
- `owner --uses_workflow--> inspect_then_patch_then_verify`

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

In addition to the triple above, ask what it reveals about:

- the owner's preferences
- the owner's constraints
- the owner's stable workflow
- the owner's principles
- the owner's interests or role signals

## High-signal extraction patterns

- explicit constraints
- repeated decision rules
- repeated workflow sequences
- repeated correction patterns
- stable acceptance or rejection criteria
- durable writing or UI taste
- durable identity or role signals
- repeated topic investment or recurring interests
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
It is also better to keep a candidate as a weak claim than to flatten the owner into a false persona.

## Promotion bias by source type

- explicit user instruction: high promotion priority
- explicit user correction: highest promotion priority
- repeated accepted pattern: medium promotion priority
- assistant-only narration with no user response: low promotion priority
- project-specific runtime detail: evidence-first, promote only if cross-project reusable

## Scope rule

Do not assume every stable signal is global.

Many true claims are scoped:

- to one domain
- to one project
- to one task family

Scoped stability is still real stability.
