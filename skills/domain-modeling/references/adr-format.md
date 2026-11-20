# Decision record format

A decision record keeps the reason for a lasting choice beside the project, so the
choice is not quietly undone later.

## Location

Use the repository's existing decision folder and numbering when one exists. Otherwise
use `docs/decisions/NNNN-short-slug.md`, numbered one above the highest existing record,
and create the folder together with the first record.

## Test before offering a record

Answer three questions about the choice. Offer a record only when every answer is yes;
a single no means no record.

1. **Alternatives actually weighed?** At least one other option was considered and
   turned down for a stated reason.
2. **Costly to undo?** Reverting would take real effort or coordination, for example
   migrating data, changing a public API, a dependency or the deployment shape, or
   renegotiating with someone outside the team.
3. **Reason invisible in the code?** A careful reader of the source could not work out
   why, and the choice looks like an oversight.

Choices that pass: pricing a ride when the bike is locked rather than unlocked; keeping
rider location history for thirty days because of a privacy commitment; reconciling dock
counts nightly because dock firmware cannot push events. A naming preference, a library
swapped behind an interface or the only workable option does not pass.

## Shape

~~~md
# 0004 Price rides at lock time

Status: accepted

Docks lose connectivity during peak-hour unlock bursts, so the fare is computed when
the bike is locked and the ride closes. Rejected: pricing at unlock with a later
correction, which produced refunds riders found confusing.
~~~

Give the number and title, a status line (proposed, accepted, deprecated or superseded by NNNN),
then the situation, the choice, its reason and the rejected options in plain prose.
Length follows the decision; a few sentences usually suffice.

## Changing a decision

Never edit the decision of an accepted record. Write a new record that names the one it
replaces, then change only the old record's status line to `superseded by NNNN`.
