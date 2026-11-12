# Deployment planning input
A personal cloud project needs one managed secret store and non-human identities.
Provider services are selected; their APIs are available, but workload bootstrap
identity delivery has not yet been decided. No cloud changes are authorized.
Existing inspected files: infra/root.hcl (provider), infra/identity/main.tf (groups),
ci.yml (jobs), config/encryption.yaml (recipient public identifiers).
Preserve groups, remote state, local private keys and existing user edits.
Do not implement consumer applications as part of the identity foundation.
