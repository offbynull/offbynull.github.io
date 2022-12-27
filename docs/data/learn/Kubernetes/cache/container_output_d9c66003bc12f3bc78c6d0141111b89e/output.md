<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

So, it seems like these hooks don't actually test your manifests. They're sanity checking your manifests after they've already been applied? There's a secondary tool called Chart Testing Tool that allows you to do more elaborate tests: different configurations, `Chart.yaml` schema validation, ensuring `Chart.yaml` has its version incremented if using source control, etc...
</div>

