`{bm-disable-all}`[ch8_code/src/clustering/KMeans_Lloyds.py](ch8_code/src/clustering/KMeans_Lloyds.py) (lines 245 to 263):`{bm-enable-all}`

```python
def k_means_PP_initializer(
        k: int,
        vectors: list[tuple[float]],
):
    centers = [random.choice(vectors)]
    while len(centers) < k:
        choice_points = []
        choice_weights = []
        for v in vectors:
            if v in centers:
                continue
            _, d = find_closest_center(v, centers)
            choice_weights.append(d)
            choice_points.append(v)
        total = sum(choice_weights)
        choice_weights = [w / total for w in choice_weights]
        c_pt = random.choices(choice_points, weights=choice_weights, k=1).pop(0)
        centers.append(c_pt)
    return centers
```