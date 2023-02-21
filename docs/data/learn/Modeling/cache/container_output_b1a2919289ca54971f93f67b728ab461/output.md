

```python
df = pandas.read_csv('people.csv', index_col=0, skipinitialspace=True)
print(df, end='\n\n')
child = df['age'] < 18
print(f'{sum(child == True)=}', end='\n\n')
```


<div style="border:1px solid black;">

```
     age  overweight
0     22        True
1     53       False
..   ...         ...
998    1        True
999   76       False

[1000 rows x 2 columns]

sum(child == True)=250

```

</div>

