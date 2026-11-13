<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Much like loft_FC, it's totally unclear / undocumented how pipe_FC makes its transitions between sketches_FC (e.g., which vertexes line up with which vertexes between sketches_FC, what happens when there's more vertexes in one sketch_FC vs the next).

Notes from source:

* To better control the shape of the pipe_FC, it is recommended that all cross-sections have the same number of segments. For example, for a pipe_FC between a rectangle and a circle, the circle should be broken down into 4 connected arcs.
* You can pipe_FC from or toward a single vertex from a sketch_FC or the body_FC.
* When you select a vertex as section, it must be the last section of the pipe_FC. Otherwise the pipe_FC body_FC would consist of two solids connected at a single point. This would violates the CAD kernel's definition of a 3D object. You can change the order of the sections by dragging them in the list.
* The path can only be from a single sketch_FC, feature_FC or ShapeBinder. In case you want to !!sweep!! along several edges from different sketches_FC, use a SubShapeBinder.
* The path must not contain branches or T-junctions etc. Loops are allowed.
* It can lead to issues if the cross-section is not perpendicular to the path in 3D.
* A cross-section cannot lie on the same plane as the one immediately preceding it.
* The cross-sections must not contain !!disjoint!! or crossing loops.
* If the sketch_FC has inner geometry, then the order in which the sketch_FC geometry is created should be the same for all sections. Either start all sections with the inner geometry, or start them all with the outer. Otherwise an invalid pipe_FC will be created where inner and outer walls cross.
</div>

