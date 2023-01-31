<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

What's happening here? The right-hand side graph is being modified such that, when you go backwards, the terms being added in the expression are the same as when you go forward. That's all. This can't happen without the node duplication because the terms wouldn't end up being the same (as per the B2 example).

If you have no non-emitting states, your backward graph will have no duplicate nodes (same structure as the forward graph).

When computing backwards, SINK is being initialized to 1.0 similar to how B1 is initialized to 1.0 when computing forwards.
</div>

