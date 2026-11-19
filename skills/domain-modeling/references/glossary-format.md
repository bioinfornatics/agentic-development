# Glossary format

A glossary fixes the words a project uses for its own domain concepts. It is not
a specification, a design note or a record of implementation choices.

## Layout

One context, the common case: a single `GLOSSARY.md` at the repository root.

~~~md
# Clinic scheduling

Books patients with practitioners and keeps the agenda consistent.

## Language

**Appointment**:
A reserved time slot that links one patient to one practitioner.
_Avoid_: booking, meeting

**No-show**:
An appointment the patient neither attended nor cancelled before it started.
_Avoid_: missed visit, absence
~~~

Several bounded contexts: a root `GLOSSARY-MAP.md` links each context's own
glossary and states how the contexts relate, such as the events or identifiers
they share.

## Rules

- Include only concepts specific to this domain. General programming notions,
  such as timeouts or error types, do not belong even when the code uses them often.
- Choose one canonical term per concept and list the rejected synonyms under `_Avoid_`.
- Define what the concept is in one or two sentences, not what the code does with it.
- Group terms under subheadings only when natural clusters appear.
- Create the file, or a context's file, only when its first term is resolved.
- When a definition changes, update it in place; a changed meaning with lasting
  consequences may also need a decision record.
