<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Thickness_FC looks to be broken for custom curves outsides of shapes derived from conics (e.g., spheres, half spheres, cylinders). Anything that involves a custom curved face won't work.

One thing I've tried doing that may work in some cases where thickness_FC fails is a subtractive loft_FC. You take profile sketches_FC and punch through the solid. You may need to do multiple such subtractive lofts_FC to get what you're hoping for.
</div>

