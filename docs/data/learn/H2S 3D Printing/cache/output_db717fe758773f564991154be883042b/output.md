<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

It's totally unclear / undocumented how loft makes its transitions between sketches. For example, ...

* there's nothing saying which vertexes line up with which vertexes between sketches,
* there's nothing saying what happens when there's more vertexes in one sketch vs the next,
* there's nothing saying what algorithm is used to bridge the gap between sketches:
  * edges between sketches turned into planar faces vs curved surfaces - if curved, what defines the curvature?
  * sketch 1 is a square, sketch 2 is the same square rotated 45 degrees - loft bends 45 degrees, but why not 180+45 degrees or 360+45 degrees?

All ChatGPT says is that it delegates to OpenCASCADE.

Notes from source:

* To better control the shape of the loft, it is recommended that all cross-sections have the same number of segments. For example, for a loft between a rectangle and a circle, the circle should be broken down into 4 connected arcs.
* You can loft from or toward a single vertex from a sketch or the body.
* Vertices can only be either the start or end of a loft. Otherwise the loft body would consist of two solids connected at a single point. This would violate the CAD kernel's definition of a 3D object.
* A cross-section cannot lie on the same plane as the one immediately preceding it.
* If the sketch has inner geometry, then the order in which the sketch geometry is created should be the same for all sections. Either start all sections with the inner geometry, or start them all with the outer. Otherwise an invalid loft will be created where inner and outer walls cross.
* It is not possible to loft disjoint or crossing loops.
* Some failure modes will turn the part black.
</div>

