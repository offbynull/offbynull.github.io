```{title}
Algebra
```

```{toc}
```

# Introduction

PREREQ OF NEEDING TO KNOW ABOUT REAL NUMBERS AND ARITHMETIC OPERATIONS ON THOSE REAL NUMBERS.

TODO: continue with openstax elementary algebra, then intermediate algebra, then college algebra DO NOT DO THE PROBLEMS, JUST DO PROCESS AND TERMS

# Algorithms

## Prime Factorization

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

Every composite number can be written as a product of prime numbers. For example...

* 12 = 3\*2\*2
* 16 = 2\*2\*2\*2
* 21 = 3\*3\*3

The process of breaking down a composite number into a product of primes is called prime factorization. Prime factorization happens via the factor tree algorithm, which involves taking the input and recursively breaking it down into one of its factor pairs until all factors are prime.
   
   For example, to break down the number 54, choose one of its factor pairs...
   
   ```{svgbob}
   +----54----+
   |          |
   6          9
   ```
   
   Then, for each factor, break it down even further by choosing one of its factor pairs...
   
   ```{svgbob}
        +--------54--------+
        |                  |
   +----6----+        +----9----+
   |         |        |         |
   3         2        3         3
   ```
   
   All factors are now prime -- 54 = 3\*2\*3\*3.
   
   ```{note}
   Prime factors are typically written out from smallest to largest, so writing out the prime factors of the example above would be    54 = 2\*3\*3\*3.
   
   If you know exponents, the example above can be further condensed as `{kt} 54 = 2 \cdot 3^3`.
   ```
   
   When choosing a factor pair, the pair can't include 1 or the number being factored itself. For example, if choosing a factor pair    for 12..
    
   * ~~1*12=12~~ <-- can't choose this one
   * 2*6=12
   * 3*4=12
   * 4*3=12
   * 6*2=12
   * ~~12*1=12~~ <-- can't choose this one
   
   The reason why ...
    * 1 can't be used is because 1 is neither a prime nor can it be factorized to primes.
    * 12 (the number being factored itself) can't be used is because it effectively does nothing -- it finishes at the same place it    started at.
    
   For example, trying to build a factor tree for 12 using one of the bad factor pairs...
   
   ```{svgbob}
        +--------12--------+
        |                  |
        1             +----12----+
      (bad)           |          |
                      1       +--12--+
                    (bad)     |      |
                              1      ...
                            (bad)
   ```
   
   Note that the prime factors for a number will always be the same regardless of which factor pairs are chosen (as long as its a    valid factor pair). For example, in the initial example above, if 54 were factored to (2, 27) instead of (9, 6) ...
   
   ```{svgbob}
        +--------54--------+
        |                  |
        2             +----27---+
                      |         |
                      3     +---9---+
                            |       |
                            3       3
   ```
   
   The prime factors would still be 54 = 2\*3\*3\*3. 
   
   The way to perform this algorithm as code is as follows...
   
   ```{output}
   arithmetic_code/Factor.py
   python
   #MARKDOWN_FACTORTREE\s*\n([\s\S]+)\n\s*#MARKDOWN_FACTORTREE
   ```
   
   ```{arithmetic}
   FactorTreeLauncher
   24
   ```

## Least Common Multiple

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)



```{prereq}
Prime factor
```

The least common multiple is the process of taking 2 numbers and finding the smallest multiple between them. That is, if you listed out their multiples starting from 1, the first match between them would be the least common multiple.

There are 2 common algorithms used to find the least common multiple between 2 numbers.

The first algorithm is called the listing multiples method. It involves listing out the multiples for each number starting from 1 until there's a match. For example, finding the least common multiple between 4 and 6... 

|       | 1 |   2    |   3    |   4    | 5  |   6    | 7  | 8  |   9    |
|-------|---|--------|--------|--------|----|--------|----|----|--------|
| **4** | 4 |   8    | **12** |   16   | 20 | **24** | 28 | 32 | **36** |
| **6** | 6 | **12** |   18   | **24** | 30 | **36** |    |    |        |

is 12 because 6\*2=12 and 4\*3=12.

The way to perform this algorithm as code is as follows...

```{output}
arithmetic_code/LeastCommonMultiple.py
python
#MARKDOWN_WALK\s*\n([\s\S]+)\n\s*#MARKDOWN_WALK
```

```{arithmetic}
LeastCommonMultipleWalkLauncher
12 18
```

The second algorithm is called the prime factors method. It involves calculating the prime factors for each number and merging them to get the least common multiple. For example, finding the least common multiple between 4 and 6... 

 * prime factors of 4: 4 = 2 \* 2
 * prime factors of 6: 6 = 2 \* 2 \* 3
 * merge the prime factors together to get 12 = 2 \* 2 \* 3

   ```{svgbob}
          +-+  +-+
    4 "=" |2|  |2|
          +-+  +++
                |
          +-+   |   +-+
    6 "=" |2|   |   |3|
          +++   |   +++
           |    |    |
           |    |    |
           |    |    |
           v    v    v
          +-+  +-+  +-+
   12 "=" |2|  |2|  |3|
          +-+  +-+  +-+
   ```

   ```{note}
   What's actually happening in the "merge" above is that the primes are being segmented by value and the segment with the highest occurrence count is being picked...

   * prime 2 = {4=[2, 2], 6=[2]}
   * prime 3 = {4=[], 6=[3]}

   For prime 2, take from 4. From prime 3, take from 6.
   ```

The way to perform this algorithm as code is as follows...

```{output}
arithmetic_code/LeastCommonMultiple.py
python
#MARKDOWN_PF\s*\n([\s\S]+)\n\s*#MARKDOWN_PF
```

```{arithmetic}
LeastCommonMultiplePFLauncher
12 18
```

## Greatest Common Divisor

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)

TODO: fix me (add bookmarks for header, convert code)


```{prereq}
Factor
Prime factor
```

The greatest common divisor is the process of taking 2 numbers and finding the largest possible divisor between the two of them. In other words, finding the greatest number that evenly divides both numbers.

There are 3 common algorithms used to find the greatest common divisor between 2 numbers.

The first algorithm is to test divisions on incrementally larger numbers until you reach the smaller of the 2 numbers. The largest tested number that was evenly divisible is the greatest common divisor. For example, for the numbers 22 and 8...

 * `{kt} 22 \div 1 = 22` and `{kt} 8 \div 1 = 1` (both divisible)
 * `{kt} 22 \div 2 = 11` and `{kt} 8 \div 2 = 4` (both divisible)
 * `{kt} 22 \div 3 = 7R1` and `{kt} 8 \div 3 = 2R2` (both NOT divisible)
 * `{kt} 22 \div 4 = 5R2` and `{kt} 8 \div 4 = 2` (first NOT divisible)
 * `{kt} 22 \div 5 = 4R2` and `{kt} 8 \div 5 = 1R3` (both NOT divisible)
 * `{kt} 22 \div 6 = 3R4` and `{kt} 8 \div 6 = 1R2` (both NOT divisible)
 * `{kt} 22 \div 7 = 3R1` and `{kt} 8 \div 7 = 1R1` (both NOT divisible)
 * `{kt} 22 \div 8 = 2R6` and `{kt} 8 \div 8 = 1` (first NOT divisible)

The greatest common divisor is 2.

The way to perform this algorithm as code is as follows...

```{output}
arithmetic_code/GreatestCommonDivisor.py
python
#MARKDOWN_NAIVE\s*\n([\s\S]+)\n\s*#MARKDOWN_NAIVE
```

```{arithmetic}
GreatestCommonDivisorNaiveLauncher
22 8
```

The second algorithm is to factor both numbers and take the largest common factor between them. The largest common factor is the greatest common divisor. For example, for the numbers 22 and 8, ...

 * the factors of 22 are 1, 2, 11, and 22.
 * the factors of 8 are 1, 2, 4 and 8.

The greatest common factor between them is 2.

````{note}
You can also use prime factorization. Prime factorize both numbers to their prime factors -- any factors contained in both are prime factors of the greatest common divisor. For example...

* primeFactorize(22) is 2 \* 11.
* primeFactorize(8) is 2 \* 2 \* 2.

```{svgbob}
        +--+                +--+
22 "="  |2 |                |11|
        ++-+                +--+
         |
        ++-+   +--+   +--+
8  "="  |2 |   |2 |   |2 |
        ++-+   +--+   +--+
         |
         v
        +--+
GCD "=" |2 |
        +--+
```
````

The way to perform this algorithm as code is as follows...

```{output}
arithmetic_code/GreatestCommonDivisor.py
python
#MARKDOWN_FACTOR\s*\n([\s\S]+)\n\s*#MARKDOWN_FACTOR
```

```{arithmetic}
GreatestCommonDivisorFactorLauncher
22 8
```

The third algorithm is to use Euclid's algorithm to compute the greatest common divisor. This is the algorithm most used by both humans and computers to calculate the greatest common divisor because, for large numbers, it's less labour intensive than the other two methods.

Imagine the numbers 8 and 22. The algorithm starts by sorting the numbers from largest to smallest and dividing them:

 * `{kt} 22 \div 8 = 2R6`

It then takes the divisor and the remainder, sorts them from largest to smallest, and divides them again:

 * `{kt} 8 \div 6 = 1R2`

It keeps repeating this process until the remainder reaches 0. For this example, it only needs to repeat the process one more time:

 * `{kt} 6 \div 2 = 3R0`

The greatest common factor is the divisor when the remainder is 0. In this example, it's 2.

The way to perform this algorithm as code is as follows...

```{output}
arithmetic_code/GreatestCommonDivisor.py
python
#MARKDOWN_EUCLID\s*\n([\s\S]+)\n\s*#MARKDOWN_EUCLID
```

```{arithmetic}
GreatestCommonDivisorEuclidLauncher
22 8
```

````{note}
The following is my attempt at explaining Euclid's algorithm after reading several online resources. You need an understanding of geometry and algebra before continuing.

 * Geometric explanation

   Conceptually, you can think of Euclid's algorithm as recursively breaking off square chunks out of a rectangular area until it finds the smallest possible chunk that can be evenly copied to recreate the original rectangle. For example, imagine the numbers 21 and 6...
   
   ```{svgbob}
                  21
      +------------------------+
      |                        |
      |                        |
      |                        | 6
      +------------------------+
   ```
   
   Since in 21x6, 6 is the smaller side, break off 6 from the 21 to get a 6x6 block...
   
   ```{svgbob}
                      15
      +------+-----------------+
      |      |                 |
      | 6x6  |                 |
      |      |                 | 6
      +------+-----------------+
   ```
   
   Since in 15x6, 6 is the smaller side, break off 6 from the 15 to get a 6x6 block...
   
   ```{svgbob}
                          9
      +------+------+----------+
      |      |      |          |
      | 6x6  | 6x6  |          |
      |      |      |          | 6
      +------+------+----------+
   ```
   
   Since in 9x6, 6 is the smaller side, break off 6 from the 9 to get a 6x6 block...
   
   ```{svgbob}   
                             3
      +------+------+------+---+
      |      |      |      |   |
      | 6x6  | 6x6  | 6x6  |   |
      |      |      |      |   | 6
      +------+------+------+---+
   ```
   
   Since in 3x6, 6 is the smaller side, break off 3 from the 6 to get a 3x3 block...
   
   ```{svgbob}   
      +------+------+------+---+
      |      |      |      |3x3|
      | 6x6  | 6x6  | 6x6  +---+
      |      |      |      |   | 3
      +------+------+------+---+
                             3
   ```

   The remaining block is also 3x3 block. As such, the largest size that this entire rectangle can be constructed from is 3x3. The greatest common divisor is 3.
   
   ```{svgbob}   
      +------+------+------+---+
      |      |      |      |3x3|
      | 6x6  | 6x6  | 6x6  +---+
      |      |      |      |3x3|
      +------+------+------+---+
   ```

   Notice how this is subtracting from the larger side at each step. Since division is iterative subtraction, this entire algorithm can be done using division. Starting from the very beginning...

   ```{svgbob}
                  21
      +------------------------+
      |                        |
      |                        |
      |                        | 6
      +------------------------+
   ```
   
   Since in 21x6, 6 is the smaller side, break off as many blocks of 6 as possible from 21: `{kt} 21 \div 6 = 3R3` (3 blocks of 6x6, with 3 remaining)...

   ```{svgbob}   
                             3
      +------+------+------+---+
      |      |      |      |   |
      | 6x6  | 6x6  | 6x6  |   |
      |      |      |      |   | 6
      +------+------+------+---+
   ```

   Since in 3x6, 3 is the smaller side, break off as many blocks of 3 as possible from 6: `{kt} 21 \div 6 = 2R0` (2 blocks of 3x3, with 0 remaining)...

   ```{svgbob}   
      +------+------+------+---+
      |      |      |      |3x3|
      | 6x6  | 6x6  | 6x6  +---+
      |      |      |      |3x3|
      +------+------+------+---+
   ```

 * Algebraic explanation

   If 2 numbers are evenly divisible by some other number, then their sum/difference must also be divisible. For example, the numbers 21 and 6 are both divisible by 3:
   
   ```{svgbob}
         21 / 3 = 7R0                6 / 3 = 2R0
   
   +---+---+---+---+---+---+---+      +---+---+
   |xxx|xxx|xxx|xxx|xxx|xxx|xxx|      |xxx|xxx|
   +---+---+---+---+---+---+---+      +---+---+
   ```
   
   Since they're both divisible by 3, if you were to add 18 and 6 together, the sum would also be divisible by 3...
   
   ```{svgbob}
         21 / 3 = 7R0                6 / 3 = 2R0
   
   +---+---+---+---+---+---+---+      +---+---+
   |xxx|xxx|xxx|xxx|xxx|xxx|xxx|      |xxx|xxx|
   +---+---+---+---+---+---+---+      +---+---+
   
               |                          |
               |        21 + 6 = 27       |
               |                          |
               +-------------+------------+
                             |
                             v
           
                        27 / 3 = 9R0
          
          +---+---+---+---+---+---+---+---+---+
          |xxx|xxx|xxx|xxx|xxx|xxx|xxx|xxx|xxx|
          +---+---+---+---+---+---+---+---+---+
   ```
   
   Similarly, if you were to subtract 21 and 6, the difference would also be divisible by 3...
   
   ```{svgbob}
         21 / 3 = 7R0                6 / 3 = 2R0
   
   +---+---+---+---+---+---+---+      +---+---+
   |xxx|xxx|xxx|xxx|xxx|xxx|xxx|      |xxx|xxx|
   +---+---+---+---+---+---+---+      +---+---+
   
               |                          |
               |        21 - 6 = 15       |
               |                          |
               +-------------+------------+
                             |
                             v
   
                        15 / 3 = 5R0
                   
                   +---+---+---+---+---+
                   |xxx|xxx|xxx|xxx|xxx|
                   +---+---+---+---+---+
   ```
   
   Even if you don't know what the divisor is, you can recursively break down the problem using the rules stated above. Imagine that you didn't know that 3 was the divisor for the previous example, but you know that some evenly divisible number `{kt} d` existed...
   
   * `{kt} \frac{21}{d} = xR0`
   * `{kt} \frac{6}{d} = yR0`
   
   Since you know that the if 21 and 6 are both divisible by d, their difference must also be divisible by d...
   
   * `{kt} \frac{21 - 6}{d} = \frac{15}{d} = zR0`
   
   Now you know that 3 numbers are divisible by d: 21, 6, 15. Since you know that 15 and 6 are both divisible by d, their difference must also be divisible by d...
   
   * `{kt} \frac{15 - 6}{d} = \frac{9}{d} = wR0`
   
   Now you know that 4 numbers are divisible by d: 21, 6, 15, and 9. Since you know that 15 and 9 are both divisible by d, their difference must also be divisible by d...
   
   * `{kt} \frac{15 - 9}{d} = \frac{6}{d} = vR0`
   
   Now you know that 5 numbers are divisible by d: 21, 6, 15, 9, and 6. Since you know that 9 and 6 are both divisible by d, their difference must also be divisible by d...
   
   * `{kt} \frac{9 - 6}{d} = \frac{3}{d} = uR0`

   Now you know that 6 numbers are divisible by d: 21, 6, 15, 9, 6, 3. Since you know that 9 and 6 are both divisible by d, their difference must also be divisible by d...
   
   * `{kt} \frac{3 - 3}{d} = \frac{0}{d} = uR0`

   `{kt} 3-3` is 0, so the algorithm stops at this point -- d is 3.

   ```{note}
   Notice how for each subtraction step, the last 2 numbers are being chosen. When subtracting, the larger number goes first -- always subtract FROM the larger number.
   ```
   
   You can plug 3 for d into the expressions above and each will evaluate to a whole number (no remainder). This algorithm is continually reducing the problem until it converges to the single greatest common divisor...
   
   * `{kt} a - b` is divisible by d because both a and b are divisible by d
   * `{kt} a - (a - b)` is divisible by d because both a and (a - b) are divisible by d
   * `{kt} a - (a - (a - b))`  is divisible by d because both a and (a - (a - b)) are divisible by d
   * ...
````

# Terminology

 * `{bm} place value system/(place value system|place-value system|place value notation|place-value notation|positional numeral system)/i` - A way to represent a number. A number represented using the place value system is made up of a string of symbols separated by a dot, where each (index, symbol) combination in the string represents a value.

   The symbols used to represent a number are called `{bm} digit`s. All digits to the...

    * left of the dot represents entire objects, called the whole part.
    * right of the dot represents a partial object, called the fractional part.

   These wholes and fractional are combined to represent the final value for the number. For example, the number 43.5 represents...

   ```
   ●●●●●●●●●●
   ●●●●●●●●●●
   ●●●●●●●●●●
   ●●●●●●●●●●  ●●●     ◑
       4        3   .  5
   ```

 * `{bm} fraction/(fraction|numerator|denominator)/i` - A way of representing numbers with equally-sized partial objects. The syntax for a fraction is `{kt} \frac{numerator}{denominator}`, where the...

   * numerator (top) is an integer that represents the number of parts available.
   * denominator (bottom) is an integer that represents the number of parts in a whole.

   For example, if 4 parts make up a whole (denominator) and you have 9 of those parts (numerator), that's represented as `{kt} \frac{9}{4}`.

 * `{bm} proper fraction` - A fraction with less than 1 whole (e.g. `{kt} \frac{1}{2}`, `{kt} \frac{4}{5}`, and `{kt} \frac{3}{10}`).

 * `{bm} improper fraction` - A fraction with at least 1 whole (e.g. `{kt} \frac{3}{2}`, `{kt} \frac{5}{5}`, and `{kt} \frac{15}{3}`).

 * `{bm} equivalent fraction` - Two fractions that represent the same value even though they have different numerators and denominators (number of parts may be different, but the overall value represented by the fraction is the same). For example, `{kt} \frac{3}{2}`, `{kt} \frac{6}{4}`, and `{kt} \frac{12}{8}` are all considered equivalent fractions because they represent the same value.

 * `{bm} simplified fraction/(simplified fraction|simplify)/i` - Of all equivalent fractions for a fraction, the one with smallest numerator and denominator. For the example above, `{kt} \frac{3}{2}` is the simplified fraction for both `{kt} \frac{12}{8}` and `{kt} \frac{6}{4}`.

 * `{bm} common denominator` - Two fractions that have the same value for the denominator. For example, the fractions `{kt} \frac{1}{2}` and `{kt} \frac{1}{3}` don't have a common denominator, but their equivalent fractions `{kt} \frac{3}{6}` and `{kt} \frac{2}{6}` do.

 * `{bm} reciprocal` - A fraction with its numerator and denominator swapped. For example, the reciprocal of `{kt} \frac{5}{6}` is `{kt} \frac{6}{5}`.

 * `{bm} mixed number` - A fraction written in a form where an integer is used to represent the wholes and the remaining portion is written as a fraction. Recall that fractions can be thought of as unresolved integer division. For example, the fraction `{kt} \frac{15}{4}` is equivalent to the division `{kt} 15 \div 4`. Performing `{kt} 15 \div 4` results in a quotient of `{kt} 3R3` (3 wholes with 3 remaining pieces). As such, `{kt} 15 \div 4` can be written as the mixed number `{kt} 3 \frac{3}{4}`.

   ```{note}
   Don't get confused -- the mixed number `{kt} 3 \frac{3}{4}` !!means!! `{kt} 3 + \frac{3}{4}`, it does not !!mean!! `{kt} 3 \cdot \frac{3}{4}` (multiplication).
   ```

 * `{bm} number line` - A type of diagram used to visualize the value that a number represents. It consists of a straight horizontal line with equidistant vertical notches spliced through out, where each notch is labelled with incrementally larger numbers from left-to-right...

   ```{svgbob}
   |---|---|---|---|---|---|---|---|---|
   0   1   2   3   4   5   6   7   8   9
   ```

   The number being represented is marked on the line. For example, to represent the number 5...

   ```{svgbob}
                       5
                       |
                       v
   |---|---|---|---|---|---|---|---|---|
   0   1   2   3   4   5   6   7   8   9
   ```

 * `{bm} addition/(addition|add|sum)/i` - Combining the values of two numbers. For example, combining 3 items and 5 items together results in 7 items...

   ```
    [●●●]    [●●●●●]
      3         5
   
   group values together
   
      [●●●●●●●●]
          7
   ```

* `{bm} subtraction/(subtraction|subtract)/i` - Removing the value of one number from another number. For example, removing 3 items from 5 items results in 2 items...

  ```
      [●●●●●]
         5
  
  pick out 3 from the 5
  
     [●●] [●●●]
      2     3
  ```

 * `{bm} multiplication/(multiplication|multiply|product|multiplier|multiplicand)/i` - Iteratively adding a number to itself for a certain number of iterations.

   ```
   3+3+3+3+3=15
   
    [●●●] 3
    [●●●] 3
    [●●●] 3
    [●●●] 3
    [●●●] 3
   ```

   The output of a multiplication operation is called the product. In the example above, 15 is the product.

   The inputs into the multiplication operation are either...

    * called factors: In the example above, 3 and 5 are the factors,
    * the first input is called the multiplier and the second input is called the multiplicand: In the example above, 3 is the multiplier and 5 is the multiplicand.

 * `{bm} division/(division|divide|remainder|quotient|dividend|divisor)/i` - Iteratively subtracting a number by another number to find out how many iterations can be subtracted. For example, 15 can be subtracted by 3 exactly 5 iterations before nothing's left...

   ```
    [●●●●●●●●●●●●●●●] start with 15
   
    [●●●●●●●●●●●●] 15-3=12 (iteration 1)
    [●●●●●●●●●] 12-3=9 (iteration 2)
    [●●●●●●] 9-3=6 (iteration 3)
    [●●●] 6-3=3 (iteration 4)
    [] 3-3=0 (iteration 5)
   ```

   Another way of thinking about division is that it's chopping up a number. Imagine cutting up a pie into 15 pieces and eating 3 pieces at a time. The pie will be done after you've eaten 5 times.

   The output of a division operation is called the quotient. In the example above, the quotient is 5 (it subtracts 5 times).

   The inputs into the division operation are called the dividend and divisor. In the example above, 15 is the dividend and 3 is the divisor.

    * `{kt} dividend \div divisor = quotient`
    * `{kt} dividend / divisor = quotient`
    * `{kt} \frac{dividend}{divisor} = quotient`

   ```{note}
   One way to think of this is that the dividend (the number on the left / top) is the starting value, and the divisor is the number being iteratively subtracted.
   
   The quotient is the number of times you can subtract.
   ```

   In certain cases, division may result in some remaining value that isn't large enough for another subtraction iteration to take place. This remaining value is called the remainder. For example, 16 can be subtracted by 3 for 5 iterations but will have a remainder of 1...

   ```
    [●●●●●●●●●●●●●●●●] start with 16
   
    [●●●●●●●●●●●●●] 16-3=13 (iteration 1)
    [●●●●●●●●●●] 13-3=10 (iteration 2)
    [●●●●●●●] 10-3=7 (iteration 3)
    [●●●●] 7-3=4 (iteration 4)
    [●] 4-3=1 (iteration 5)
   
    only 1 item left -- not enough for another subtraction iteration
    
    1 is the remainder
   ```

 * `{bm} multiple` - Given integer numbers n and m (use the letters as placeholders for some arbitrary integer numbers). m is a multiple of n if some integer exists such that `{kt} n \cdot ? = m`. For example, the multiples of 2 are...

   * 2*0=2 -- 0 is a multiple of 2
   
   * 2*1=2 -- 2 is a multiple of 2
   
     ```
     ┌──┐
     │●●│ 2 can be grouped as 1 group of 2
     └──┘
     ```
   
   * 2*2=4 -- 4 is a multiple of 2
   
     ```
     ┌──┬──┐
     │●●│●●│ 4 can be grouped as 2 groups of 2
     └──┴──┘
     ```
   
   * 2*3=6 -- 6 is a multiple of 2
   
     ```
     ┌──┬──┬──┐
     │●●│●●│●●│ 6 can be grouped as 3 groups of 2
     └──┴──┴──┘
     ```
   
   * 2*4=8 -- 8 is a multiple of 2
   
     ```
     ┌──┬──┬──┬──┐
     │●●│●●│●●│●●│ 8 can be grouped as 4 groups of 2
     └──┴──┴──┴──┘
     ```
   
   * etc..
   
   A number like 7 wouldn't be a multiple of 2 because there is no integer that can be multiplied by 2 to get 7 -- 2\*3.5=7, but 3.5 isn't an integer.
   
   ```
   ┌──┬──┬──┬─┐
   │●●│●●│●●│●│ 7 can't be grouped as groups of 2 (last group only has 1)
   └──┴──┴──┴─┘
   ```

 * `{bm} divisible` - Given integer numbers d and n (use the letters as placeholders for some arbitrary integer numbers). d is divisible by n if `{kt} d \div n` has a remainder of 0. For example, 8 is divisible by...

   * 8/1=8 -- 8 is divisible by 1
   
     ```
     ┌────────┐
     │●●●●●●●●│ 8 can be grouped as 1 group of 8
     └────────┘
     ```
   
   * 8/2=4 -- 8 is divisible by 2
   
     ```
     ┌────┬────┐
     │●●●●│●●●●│ 8 can be grouped as 2 groups of 4
     └────┴────┘
     ```
   
   * 8/4=2 -- 8 is divisible by 4
   
     ```
     ┌──┬──┬──┬──┐
     │●●│●●│●●│●●│ 8 can be grouped as 4 groups of 2
     └──┴──┴──┴──┘
     ```
   
   * 8/8=1 -- 8 is divisible by 8
   
     ```
     ┌─┬─┬─┬─┬─┬─┬─┬─┐
     │●│●│●│●│●│●│●│●│ 8 can be grouped as 8 groups of 1
     └─┴─┴─┴─┴─┴─┴─┴─┘
     ```
   
   In all of the above cases, there is no remainder. 8 wouldn't be divisible by a number like 3 because there would be a remainder. 8/3=2R2.
   
   ```
   ┌───┬───┬──┐
   │●●●│●●●│●●│ 8 can't be grouped as groups of 3 (last group only has 2)
   └───┴───┴──┘
   ```
   
   ```{note}
   The phrases evenly divisible, evenly divides, and divisible all !!mean!! the same thing.
   ```
   
   ```{note}
   Divisible and multiple refer to the same idea. Saying that 275 is a multiple of 5 (`{kt} 5\cdot?=275`) is the same as saying 275 is divisible by 5 (`{kt} 275\div5=?`).
   ```

 * `{bm} factor` - Given a whole number x, the whole number f is its factor if x is divisible by f: x divided by f results in no remainder. For example, the factors of 32 are...

   * 32/1=32R0
   * 32/2=16R0
   * 32/4=8R0
   * 32/8=4R0
   * 32/16=2R0
   * 32/32=1R0

   ... 1, 2, 4, 8, 16, and 32. The factors for any number will always be between 1 and that number (inclusive). 

   ```{note}
   Shouldn't negative integers also be factors? e.g. 32=-1*-32. It turns out that for positive integers, negative factors aren't included? For negative integers, they are. Factoring negative integers is discussed further below in this section.
   
   See https://math.stackexchange.com/a/404789
   ```

 * `{bm} prime` - A counting number with only two factors (1 and itself). Examples of prime numbers: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, and 47.

 * `{bm} composite` - A counting number with more than 2 factors. Examples of composite numbers: 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, and 20.

 * `{bm} prime factorization/(prime factorization|prime factor|factor tree)/i` - The process of breaking down a composite number into a product of primes. Every composite number can be written as a product of prime numbers. For example...

   * 12 = 3\*2\*2
   * 16 = 2\*2\*2\*2
   * 21 = 3\*3\*3

 * `{bm} least common multiple` `{bm} /(LCM)/` - The process of taking 2 numbers and finding the smallest multiple between them. That is, if you listed out their multiples starting from 1, the first match between them would be the least common multiple.

 * `{bm} greatest common divisor/(greatest common divisor|highest common divisor|largest common divisor|greatest common factor|highest common factor|largest common divisor)/i` `{bm} /(GCD|HCF)/i` - The process of taking 2 numbers and finding the largest possible divisor between the two of them. That is, finding the greatest number that evenly divides both numbers.

   ```{note}
   This is also referred to as the highest common factor -- you're finding the largest factor that's common in both of them. Common factors between the numbers will evenly divide both numbers.
   ```

 * `{bm} positive/(positive|negative)/i` - Numbers may be mirrored across 0, where everything to the ...

   * right of 0 is called a positive number (signified by a + prefix, called a sign)
   * left of 0 is called a negative number (signified by a - prefix, called a sign)
   
   ```{svgbob}
   <--+----+----+----+----+----+----+----+----+-->
      |    |    |    |    |    |    |    |    | 
     -4   -3   -2   -1    0   +1   +2   +3   +4
   ```
 
   Conceptually, you can think of the positives the same way you think about natural numbers. They represent some value. For each positive, there's a corresponding negative that represents the opposite of that positive value. For example, if...

   * positive integers represent steps forward, then negative integers would represent steps backward.

     * walk 5 steps (go forward 5 steps)
     * walk -5 steps (go backward 5 steps)
   
     ```{svgbob}
     <--+-------------------------+-------------------------+-->
        |                         |                         | 
       -5                         0                        +5
     5 feet backward         no movement         5 feet forward
     ```
   
   * positive integers represent money gained, then negative integers would represent money owed or spent.
   
     * 5 dollars (gain $5)
     * -5 dollars (spend $5, or be in debt $5)
   
     ```{svgbob}
     <--+-------------------------+-------------------------+-->
        |                         |                         | 
       -5                         0                        +5
     5 dollar debt              broke           5 dollars gained
     ```
   
   * positive integers represent depth below sea-level, then negative integers would represent elevation above sea-level.
   
     * depth of 5 meters (5 meters below sea-level)
     * depth of -5 meters (5 meters above sea-level)
   
   
     ```{svgbob}
     ^
     |
     +- -5 meters deep (5 meters above sea-level)
     |
     |
     |
     +- 0, sea-level
     |
     |
     |
     +- 5 meters deep (5 meters below sea-level)
     |
     v
     ```

 * `{bm} sign` - A prefix that determines if a number is positive or negative. All numbers other than 0 have a sign. 0 represents nothing / no value, which is why it doesn't have a sign (it's used as a separation point between the positive and negative numbers).

   If a number (other than 0) is positive, the convention is to leave the + sign is typically left out.

 * `{bm} decimal number/(decimal number|decimal point)/i` - Another way of representing a mixed number where the denominator of the fraction is 1 followed by 0s. For example, ...

   * `{kt} 2 \frac{0}{1}` ↔ 2.0
   * `{kt} 2 \frac{9}{10}` ↔ 2.9
   * `{kt} 2 \frac{9}{100}` ↔ 2.09
   * `{kt} 2 \frac{9}{1000}` ↔ 2.009

   The period placed in between the whole and the fraction is called a decimal point. The number to the ...

   * left of the decimal point is referred to as the wholes.
   * right of the decimal point is referred to as the fractional.

   A mixed number can be converted to a decimal number so long as it has a suitable denominator: 1 followed by zero or more 0s. For example, `{kt} 2 \frac{1}{10}` has a suitable denominator but `{kt} 2 \frac{1}{2}` doesn't.

   If the denominator isn't suitable, the mixed number may still be convertible so long as an equivalent fraction exists that does have a suitable denominator. In the previous example, `{kt} 2 \frac {5}{10}` is an equivalent fraction to `{kt} 2 \frac{1}{2}`.

 * `{bm} average` / `{bm} mean/(mean)_ST/i` - The "typical" number in a list of numbers. Numbers in the list are summed together, then the result is divided by the count of numbers in that list. For example, to average of [1, 2, 3] is 2: 1+2+3 = 6, then 6 / 3 = 2.
    
   `{bm-error} Wrap in !! or apply suffix _ST/\mean/i`

 * `{bm} median` - The middle number in a sorted list of numbers. Numbers in the list that come ...
 
   * before the median should be less than the median.
   * after the median should be greater than the median.

   When the count of numbers in the list is odd, there is a middle number. For example, the median of [55, 57, 58, 59, 70] is 58.

   When the count of numbers in the list is even, there is no middle number. The median of a list with an even count is the two numbers closest to the middle averaged together. For example, the median of [3, 5, 6, 7, 9, 10] is the average of 6 and 7: 6.5.

 * `{bm} mode` - The number that appears most often in a list of numbers. For example, the mode of [5, 5, 6, 7, 8, 8, 8, 10] is 8, because 8 appears the most often in the list.

   Some lists may have multiple modes. For example, the mode of [1, 5, 5, 6, 6, 8] is both 5 and 6, because 5 and 6 appear the same amount of times, and that amount is more often than any other number in that list.

 * `{bm} frequency` - A count of how often some number occurs. For example, in the list [1, 5, 5, 6, 6, 8], ...

   * 8 has a frequency of 1.
   * 6 has a frequency of 2.
   * 5 has a frequency of 2.
   * 1 has a frequency of 1.

 * `{bm} probability/(probability|probabilities)/i` - A number describing how likely it is for a desired outcome to occur in some scenario.Probability is calculated as the number of desired outcomes over the number of total outcomes: `{kt} \frac{desired}{total}`. The result is a number between 0 and 1, where 0 !!means!! never happens and 1 !!means!! always happens.
 
   For example, a bowl of marbles has 6 red marbles and 1 blue marble. Without looking, selecting a blue marble from the bowl has a probability of `{kt} \frac{1}{7}`. The desired outcome is selecting a blue marble (1 marble is blue) divided by the total number of marbles in the bowl (7 marbles total).

 * `{bm} ratio` - A comparison of two numbers representing measurements of the same unit (e.g. inches, lbs, US dollars, etc..), written as either a fraction `{kt} \frac{a}{b}` or in the form `{kt} a:b`. For example, in a bag of M&Ms, there are 30 red M&Ms to 20 blue M&Ms, !!meaning!! the ratio of red to blue is `{kt} \frac{30}{20}` or `{kt} 30:20`. The fraction, once simplified, is `{kt} \frac{3}{2}`, !!meaning!! for every 3 red M&Ms there are 2 blue M&Ms.

 * `{bm} rate` - A comparison of two numbers representing measurements of different units (e.g. inches, lbs, US dollars, etc..), written as a fraction `{kt} \frac{a}{b}`. For example, it costs $100 to fill up 2 Olympic sized swimming pool with water, !!meaning!! that the rate of money to water is `{kt} \frac{100}{2}`. The fraction, once simplified, is `{kt} \frac{50}{1}`, !!meaning!! it costs $50 to fill up each Olympic sized swimming pool.

 * `{bm} unit rate` - The rate `{kt} \frac{a}{b}`, but normalized such the rate only considers a single unit of the second measurement. For example, it costs $100 to fill up 2 Olympic sized swimming pool with water, !!meaning!! that the rate of money to water is `{kt} \frac{100}{2}`. Once converted to a unit rate, it becomes $50 to fill up each Olympic sized swimming pool.

   To figure out the unit rate, simply convert the fraction to a decimal (divide its numerator by its denominator).

 * `{bm} square` - Power of two. For example, 5 squared is `{kt} 5^2`.

 * `{bm} cube` - Power of three. For example, 5 cubed is `{kt} 5^3`.

 * `{bm} real number` - A decimal number whose fractional part can be arbitrarily small. There's no limit to how small it can get.

   Real numbers include counting numbers, whole numbers, integer numbers, rational numbers, and irrational numbers.

   ```{svgbob}
   +----------------------------------------------------------------------------------+
   |                                                                                  |
   |                                      Real                                        |
   |                                                                                  |
   |   +-+-+-+------------------------------+   +---------------------------------+   |
   |   | | | |                              |   |                                 |   |
   |   | | | |   "Counting (e.g. 1, 7, 21)" |   |                                 |   |
   |   | | | |                              |   |                                 |   |
   |   | | | +------------------------------+   |                                 |   |
   |   | | |                                |   |                                 |   |
   |   | | |   "Whole (e.g. 0, 1, 7, 21)"   |   |                                 |   |
   |   | | |                                |   |                                 |   |
   |   | | +--------------------------------+   | "Irrational (e.g. pi, sqrt(2))" |   |
   |   | |                                  |   |                                 |   |
   |   | |   "Integer (e.g. -7, -19, -471)" |   |                                 |   |
   |   | |                                  |   |                                 |   |
   |   | +----------------------------------+   |                                 |   |
   |   |                                    |   |                                 |   |
   |   |   "Rational (e.g. -0.5, 1/3, 1.2)" |   |                                 |   |
   |   |                                    |   |                                 |   |
   |   +------------------------------------+   +---------------------------------+   |
   +----------------------------------------------------------------------------------+
   ```

 * `{bm} whole number` - Numbers that begin at 0 and increment by 1. Whole numbers only consist of wholes (no non-complete parts of wholes): For example, 0, 1, 2, 3, ... are whole numbers while 2.2 is not.
 
 * `{bm} counting number/(natural number|counting number|cardinal number)/i` - Numbers that begin at 1 and increment by 1. For example, 0, 1, 2, 3, ... are whole numbers while 0 and 2.2 are not.
  
    Counting numbers start where you start counting / where set of something has at least one element. For example, if you're counting apples, you start counting at 1. There needs to be at least 1 apple to start.
 
 * `{bm} integer number/(integer number|integer)/i` - 2 sets of counting numbers separated by 0, where everything to the...
 
   * right of 0 is called a positive number (signified by a + prefix)
   * left of 0 is called a negative number (signified by a - prefix)
   
   ```{svgbob}
   <--+----+----+----+----+----+----+----+----+-->
      |    |    |    |    |    |    |    |    | 
     -4   -3   -2   -1    0   +1   +2   +3   +4
   ```

 * `{bm} rational number` - 

 * `{bm} irrational number` - 


`{bm-ignore} !!([\w\-]+?)!!/i`

TODO: add two terms above

TODO: continue from 5.7 - continue from definition of square (above)

TODO: continue from 5.7 - continue from definition of square (above)

TODO: continue from 5.7 - continue from definition of square (above)


TODO: ADD DEFINITIONS HERE - real / whole / decimal / etc..

TODO: move basic terminology from pre-algebra

