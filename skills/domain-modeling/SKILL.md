---
name: domain-modeling
description: Sharpens a project's domain language and records durable decisions. Use when domain terms conflict, are vague or overloaded, when creating or editing a glossary, or when recording an architecture decision; not for merely reading existing vocabulary.
---

# Domain modeling

## Intent and outcome

Make the shared domain language precise while a design is being discussed, and
record a durable decision only when a future reader needs it. Return resolved
terms and decision records as verified file changes when writing is authorized,
or as a clearly labeled proposal otherwise. This is an optional bounded
capability, not a development phase. Reading a glossary or decision records for
vocabulary is a habit of every phase and does not require this Skill.

## Procedure

1. Verify the caller's question, the sources in scope and current authority.
   Loading guidance grants no permission: writing a glossary or decision file is a
   repository change that needs current scoped write authority. Locate the domain
   language: a root glossary map lists several bounded contexts and where each
   glossary lives; otherwise a single root glossary applies. When several contexts
   exist and the topic's context is unclear, ask which one applies.
2. Challenge the language as it is used, one point at a time:
   - **Conflict.** When a term contradicts its glossary definition, quote the
     definition and ask which meaning is intended.
   - **Vagueness.** When a word is overloaded or fuzzy, propose one precise
     canonical term and name the distinct concepts it was hiding.
   - **Scenario.** Probe relationships with concrete edge cases that force a
     boundary decision, for example a partial refusal or a shared identifier.
   - **Code.** Check stated behavior against the code. Report a contradiction with
     its source location; do not ask the user for a fact you can read.
   Terms are the user's decision; facts are yours to verify.
3. Record each resolved term as it is settled, not in a final batch. Apply
   [the glossary format](references/glossary-format.md): domain concepts only,
   tight definitions, rejected synonyms listed. Keep implementation detail,
   specifications and scratch notes out of the glossary. Create a glossary only
   when the first term is resolved.
4. Offer a decision record only when the choice is hard to reverse, surprising
   without context and the result of a real trade-off between alternatives. If any
   condition is missing, skip it. Apply [the decision record format](references/adr-format.md).
5. Without write authority or capability, return the exact proposed glossary
   entries and decision records labeled as a proposal; never report a file as
   written when it was not. After an actual write, read the file back and report
   changed paths. STOP and return to the caller. Do not load a development phase,
   approve a plan, claim or close work, or infer implementation or Git authority.
   The caller keeps its own phase obligations and records accepted terms or
   decision candidates in its own output.

## Limits

A resolved term or recorded decision is not plan approval, a requirement or
acceptance evidence. Do not invent terms the user has not settled, rename code
symbols, or rewrite existing decision records; supersede one with a new record
that names it. Unresolved terms that block a decision remain open questions for
the caller.
