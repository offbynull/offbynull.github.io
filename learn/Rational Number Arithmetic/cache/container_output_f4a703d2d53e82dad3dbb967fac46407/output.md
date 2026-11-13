<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

If you know about decimal multiplication and decimal division already, you're essentially counting the number of fractional digits for the number that has more fractional digits, then multiplying each number by 10 for that many iterations.

1. Between 123.45 and 1.1, 123.45 has more fractional digits.
2. 123.45 has 2 digits in its fractional part.
3. Multiply the first number by 10 for 2 iterations...
  * 123.45 * 10 = 1234.5
  * 1234.5 * 10 = 12345
3. Multiply the second number by 10 for 2 iterations...
  * 1.1 * 10 = 11
  * 11 * 10 = 110

The results are guaranteed to have no fractional part, so you can use integer addition on them.

4. 12345 + 110 = 12445

Once you've added, divide the result by 10 for the same number of iterations to get back the result as a decimal number.

4. Divide the result by 10 for 2 iterations...
   * 12455 / 10 = 1245.5
   * 12455 / 10 = 124.55

The result is 124.55.
  
Multiplying by 10 shifts the decimal point to the right. Dividing by 10 shifts the decimal point to the left.
</div>

