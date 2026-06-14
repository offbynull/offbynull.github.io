<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

It sounds like what's happening here is that when you go to create a joint_FC, it attaches to a frame_FC to each of the component_FC elements_FC you've selected (it centers them?).

* The first frame_FC is attached to component_FC 1's element_FC and has its own LCS_FC.
* The second frame_FC is attached to component_FC 2's element_FC and has its own LCS_FC.

The translation/rotation adjustments move the component_FC relative to the frame_FC it's attached to:

* **Offset1** is relative to the first frame_FC's LCS_FC
* **Offset2** is relative to the second frame_FC's LCS_FC.

That is, the frame_FCS stays in place, but the component_FC it's attached to moves around (e.g., translates out 5mm and rotates over Z-axis by 45 degrees).

I suppose it's like this because you can't position and rotate frames_FC. You select the element_FC and a frame_FC gets attached to it at some place on the element_FC in some orientation, and it's your responsibility to adjust the translation and rotation to ensure it's as expected?

![FreeCAD assembly workbench offset both advanced example](freecad_assembly_offset_both_advanced_example.png)
</div>

