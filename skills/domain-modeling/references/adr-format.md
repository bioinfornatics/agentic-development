# Decision record format

A decision record explains why a lasting choice was made, so that a later reader
does not undo it by accident. Follow the repository's existing location and
numbering when one exists; otherwise use `docs/adr/NNNN-short-slug.md`, numbered
one above the highest existing record, and create the directory only for the
first record.

## When to write one

All three conditions must hold:

1. **Hard to reverse**: changing the choice later has a meaningful cost.
2. **Surprising without context**: a reader of the code would ask why.
3. **A real trade-off**: genuine alternatives existed and one was chosen for reasons.

Ask what a newcomer would most likely get wrong: a data store or vendor that is
costly to leave, a hidden external constraint such as a regulation or a partner's
response time, who owns which data and what is explicitly refused, a departure from
the usual approach, or an alternative that looks better but was rejected for a
reason. A reversible, unsurprising or uncontested choice needs no record.

## Template

~~~md
# Reports read from a replica

Monthly reports scan months of data and slowed down live scheduling, so they now
read from a read-only replica and may lag by up to a few minutes.
~~~

One paragraph stating context, decision and reason is often enough. Add a
status (proposed, accepted, deprecated, superseded by a named record), the
considered options or the consequences only when they help a future reader.
Never rewrite an accepted record to change its decision; write a new record that
supersedes it.
