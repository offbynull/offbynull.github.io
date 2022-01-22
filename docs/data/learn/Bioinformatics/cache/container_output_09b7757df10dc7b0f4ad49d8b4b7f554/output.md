<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

Think about what's happening here. With standard Lloyd's algorithm, you're averaging out a component for a center. For example, the points 5, 4, and 3 are calculated as ...

```
(5 + 4 + 3) / (1 + 1 + 1)
(5 + 4 + 3) / 3
12 / 3
4
```

With this algorithm, you're doing the same thing except weighting them by their confidence values. For example, if the points above had the confidence values 0.9, 0.8, 0.95 respectively, they're calculated as ...

```
((5 * 0.9) + (4 * 0.8) + (3 * 0.95)) / (0.9 + 0.8 + 0.95)
(4.5 + 3.2 + 2.85) / 2.65
10.55 / 2.65
3.98
```

The Lloyd's algorithm center of gravity calculation is just this algorithm's center of gravity calculation with all 1 confidence values ...

```
((5 * 1) + (4 * 1) + (3 * 1)) / (1 + 1 + 1)
(5 + 4 + 3) / (1 + 1 + 1)
(5 + 4 + 3) / 3
12 / 3
4
```
</div>

