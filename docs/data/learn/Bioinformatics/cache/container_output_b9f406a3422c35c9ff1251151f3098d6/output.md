```python
def center_of_gravity(data_pts, dim):
    center = []
    for i in range(dim):
        val = mean(pt[i] for pt in data_pts)
        center.append(val)
    return center
```