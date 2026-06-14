<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

There's a bug in 1.1.1 (and maybe other versions) where angles \< 180 or \> 180 roll over. Sometimes that's a problem because it can only target the interior angle range instead of the exterior angle range (or vice versa - I forget). You can workaround the bug by going into the joint_FC's properties and setting **Limits** → **Angle Min** / **Angle Max**.
</div>

