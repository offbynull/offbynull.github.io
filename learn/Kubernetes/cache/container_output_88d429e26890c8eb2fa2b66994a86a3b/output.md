<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The scaling guarantees described here can be relaxed through `spec.podManagementPolicy`. By default, this value is set to `OrderedReady`, which enables the behavior described in this section. If it were instead set to `Parallel`, the stateful set's scaling will launch / terminate pods in parallel and won't wait for preceding pods to be healthy.
</div>

