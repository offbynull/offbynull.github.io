

```python
df = pandas.read_csv('people.csv', index_col=0, skipinitialspace=True)
print(df, end='\n\n')
child = df['age'] < 18
print(child)
print(sum(child == True), end='\n\n')
print(sum(child == False), end='\n\n')
```


<div style="border:1px solid black;">

```
     age obese
id            
P0    40     F
P1    39     T
P2    12     F
..   ...   ...
P21   24     F
P22   54     T
P23   33     T

[22 rows x 2 columns]

id
P0     False
P1     False
P2      True
       ...  
P21    False
P22    False
P23    False
Name: age, Length: 22, dtype: bool
2

20

```

</div>

