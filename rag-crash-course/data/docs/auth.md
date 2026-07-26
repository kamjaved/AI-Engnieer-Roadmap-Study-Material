All internal services authenticate using short-lived JWTs issued by
the central identity provider. Tokens expire after 15 minutes and must
be refreshed using the refresh token flow — services should never
request long-lived access tokens, even for internal-to-internal calls.

Service-to-service calls use a separate client-credentials flow, not
user tokens. Each service has its own client ID and secret, rotated
every 90 days automatically by the platform team. Manual rotation is
available if a secret is suspected compromised, via the credentials
dashboard.

Every token includes a `scope` claim limiting what it can access.
Requesting a broader scope than a service actually needs is flagged
during security review — the policy is least-privilege by default,
not "request everything and filter later."

Refresh tokens are stored encrypted at rest and are never logged, even
at debug log level. Any code path found logging a raw token value is
treated as a security incident, not a bug ticket, and triggers
mandatory secret rotation for the affected service.

Public-facing APIs additionally require an API key in front of the JWT
layer, primarily for rate-limiting and abuse tracking rather than as a
primary auth mechanism.