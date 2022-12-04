<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

There is no stable support for timezones. The timezone used by all cron jobs is whatever the timezone of the controller manager is (other parts of the doc say unspecified timezone). There currently is a beta feature that's gated off that lets you specify a timezone by setting `spec.timeZone` (e.g. setting it to `Etc/UTC` will use UTC time).
</div>

