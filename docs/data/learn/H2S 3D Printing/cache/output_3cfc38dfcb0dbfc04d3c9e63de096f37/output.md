<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

In the screenshot example, the sketch_FC defines the helix_FC's thread as well as the rotational cylinder's radius. Note how the sketch_FC is 9.9mm out from the center and **Axis** is set to **Vertical sketch_FC axis**, meaning the radius of the helix_FC is 9.9mm.

If your helix_FC follows a similar setup, unless you already have a face to attach to or want the helix_FC at the origin, it may be a good idea to place a datum plane_FC in the desired location and use it to sketch_FC out a helix_FC.

To place a datum plane_FC matching the face's orientation but with a specific origin:

1. Place a sketch_FC on the face with ...

   * a point for the center of the helix_FC rotation axis.
   * a horizontal line from the point.
   * a vertical line from the point.

2. Create a new datum plane_FC and use the center point as reference 1, the horizontal line as reference 2, and the vertical line as reference 3
3. Set **Attachment mode** to **Align O-X-Y**.
4. Place a sketch_FC to new datum plane_FC. The origin will be the center point.
</div>

