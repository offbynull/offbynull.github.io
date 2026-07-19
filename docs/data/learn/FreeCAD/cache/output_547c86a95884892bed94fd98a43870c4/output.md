<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

It looks like the safest bet is to build your own datum plane_FC. To place a datum plane_FC perpendicular to some face's orientation, ...

1. create a sketch_FC on the face and insert 3 points in an L shape.
2. exit the sketch_FC and reference those points to create a datum plane_FC.
3. set the datum plane_FC's **Attachment mode** to either **Align O-N-Y** or **Align O-Y-N**.

Instead of a sketch_FC with points, you can also try placing 3 datum points_FC on the face's edges, moving those datum points_FC using the **Map Path Property** (it's hidden in the properties tab - you need to right click and show hidden properties).
</div>

