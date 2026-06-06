<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Fillets_FC and chamfers_FC are notoriously brittle for non-destructive workflows. For example, if you add a fillet_FC/chamfer_FC but then make a modification in a previous step of the non-destructive workflow, the fillet_FC/chamfer_FC will fail. The edges will have changed and fillet_FC/chamfer_FC typically isn't able to automatically guess what the new edges are. 

For this reason, I've seen only that they recommend leaving fillet_FC/chamfer_FC operations until the very end.

Tested on FreeCAD 1.1.1.
</div>

