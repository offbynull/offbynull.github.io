<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

It looks like the safest bet is to build your own datum plane. To place a datum plane perpendicular to some face's orientation, ...

1. create a sketch on the face and insert 3 points in an L shape.
2. exit the sketch and reference those points to create a datum plane.
3. set the datum plane's **Attachment mode** to either **Align O-N-Y** or **Align O-Y-N**.

Instead of a sketch with points, you can also try placing 3 datum points on the face's edges, moving those datum points using the **Map Path Property** (it's hidden in the properties tab - you need to right click and show hidden properties).
</div>

