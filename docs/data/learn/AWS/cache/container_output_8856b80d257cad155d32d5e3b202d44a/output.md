<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The learning material advises against inline policies. Instead, it says you can create a managed policy and set a condition on it such that it only applied when attached to the identity of interest: `"StringEquals": { "aws:username": "johndoe" }`.
</div>

