<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

You typically won't have to write this out by hand. The C++ standard library has the concept_TEMPLATEs `std::three_way_comparable` and `std::three_way_comparable_with`. The former makes sure that a type allows relational comparisons against the same type (same as the example above) while the former allows relational comparisons against different types (e.g. comparing an `int` against a `long`).

Both concept_TEMPLATEs are related to the spaceship operator.
</div>

