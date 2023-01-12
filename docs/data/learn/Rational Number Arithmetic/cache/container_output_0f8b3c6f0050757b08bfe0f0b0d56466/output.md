<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The reasoning behind why trailing 0s can be removed and re-appended has to do with expressions / order of operations / factoring. Taking the original 4500 / 7 example above...

 * 4500 / 7
 * (45 * 100) / 7  <-- factor out 100 from the 4500
 * 45 * 100 / 7 <-- remove parenthesis, associativity law, mult and div have same precedence so it doesn't matter which gets performed first
 * 45 / 7 * 100 <-- swap, commutative law, mult and div have same precedence so it doesn't matter which gets performed first
 * (45 / 7) * 100
 * (7R3) * 100
 * 700R300
</div>

