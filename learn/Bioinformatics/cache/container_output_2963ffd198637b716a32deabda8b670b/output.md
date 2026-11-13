<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Why represent a gap as a non-emitting hidden state? Because technically, a gap means the sequence didn't move forward (no symbol emission happened -- in otherwords, forgo a symbol emission). For example, if your sequence is BAN and the alignment starts with a gap (-), you still need to emit the initial B symbol later on...

| 0 | 1 | 2 | 3 |
|---|---|---|---|
| - | B | A | N |
| G | - | A | N |

By the end, all of BAN should have been emitted.
</div>

