<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The reason for this is that both BWT matrices and suffix arrays have their rows lexicographically sorted in the same way. Since each row's truncation point is always at the end marker (¶), and there's only ever a single end marker in a row, any symbols after that end marker don't effect of the lexicographic sorting of the rows.

Try it and see. Take the BWT matrix in the example above and change the symbols after the truncation point to anything other than end marker. It won't change the sort order.

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
| ¶ | z | z | z | z | z | z |
| a | ¶ | a | a | a | a | a |
| a | n | a | ¶ | z | z | z |
| a | n | a | n | a | ¶ | a |
| b | a | n | a | n | a | ¶ |
| n | a | ¶ | z | z | z | z |
| n | a | n | a | ¶ | a | a |
</div>

