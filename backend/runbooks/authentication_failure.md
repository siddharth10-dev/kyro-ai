# Authentication and Authorization Failures Runbook

## Symptoms
- Clients or services receiving HTTP 401 Unauthorized or HTTP 403 Forbidden.
- Logs indicating signature verification failures, token expiration, or invalid credentials.
- Service fail to retrieve secrets or authenticate with key managers (e.g. Vault, AWS KMS).

## Recovery Steps
1. Verify certificate authority chain and secret keys are correct.
2. Check token expiration times and renew expired client credentials or certificates.
3. Inspect IAM policies, role permissions, or API scopes configured in the gateway.
4. Verify network connectivity and health of the identity provider (e.g., Keycloak, Auth0, Okta).
