<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Simulations_FC are still very finicky in FreeCAD 1.1.1. Here's what I've experienced so far...

* segfaults.
* if you select conflicting joints_FC for motion, the simulation_FC seems to lockup / do nothing instead of showing an error.
* sometimes, clicking **Generate** will cause an error saying that it failed but the scrubber still shows up.  This may be because the motion being applied goes past the limits of the joint_FC (e.g., revolute joint_FC has a certain min/max angle set, but the simulation_FC exceeds it).
</div>

