<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The logic above is what was used to solve the final assignment. But, after thinking about it some more it probably isn't entirely correct. Elements that haven't been encountered yet should be left unset in the profile matrix. If this change were applied, the example above would end up looking more like this...

|                  |  0  |  1  |  2  |  3  |  4  |  5  |  6  |
|------------------|-----|-----|-----|-----|-----|-----|-----|
| Probability of T | 0.5 |     |     |     |     |     |     |
| Probability of R |     | 0.5 |     |     |     |     |     |
| Probability of M |     | 0.5 |     |     |     |     |     |
| Probability of E |     |     | 1.0 |     |     |     |     |
| Probability of L |     |     |     | 1.0 | 1.0 |     |     |
| Probability of O |     |     |     |     |     | 1.0 |     |
| Probability of W |     |     |     |     |     |     | 0.5 |

Then, when scoring an element against a column in the profile matrix, ignore the unset elements in the column. The score calculation in the example above would end up being...

```python
max(
    score('W', 'R') * profile_mat[1]['R'],
    score('W', 'M') * profile_mat[1]['M']
)
```
</div>

