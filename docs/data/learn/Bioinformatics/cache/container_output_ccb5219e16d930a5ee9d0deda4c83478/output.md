<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The column `last_to_first` wasn't discussed in the prerequisites but it was in their code. It simply maps the `last` value at a specific index to its index within `first`. For example, (a,3) is contained at index ...

* index 6 for `last`
* index 3 for `first`

So, at index 6 (where `last=(a,3)`), the `last_to_first` value points to index 3 (where `first=(a,3)`). Recall that `last_to_first` is just there to allow for quickly testing for a substring, which goes in reverse from the last column to the first column.
</div>

