Database schema changes go through a migration file, never a manual
`ALTER TABLE` run directly against production. Migrations live
alongside the service code and are applied automatically as part of
the deploy pipeline, before the new application version starts
receiving traffic.

Every migration must be backward-compatible with the previous
application version for at least one deploy cycle, since canary
rollouts mean old and new code run against the same database
simultaneously for several minutes. Adding a NOT NULL column without a
default, for example, breaks the still-running old version's inserts.

Destructive changes — dropping a column, renaming a table — require a
two-step migration across two separate deploys: first stop using the
old structure in application code, then remove it in a later
migration, never both in one step.

All migrations are reviewed by a second engineer with data-team
context before merge, specifically checking for lock duration on large
tables. A migration that takes an exclusive lock for more than a few
seconds on a hot table should be rewritten to use a non-blocking
strategy instead.

Migrations are never run manually against production by an individual
engineer, even during an incident — emergency schema changes still go
through the pipeline, just expedited.