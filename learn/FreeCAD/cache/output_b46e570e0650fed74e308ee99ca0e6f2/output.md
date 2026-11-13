<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

A core mistake people often make with joints_FC is thinking that they can be !!compounded!!. A joint_FC removes all but some options for movement. That's why if you try to place a sliding joint_FC and a revolute joint_FC on the same pair of objects, they cancel each other out.

* The sliding joint_FC cancels out all motion except moving up and down an axis.
* The revolute joint_FC cancels out all motion except revolving around an axis.

The sliding joint_FC won't let the revolute joint_FC revolve, and the revolute joint_FC won't let the sliding joint_FC slide. See [here](https://forum.freecad.org/viewtopic.php?t=105828).
</div>

