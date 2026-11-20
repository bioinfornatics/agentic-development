---
name: domain-modeling
description: Settles ambiguous domain terms and records lasting design choices. Use when domain terms collide, drift or stay ambiguous, when a glossary must be created or changed, or when an architecture or design decision is to be recorded; not for looking up existing vocabulary.
---

# Domain modeling

An optional capability, not a development phase. It turns contested words into agreed
domain terms and, rarely, turns a weighed choice into a decision record. Any phase may
consult an existing glossary or decision record for vocabulary without this Skill.

## Preconditions

Confirm the caller's question, the sources in scope and the authority actually held.
Loading this Skill grants no permission: adding or changing a glossary or decision file
is a repository change that needs current scoped write authority. Look for the place
where the repository already keeps vocabulary and decisions before choosing one;
[the glossary format](references/glossary-format.md) gives the fallback. When the
repository has several bounded contexts and the topic is unclear, ask which one applies.

## Outcomes, in order

1. **A term problem is detected.** Compare how a word is used with the sources: the
   usage departs from a recorded definition, one word covers two concepts, two words
   name one concept, a word is too vague to decide a boundary case, or the code
   behaves otherwise than claimed. Read the code before
   trusting a stated behavior and cite the source location of any contradiction.
2. **The term is settled with the user.** Raise one point at a time. Quote the record
   or code involved, propose a single canonical term, and probe it with a boundary
   case from the domain, such as "Is a bike left beside a full dock a finished ride?"
   Terms are the user's decision; facts you can check are verified, never asked.
3. **The settled term is recorded.** Write each term as soon as it is settled, not at
   the end. Record domain concepts only, leaving software mechanics out: one
   canonical term, its rejected synonyms and a definition of what the concept is.
   Create a glossary file only for the first settled term.
4. **The need for a decision record is tested.** When the discussion produced a lasting
   choice, offer a record only when alternatives were actually weighed, undoing it
   would be costly and its reason is invisible in the code. If any test fails, skip
   the record. Apply [the decision record format](references/adr-format.md).
5. **Results are handed back.** Without write authority or the means to write, return
   the exact entries and records labeled as a proposal; never report a file as written
   when it was not. After a real write, read the file back and list changed paths.
   STOP and return to the caller. Do not load a development phase, approve a plan,
   claim or close work, or infer implementation or Git authority. The caller keeps its
   own phase obligations and carries accepted terms or decision candidates forward.

## Limits

Settled terms and decision records are not plan approval, requirements or acceptance
evidence. Never invent a term the user has not settled or rename code symbols. Never
rewrite an existing decision record; write a new one that supersedes it by name, and
change only the old record's status line. A term
still open when a decision depends on it goes back to the caller as an open question.
