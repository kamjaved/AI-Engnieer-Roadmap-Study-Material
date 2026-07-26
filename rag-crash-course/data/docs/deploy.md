Deploying a new release to production follows a fixed sequence. First,
merge to main only after CI passes: unit tests, integration tests, and
the lint check. Once merged, the deploy pipeline builds a container
image tagged with the commit SHA and pushes it to the internal
registry. Never deploy an image built from a local machine.

Deployments go to staging automatically on every merge. Promotion to
production requires a manual approval from a platform on-call engineer,
triggered via the deploy dashboard, not the CLI directly.

Rollouts use a canary strategy: 5% of production traffic for 10
minutes, then 25%, then 100%, with automatic rollback if error rates
exceed 2% at any stage. Manual rollback is available at any time via
`deploy rollback <service> --to <previous-sha>`.

If a deploy needs to happen outside business hours, it requires
explicit sign-off from the on-call lead, logged in the incident
channel, since off-hours deploys have historically caused more
incidents due to reduced review bandwidth.

After any production deploy, watch the service dashboard for 30
minutes minimum before considering the deploy "safe." Silent
regressions — elevated latency without hard errors — are the most
common thing missed by teams that stop watching too early.