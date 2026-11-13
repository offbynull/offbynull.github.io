<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Why is this?

* B1's forward computation is done in exactly the same way as it is for the left-hand side of B1's forward-backward split graph. It's just that this algorithm doesn't stop after reaching B1 (it goes all the way to SINK).
* B1's backward computation is done in exactly the same way as it is for the right-hand side of B1's forward-backward split graph. It's just that this algorithm doesn't stop after reaching B1 (it goes all the way to SOURCE).
</div>

