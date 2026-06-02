<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

One thing I found that might be useful for the future:

1. Attach to the datum point to an edge (and nothing else) and set **Attachment mode** to **On edge**.
2. Click OK to finish placing the datum point.
3. Select the datum point, right-click in the Properties pane, and enable **Show hidden**.
4. Set the **Map Path Parameter** to move the point along the line (between 0 to 1).

Why does this matter? I wanted to use this to appropriately position a helix, but it didn't work out. You can use two datum points to make a datum line, but a datum line is infinite (it doesn't have a start/stop). Furthermore, FreeCAD currently doesn't let you further put a datum point on that datum line. The idea I had was to use datum points to create a datum line, then place a datum point on that datum line to act as the center point for a datum plane. The datum plane's normal would be defined with another datum line that's 90 degrees to the first datum line.

ChatGPT instead suggested I place a sketch on the face with ...

* a point for the center of the helix rotation axis.
* a horizontal line from the point.
* a vertical line from the point.

Then, create a new datum plane and use the center point as reference 1, the horizontal line as reference 2, and the vertical line as reference 3, and **Align O-X-Y** as the **Attachment mode**. You can then attach a sketch to that datum plane and the origin will be the center point.
</div>

