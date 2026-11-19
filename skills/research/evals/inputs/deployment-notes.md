# Deployment notes

This is a fictional project brief and source excerpt, not a deployed system.

## Product brief B1
Operators need the invoice worker to start in the tenant cluster and read the tenant's invoice archive without a stored credential. The selected option combines an image-signature admission policy with workload identity. Reporting labels can be planned independently of worker deployment.

## Documentation excerpts D1 and D2
D1, admission-policy manual version 4, documents accepting signed images from registry.example when a configured signer matches the policy. D2, identity manual version 2, documents exchanging a service-account token for archive access when its issuer and subject match a tenant trust record. These excerpts describe the individual components, not this composition.

## Environment record E1
The tenant cluster's admission configuration, token issuer and trust record have not been inspected. No deployment or token exchange has been attempted. No tenant cluster access or deployment permission is available for this consultation. Platform owner Maya can arrange a tenant test window; that window is not yet approved.
