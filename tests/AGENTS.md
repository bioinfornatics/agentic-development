# Source-contract checks

These tests validate the portable method's source, links and hypothetical scenario
consistency. They do not execute an agent workflow, a host integration or a release.
Run python3 -m unittest discover -s tests -v; no third-party dependency is needed.
Keep expected requirements independently tied to the user scope, not copied from
implementation output. A static red/green cycle is not behavioral TDD evidence.
