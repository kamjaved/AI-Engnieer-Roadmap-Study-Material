All public API endpoints are rate-limited per API key, not per IP,
since IP-based limits are unreliable behind shared corporate proxies.
The default limit is 100 requests per minute, with a burst allowance of
20 additional requests absorbed by a token-bucket algorithm.

Rate limit status is returned on every response via three headers:
`X-RateLimit-Limit`, `X-RateLimit-Remaining`, and
`X-RateLimit-Reset`. Clients should check `X-RateLimit-Remaining`
proactively rather than waiting for a 429 response.

Exceeding the limit returns HTTP 429 with a `Retry-After` header
indicating seconds until the window resets. Clients retrying without
respecting `Retry-After` will have their key temporarily suspended
after repeated violations within a short window.

Higher limits are available for approved internal services and
verified enterprise customers, configured per-key in the gateway
config, not hardcoded. Requests for a limit increase go through the
platform team, who evaluate based on documented traffic patterns, not
just anticipated need.

Internal service-to-service traffic authenticated via client
credentials is exempt from the public rate limit but is subject to a
separate, higher internal quota to prevent one misbehaving service from
degrading shared infrastructure for others.