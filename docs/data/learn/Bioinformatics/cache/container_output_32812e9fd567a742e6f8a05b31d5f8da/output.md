<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

At this stage, it might be worth trying to squash the first column. For example, all "a" symbol instances in the first column are ordered one after another, so you don't need to explicitly list them out. You just need to make sure you adjust how you're doing last-to-first pointer mapping to account for the first column being squashed.

```{svgbob}
ORIGINAL      SQUASHED   

 +--+--+       +--+--+
 |¶1|a3|       |¶ |a1|
 |a3|n2|       |a |n1|
 |a2|n1|       |  |n2|
 |a1|b1|       |  |b1|
 |b1|¶1|       |b |¶1|
 |n2|a2|       |n |a2|
 |n1|a1|       |  |a3|
 +--+--+       +--+--+
```
</div>

