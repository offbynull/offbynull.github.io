<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

I had also thought up this metric: distorted average. That's the name I gave it but the official name for this may be something different.

```{kt}
d\_avg(D) = (\sum_{i=1}^{n}{{D_i}^{\frac{1}{e}}})^e
```

 * D is list of all edge weights in the graph
 * n is the elements in D
 * e is some number >= 1, typically set to 2 (higher means more resilient to outliers)

The distorted average is a concept similar to squared error distortion (k-means optimization metric). It calculates the average, but lessens the influence of outliers. For example, given the inputs [3, 3, 3, 3, 3, 3, 3, 3, 15], the last element (15) is an outlier. The following table shows the distorted average for both outlier included and outlier removed with different values of e ...

| e | without 15 | with 15 |
|---|------------|---------|
| 1 | 3          | 4.33    |
| 2 | 3          | 3.88    |
| 3 | 3          | 3.76    |
| 4 | 3          | 3.71    |

The idea is that most of the edges in the graph will be in the blossoming regions. The much larger edges that connect together those blossoming regions will be much fewer, meaning that they'll get treated as if they're outliers and their influence will be reduced.

In practice, with real-world data, distorted average performed poorly.

* There's noise.
* There are more than a handful of outliers.
* One outlier could be so disproportionately huge that it throws off the distorted average anyway (having less influence doesn't mean it has no influence).
* etc..
</div>

