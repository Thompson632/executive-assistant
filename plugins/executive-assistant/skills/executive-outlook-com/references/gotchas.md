# Local Input Gotchas

## Metadata Sources

Read explicitly configured local sources or files supplied by the user.
Keep credentials and client data outside the package.

## Sender Addresses

Use the supplied sender address when present. Report missing addresses as
unavailable and avoid external lookups.

## Local Links Go Stale

Use `./scripts/unix/ea.sh resolve --path PATH` on the exact supplied file path.
Treat a missing file as stale. Avoid guessing by searching other folders.

## Calendar Recurrences

Each input contains the occurrences returned by its source. Preserve
recurring-event flags where available and surface ambiguity before proposing
changes.

## Private Items

Calendar file records marked private expose times and a generic title. The
Apple provider uses generic titles by default because its interface does not
identify private events. Keep private locations, attendees, and bodies out of
shared results.

## Attachment Paths

Use an absolute destination within the configured vault. Preview the copy
before applying. Writes preserve files already at the destination.
