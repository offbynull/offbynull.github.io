`{bm-disable-all}`[ch2_code/src/MotifLogo.py](ch2_code/src/MotifLogo.py) (lines 15 to 39):`{bm-enable-all}`

```python
def calculate_entropy(values: List[float]) -> float:
    ret = 0.0
    for value in values:
        ret += value * (log(value, 2.0) if value > 0.0 else 0.0)
    ret = -ret
    return ret

def create_logo(motif_matrix_profile: Dict[str, List[float]]) -> Logo:
    columns = list(motif_matrix_profile.keys())
    data = [motif_matrix_profile[k] for k in motif_matrix_profile.keys()]
    data = list(zip(*data))  # trick to transpose data

    entropies = list(map(lambda x: 2 - calculate_entropy(x), data))

    data_scaledby_entropies = [[p * e for p in d] for d, e in zip(data, entropies)]

    df = pd.DataFrame(
        columns=columns,
        data=data_scaledby_entropies
    )
    logo = lm.Logo(df)
    logo.ax.set_ylabel('information (bits)')
    logo.ax.set_xlim([-1, len(df)])
    return logo
```