

```python
df = pandas.read_csv('people.csv', index_col=0, skipinitialspace=True)
child = df['age'] < 18
overweight = df['overweight']
df = pandas.DataFrame(data={
  'child': child,
  'overweight': overweight,
  'both': child & overweight
})
print(df, end='\n\n')
print(f'{df["child"].mean()=}', end='\n\n')
print(f'{df["overweight"].mean()=}', end='\n\n')
print(f'{df["both"].mean()=}', end='\n\n')
```


<div style="border:1px solid black;">

```
     child  overweight   both
0    False        True  False
1    False       False  False
..     ...         ...    ...
998   True        True   True
999  False       False  False

[1000 rows x 3 columns]

df["child"].mean()=0.25

df["overweight"].mean()=0.5

df["both"].mean()=0.115

```

</div>

