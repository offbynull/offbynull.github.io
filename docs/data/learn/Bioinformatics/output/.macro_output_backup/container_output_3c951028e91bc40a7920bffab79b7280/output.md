<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The last point may be confusing. All it's saying is that taking an indirect path between two species should produce a distance that's >= the direct path. For example, the direct path between cat and dog is 6: `dist(cat, dog) = 6`. If you were to instead jump from cat to lion `dist(cat, lion) = 2`, then from lion to dog `dist(lion, dog) = 5`, that combined distance should be >= to 6...

```
dist(cat, dog)  = 6
dist(cat, lion) = 2
dist(lion, dog) = 5

dist(cat, lion) + dist(lion, dog) >= dist(cat, dog)
        2       +        5        >=       6
                7                 >=       6
```

The Pevzner book refers to the this as the triangle inequality.

```{svgbob}
      2
cat ------ lion
   \        |
    \       |
     \      |
    6 \     | 5
       \    |
        \   |
         \  |
          \ |
          dog
```

Later on non-conforming distance matrices are discussed called non-additive distance matrices. I don't know if non-additive distance matrices are required to have this specific property, but they should have all others.
</div>

