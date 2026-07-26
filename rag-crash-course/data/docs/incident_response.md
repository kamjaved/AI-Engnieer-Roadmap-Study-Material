An incident is declared the moment customer impact is confirmed or
strongly suspected — waiting for full certainty before declaring wastes
critical early response time. Declaring an incident that turns out to
be a false alarm has near-zero cost; declaring one too late has a real
one.

The engineer who declares becomes incident commander until explicitly
handed off, and is responsible for coordination, not necessarily for
fixing the issue directly. A dedicated incident channel is created
immediately, and all relevant communication moves there rather than
scattered DMs.

Severity is assigned on a 1–4 scale based on customer impact and scope,
reassessed as new information comes in rather than fixed at
declaration time. Sev-1 pages the full response team immediately;
lower severities can wait for business hours if declared overnight.

Once mitigated, service returning to normal takes priority over root
cause analysis — stop the bleeding first, understand why later. A
postmortem is scheduled within 48 hours, blameless by policy, focused
on process and system gaps rather than individual mistakes.

Every incident gets a written summary distributed to the wider
engineering org, regardless of severity, so lessons don't stay siloed
within the team that handled it.