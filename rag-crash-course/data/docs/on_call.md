On-call rotates weekly, Monday to Monday, across the platform team's
six engineers. The current rotation schedule is maintained in the
on-call tool, not in a shared spreadsheet, since the tool handles
timezone conversion and escalation automatically.

Primary on-call is paged first for any triggered alert. If there's no
acknowledgment within 5 minutes, the page automatically escalates to
secondary on-call, then to the team lead after another 5 minutes with
no response.

Being on-call means carrying a laptop and reliable internet access at
all times during the rotation window, including evenings and weekends.
Swapping a shift is allowed with 48 hours notice through the on-call
tool, so the escalation chain stays accurate.

Every page must be acknowledged even if it turns out to be a false
alarm — silently dismissing a page without acknowledgment breaks the
escalation timer's assumptions and can result in an unnecessary
escalation to the next person in the chain.

At the end of each rotation, the outgoing on-call writes a short
handoff note: anything still being watched, any alerts that fired and
why, and any follow-up tickets filed. This handoff is reviewed at the
next team sync.