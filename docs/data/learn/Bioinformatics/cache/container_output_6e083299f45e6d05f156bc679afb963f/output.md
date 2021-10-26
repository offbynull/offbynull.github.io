<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The example below hard codes k to 18, but you typically don't know what k should be set to beforehand. The Pevzner book doesn't discuss how to work around this problem. A strategy for finding k may be to run the motif matrix finding algorithm multiple times, but with a different k each time. For each member_MOTIF, if the k-mers selected across the runs came from the same general vicinity of the gene's upstream region, those k-mers may either be picking ...

 * the actual member_MOTIF.
 * a part of the actual member_MOTIF.
 * a part of the actual member_MOTIF with some junk prepended/appended to it.
</div>

