# Glossary format

The glossary records the meaning of words the project uses for its own domain. It holds
meanings only: requirements, designs, implementation choices and working notes belong
elsewhere.

## Location

1. If the repository already keeps a glossary or vocabulary page, extend it in place and
   follow its existing shape.
2. Otherwise, a project with one context uses `docs/glossary.md`.
3. A project with several bounded contexts uses `docs/glossary/index.md`, which lists
   each context with a one-line purpose, the path of its glossary and the identifiers
   or events it shares with others. Each context then has `docs/glossary/<context>.md`.

Create a file only when its first term is settled; never commit an empty skeleton.

## Entry shape

~~~md
# Bike sharing

## Dock
A fixed slot at a station that holds and charges one bike.
Not: rack, stand, station

## Ride
One rental, from unlocking a bike at a dock to locking it at any dock.
Not: trip, journey, session
~~~

## Admitting a term

Answer these in order before writing an entry:

1. Would someone who works in the domain, without reading the code, use this word?
   If not, leave it out: infrastructure vocabulary belongs to the code.
2. Which single word will the project use from now on? The others go on its `Not:`
   line.
3. Can a reader decide, for a real case, whether it is an instance? Draw that line,
   as the Ride entry does from unlock to lock, instead of describing processing steps.

Keep entries alphabetical, and split a long context by sub-domain only when readers
struggle to find terms. When a meaning changes, edit the entry in place; if the
change alters a lasting choice, run the decision record test as well.
