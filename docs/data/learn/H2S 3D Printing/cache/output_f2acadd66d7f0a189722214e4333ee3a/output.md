<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

One thing I found that might be useful for the future:

1. Attach to the datum point_FC to an edge (and nothing else) and set **Attachment mode** to **On edge**.
2. Click OK to finish placing the datum point_FC.
3. Select the datum point_FC, right-click in the Properties pane, and enable **Show hidden**.
4. Set the **Map Path Parameter** to move the point along the line (between 0 to 1).

Why does this matter? I wanted to use this to appropriately position a helix_FC, but it didn't work out. You can use two datum points_FC to make a datum line_FC, but a datum line_FC is infinite (it doesn't have a start/stop). Furthermore, FreeCAD currently doesn't let you further put a datum point_FC on that datum line_FC. The idea I had was to use datum points_FC to create a datum line_FC, then place a datum point_FC on that datum line_FC to act as the center point for a datum plane_FC. The datum plane_FC's normal would be defined with another datum line_FC that's 90 degrees to the first datum line_FC.

ChatGPT instead suggested I place a sketch_FC on the face with ...

* a point for the center of the helix_FC rotation axis.
* a horizontal line from the point.
* a vertical line from the point.

Then, create a new datum plane_FC and use the center point as reference 1, the horizontal line as reference 2, and the vertical line as reference 3, and **Align O-X-Y** as the **Attachment mode**. You can then attach a sketch_FC to that datum plane_FC and the origin will be the center point.
</div>

