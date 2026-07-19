<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

For effective use of this joint_FC type, you'll likely need to use helper geometry: Datum points_FC, datum planes_FC, local coordinate systems_FC, and sketch_FC elements_FC. Note the use of helper geometry in the second example screenshot above: The grounded joint_FC is a body_FC with nothing but a sketch_FC line on the z-axis and a sketch_FC line on the x-axis. The revolve joint_FC is using one of those lines as its revolving axis, and the slider joint_FC is using the other line as the sliding axis.
</div>

