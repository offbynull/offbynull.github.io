<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The book mentions that it's convenient to define 0! as 1.

* `{kt} {n \choose n} = \frac{n!}{(n-n)!n!} = \frac{n!}{0!n!} = \frac{n!}{1 \cdot n!} = \frac{n!}{n!} = 1`.
* `{kt} {n \choose 0} = \frac{n!}{(n-0)!0!} = \frac{n!}{n!0!} = \frac{n!}{n! \cdot 1} = \frac{n!}{n!} = 1`.

The reason for `{kt} {n \choose n} = 1` is that, in a set of size n, there is exactly 1 subset of size n. Likewise, the reason for `{kt} {n \choose 0} = 1` is that, in a set of size n, there is exactly 1 subset of size 0.

The book also mentions that `{kt} {n \choose r} = 0` when r is out of bounds (r < 0 or r > n). It doesn't say why.
</div>

