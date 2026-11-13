```{toc}
```

# Review


# Terminology

* `{bm} polynomial function/(polynomial function|polynomial)/i` - A function in the form `{kt} a_nx^n+a_{n-1}x^{n-1}+...+a_2x^2+a_1x^1+a_0x^0`, where n is a non-negative integer and `{kt} a_n,...,a_2,a_1,a_0` are referred to as the coefficients of the polynomial. 

  The form shown above for a polynomial simplifies to `{kt} a_nx^n+a_{n-1}x^{n-1}+...+a_2x^2+a_1x+a_0` (last two terms simplified).
  
  A polynomial's ...
  
  * domain is all real numbers.
  * degree_POLY is the highest exponent across all terms that have a coefficient other than 0.

* `{bm} degree/(degrees?)_POLY/i` - Highest exponent across all terms of a polynomial that have a coefficient other than 0. For example, ...

  * `{kt} f(x)=10x^2+3` has a degree_POLY of 2.
  * `{kt} f(x)=0x^4+3x` has a degree_POLY of 1.
  * `{kt} f(x)=0x^4+3` has a degree_POLY of 0.

  A polynomial function of degree_POLY ...

  * 1 is called a linear function.
  * 2 is called a quadratic function.
  * 3 is called a cubic function.

* `{bm} root/(roots?)_POLY/i` - Given a polynomial `{kt} P(x)`, its roots_POLY are x values where `{kt} P(x)=0`. If you were to graph `{kt} P(x)`, the roots_POLY would be values of x that touch the x-axis.

  ```{note}
  Roots_POLY can be thought of as factors? If a polynomial's root_POLY is x=0.5, then it should have the factor (2x-1)?
  ```

* `{bm} product-sum factoring/(product[-\s]sum factoring)/i` - A process that factors a quadratic `{kt} ax^2+bx+c` by finding two numbers r and s that when ...

  * added, `{kt} ar+s=b`.
  * multiplied, `{kt} rs=c`.

  `{kt} ax^2+arx+sx+rs = ax(x+r)+s(x+r) = (ax+s)(x+r)`

  Factoring quadratics is useful for finding their roots_POLY (where x=0 / where they touch x-intercepts) as well as for algebraic manipulations such as simplifying.

  ```{note}
  You often see explained online for the special case where a=1: `{kt} x^2+bx+c`, which means you're trying to find two numbers r and s where `{kt} r+s=b` and `{kt} rs=c`...
  
   * added, equal b: `{kt} r+s=b`.
   * multiplied, equal c: `{kt} rs=c`.
  
  `{kt} x^2+rx+sx+rs = x(x+r)+s(x+s) = (x+r)(x+s)`.
  ```

* `{bm} complete the square/(complete the square|completing the square)/i` - A technique for converting a quadratic in the form `{kt} ax^2+bx+c` into the form `{kt} a(x-h)^2+k`. To complete the square for a `{kt} ax^2+bx+c`, begin by pulling out a from first two terms: `{kt} a(x^2+\frac{b}{a}x)+c`.

  Then, rewrite the inner group `{kt} x^2+\frac{b}{a}x` to be in the form `{kt} (x+s)^2`. To do this, a constant term needs to be added to the inner group such that it can be factored. `{kt} (x+s)^2` expands out to `{kt} x^2+2sx+s^2`, meaning the constant term should map to `{kt} s^2`.
  
  To determine what s should be for the inner group, use algebra. It's known that the ...
  
   * inner group's middle term `{kt} \frac{a}{b}` maps to `{kt} 2sx`.
   * inner group's constant term should map to `{kt} s^2`.
  
  ```{kt}
  \frac{b}{a}x = 2sx
  \frac{b}{a} = 2s
  \frac{b}{2a} = s
  ```
  
  Since `s = \frac{b}{2a}`, adding `{kt} \frac{b}{2a}^2` to the inner group makes it factorable into the form `{kt} (x+s)^2`: `{kt} a(x^2+\frac{b}{a}x+\frac{b}{2a}^2)+c`. However, the problem with adding this term to the inner group is that the overall expression is now different from the original: `{kt} a(x^2+\frac{b}{a}x)+c \neq a(x^2+\frac{b}{a}x+\frac{b}{2a})+c`. A quantity of `{kt} a(\frac{b}{2a}^2)` has been added in, and so that same quantity needs to be removed: `{kt} a(x^2+\frac{b}{a}x)+c = a(x^2+\frac{b}{a}x+\frac{b}{2a}^2)+c-a(\frac{b}{2a}^2)`.
  
  For example, to complete the square for `{kt} 2x^2-12x+11` ...
  
   * pull out a from first two terms: `{kt} 2(x^2-6x)+11`.
   * add and remove quantity to make factorable: `{kt} 2(x^2-6x+9)+11-18`.
   * factor inner group to `{kt} (x+s)^2` form: `{kt} 2(x-3)^2+11-18`.
   * add together constant terms: `{kt} 2(x-3)^2-7`.
  
  Completing the square is useful because it makes explicit the translation and scaling applied to `{kt} x^2`. For example, completing the square of `{kt} 2x^2+8x+6` results in `{kt} 2(x+2)^2-2`, which is `{kt}x^2` shifted left by 2 and down by 2, and compressed horizontally by half.

  ```{calculus}
  Graph
  funcs: [x^2, 2*(x+2)^2-2]
  x_lim: [-12, 12]
  y_lim: [-12, 12]
  fig_size: [4, 4]
  ```

  ```{note}
  Note that this is completing the square, not factor. Factoring will tell you the roots_POLY (where it crosses the x-axis): `{kt} (2x+6)(x+1)` crosses the x-axis as -3 and -1.
  ```
  
  ```{note}
  The material also mentions that this is useful for integrating rational functions.
  ```

* `{bm} quadratic formula` - The quadratic formula determines the x-intercepts of a quadratic (where `{kt} ax^2+bx+c=0`, as in where the quadratic evaluates to 0, also called roots_POLY): `{kt} x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}`. For example, the quadratic `{kt} 2x^2-7x-4` has the x-intercepts `{kt} x=\frac{-(-7)\pm\sqrt{(-7)^2-4(2)(-4)}}{2(2)}=\frac{7\pm\sqrt{81}}{4}=\frac{7\pm9}{4}=\{-0.5,4\}`.

  `{kt} b^2-4ac` is referred to as the discriminant, and can be used to determine the number of real numbered roots_POLY that a quadratic has.
  
  The quadratic formula is derived by completing the square:
  
  ```{kt}
  ax^2+bx+c=0 \\
  \\
  ax^2+bx=-c \\
  \\
  x^2+\frac{b}{a}x=\frac{-c}{a} \\
  \\
  x^2+\frac{b}{a}x+(\frac{b}{2a})^2=\frac{-c}{a}+(\frac{b}{2a})^2 \\
  \\
  (x+\frac{b}{2a})^2=\frac{-c}{a}+(\frac{b}{2a})^2 \\
  \\
  (x+\frac{b}{2a})^2=\frac{-c}{a}+\frac{b^2}{4a^2} \\
  \\
  (x+\frac{b}{2a})^2=\frac{-4ac}{4a^2}+\frac{b^2}{4a^2} \\
  \\
  (x+\frac{b}{2a})^2=\frac{-4ac+b^2}{4a^2} \\
  \\
  (x+\frac{b}{2a})^2=\frac{b^2-4ac}{4a^2} \\
  \\
  x+\frac{b}{2a}=\pm\sqrt(\frac{b^2-4ac}{4a^2}) \\
  \\
  x=\pm\sqrt(\frac{b^2-4ac}{4a^2})-\frac{b}{2a}
  ```
  
  ```{note}
  The completing the square step is from step 2 to 3.
  ```

* `{bm} discriminant` - The expression `{kt} b^2-4ac` within the quadratic formula. When the discriminant is ...

  * `{kt} b^2-4ac > 0`, there are two real root_POLYs.
  * `{kt} b^2-4ac = 0`, there's one real root_POLY.
  * `{kt} b^2-4ac < 0`, there's no real root_POLY.

* `{bm} binomial theorem` - A formula to quick expansion of expressions in the form `{kt} (a+b)^n` where k is a positive integer: `{kt} (a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k`.

  ```{note}
  `{kt} \binom{n}{k}` is "k choose n", something covered in statistics / probability theory / combinatorics. For now, just know `{kt} \binom{n}{k} = \frac{n!}{k!(n-k)!}`.
  ```

  For example, ...

  * `{kt} (a + b)^2 = a^2+2ab+b^2`
  * `{kt} (a + b)^3 = a^3+3a^2b+3ab^2+b^3`
  * `{kt} (a + b)^4 = a^4+4a^3b+6a^2b^2+4ab^3+b^4`
  * etc..

* `{bm} difference of squares` - Quadratic expressions that follow the pattern `{kt} a^2-b^2`. Difference of squares factor as `{kt} a^2-b^2 = (a-b)(a+b)`.

* `{bm} difference of cubes` - Cubic expressions that follow the pattern `{kt} a^3-b^3`. Difference of cubes factor as `{kt} a^3-b^3 = (a-b)(a^2+ab+b^2)`.

* `{bm} sum of cubes` - Cubic expressions that follow the pattern `{kt} a^3+b^3`. Sum of cubes factor as `{kt} a^3+b^3 = (a+b)(a^2-ab+b^2)`.

* `{bm} polynomial division` - A process that breaks a polynomial into two factors, given that one of the factors is already known. The process works similarly to long division in that you're dividing the polynomial by that known factor to determine the other factor. For example, consider the polynomial `{kt} 2x^3+x^2-6x-8`. If you already know that `{kt} (x-2)` is a factor, you can divide the polynomial by that known factor to determine the other factor:

  ```
                 2x^2  + 5x  + 4
      .-------------------------
  x-2 |    2x^3 +  x^2 -  6x - 8
        - (2x^3 - 4x^2)
  	    -------------
  		        5x^2 -  6x
  			 - (5x^2 - 10x)
  			   ------------
  			            4x - 8
  				     - (4x - 8)
  					  ---------
  					         0
  ```
  
  ```{note}
  Note what's happening here. The first term in the quotient is `{kt} 2x^2` because when you multiply it by the divisor `{kt} (x-2)` it results in `{kt} 2x^3+x^2`. Subtracting `{kt} 2x^3+x^2` from the dividend completely eliminates the 2x^3 from the dividend.
  
  This same process continues for each term in the quotient.
  ```
  
  In the example, polynomial division determined that the other factor is `{kt} 2x^2+5x+4`. That is, `{kt} (x-2)(2x^2+5x+4)=2x^3+x^2-6x-8`. The other factor can then go on to be factored again by some other method (or potentially the same method), assuming it's factorable.
  
  For polynomial division to work, you must already know one of the polynomial's factors. If you don't already have a starting factor, there are multiple ways to find one:
  
   * Graphing calculator: Try using a graphing calculator to see if you can find one of the roots_POLY. The roots_POLY are values of x where the graph touches or crosses the x-axis.
  
   * Trial-and-error: Try plugging values for x into the polynomial until one evaluates to 0. For example, `{kt} 2x^3+x^2-6x-8` when ...
  
     * x=0 evaluates to -8
     * x=1 evaluates to -11  
     * x=2 evaluates to 0 
  
     When x=2, the polynomial evaluates to 0, meaning `{kt} (x-2)` is a factor.
  
   * Rational root theorem: Assuming `{kt} P(x)` is a polynomial with integer coefficients, a root_POLY of the equation `{kt} P(x)=0` can be expressed in the form `{kt} \frac{p}{q}`, where ...
   
     * p is a factor of the constant term.
     * q is a factor of the leading coefficient.
   
     In other words, you can find a factor by testing all possible `{kt} \frac{p}{q}` to see if it's a root_POLY / factor of the polynomial.
  
  You can use the methods described above to iteratively pull out roots_POLY using polynomial division until the entire polynomial is factored. For example, ...
  
  1. use rational root theorem to determine `(x-2)` is a factor of `{kt} x^3-3x^2-10x+24`.
  2. use polynomial division to factorize `{kt} x^3-3x^2-10x+24` to `{kt} (x-2)(x^2-x-12)`.
  3. use rational root theorem to determine `(x-4)` is a factor of `{kt} x^2-x-12`.
  4. use polynomial division to factorize `{kt} x^2-x-12` to `{kt} (x-2)(x-4)`.
  
  `{kt} x^3-3x^2-10x+24 = (x-2)(x-2)(x-4)`.

* `{bm} Rational root theorem` - A theorem that states a root_POLY of the polynomial equation `{kt} P(x)=0` can be expressed in the form `{kt} \frac{p}{q}` (assuming `{kt} P(x)` is a polynomial with integer coefficients), where ...
 
  * p is a factor of the constant term.
  * q is a factor of the leading coefficient.
 
  In other words, you can find a factor by testing all possible `{kt} \frac{p}{q}` to see if it's a root_POLY / factor of the polynomial. For example, the polynomial `{kt} P(x)=2x^3+x^2-6x-8` has ...

  * constant term factors p={-8,-6,-4,-2,-1,1,2,4,6,8}.
  * leading coefficient factors q={1,2}.

  Testing possible `{kt} \frac{p}{q}` within `{kt} P(x)` shows that `{kt} \frac{4}{2}=2` is a root_POLY: `{kt} P(2) = 0`. Since `{kt} 2` is a root_POLY, `{kt} (x-2)` is a factor.

  `{bm-error} Remove _POLY from the word root/(rational root_POLY theorem)/i`

* `{bm} function` - A mapping between two sets I and O, where each element in I maps to _exactly one_ element in set O. A function is written in the format `{kt} f(x)`, where ...

  * f is the name of the function.
  * x is an element in set I.
  * `{kt} f(x)` is an element in set O (the element corresponding to x).

  ```{note}
  `{kt} f(x)` is typically spoken "f of x".
  ```

  If the mapping performed by the function is a mathematical expression, that expression is typically written alongside the function: `{kt} f(x)=x^2`. Not all functions are representable as an expression. For example, a function that maps time to a company's stock price typically isn't representable as an expression (but it may be approximated using an expression, called a mathematical model).

  * The set I is referred to as the function's domain. For example, in `{kt} f(x)=\frac{1}{x}`, the domain is all real numbers except 0 because division by 0 isn't a valid and so the function has no output (no corresponding element in set O).
  * The set O is referred to as the function's range. For example, in `{kt} f(x)=x^2`, the range is all real numbers >=0 because there is no element in set I will produce a negative output.

  A function can be thought of as a mapping (as described above) or as a machine that transforms inputs. As long as the input is in the domain of that function, then the machine accepts it and produces an output. For example, the function `{kt} g(x)=\frac{1}{x}` can be thought of as a machine named g, which takes in an input named x and produces an output named `{kt} g(x)`. 

  ```{svgbob}
           .-------.
       ----'       '----
  x ---->      g      ----> "g(x)"
       ----.       .----
	       '-------'
  ```

* `{bm} domain` - The set of all of valid inputs for a function. For example, in `{kt} f(x)=\frac{1}{x}`, the domain is all real numbers except 0 because division by 0 isn't a valid and so the function has no output (no corresponding element in set O).

  Some functions explicitly state domain. If a function is mapped as an expression and its domain isn't explicitly stated, such as in the example above, the convention is that its domain is the set of all *real numbers* for which the expression evaluates to a *real number*. For example, `{kt} f(x)=\sqrt{x-2}` has the domain `{kt} x \ge 2` because `{kt} x < 2` would result in a negative number being fed into the square root, resulting in an imaginary number rather than a real number.

* `{bm} range` - The set of all valid outputs for a function. For example, in `{kt} f(x)=x^2`, the range is all real numbers >= 0 because there is no element in set I will produce a negative output.

* `{bm} independent variable` - A symbol that represents some value in a function's domain. For example,  x in `{kt} a=x^2` is an independent variable. In other words, a depends on x, making x the independent variable and a the dependent variable.

  ```{note}
  Normally the function would be written as `{kt} f(x)=x^2`, but f(x) is replaced with a to illustrate the point?
  ```

* `{bm} dependent variable` - A symbol that represents some value in a function's range. For example, a in `{kt} a=x^2` is a dependent variable. In other words, a depends on x, making x the independent variable and a the dependent variable.

  ```{note}
  Normally the function would be written as `{kt} f(x)=x^2`, but f(x) is replaced with a to illustrate the point?
  ```

* `{bm} mathematical model` - An approximation of a real-world phenomenon, often by means of a function or equation, used to understand or make predictions about that phenomenon. For example, imagine a device monitoring the growth of bacteria within a petri dish. The device captures the number of bacterial cells within the dish, every hour, over a 4 hour duration:

  | t | cell count |
  |---|------------|
  | 1 | 1010       | 
  | 2 | 3990       |
  | 3 | 9022       |
  | 4 | 15981      |

  The growth of bacteria over time may be approximated using the mathematical model `{kt} g(t)=1000t^2`.

  The process of building a mathematical model typically involves identifying the dependent variables, identifying independent variables, formulating the model (e.g. devising a function or equation), and testing the model against measurements of the real-world phenomenon.

* `{bm} empirical model` - A mathematical model based solely on collected data rather than physical laws / principles. Empirical models aim to find curves that follow the trend shown by the data, referred to as fit / fitting the data. 

* `{bm} interpolation` - Estimating a value between observations.

* `{bm} extrapolation` - Estimating a value before observations the first observation or after the last observation. In other words, estimating a value outside the window of observations.

* `{bm} vertical line test` - A test to determine if a curve (bendy line graphed on a 2D coordinate plane) is representable as a function. The test involves scanning a vertical line over the curve, checking to see if the vertical line ever intersects the curve more than once.

  The test assumes that the x-axis is the function's input and the y-axis is the function's output. More than one intersection with a vertical line means that there's a case where the function has 2 outputs for 1 input, which breaks the definition of a function: A function requires that each input have exactly one output.

  ```{svgbob}
  "Not representable as a function"         "Representable as a function"

              | /                                        | /  
              |/                                         |/   
          ----+----                                  ----+----
              |                                          |\   
              |                                          | \  
  ```

* `{bm} piecewise function/(piece[-\s]?wise function|piece[-\s]?wise defined function)/i` - A collection of functions combined together to form a single function, where each function in the collection is used for a different part of the parent function's domain.

  The notation for piecewise functions is to stack the collection of functions on top of each other, listing out the domain where each function is active. For example, the piecewise function below uses `{kt} 1-x` when `{kt} x \le -1` but `{kt} x^2` when `{kt} x > 1`

  ```{kt}
  f{x} = \begin{cases}
   1-x &\text{if } x \le -1 \\
   x^2 &\text{if } x > -1
  \end{cases}
  ```

  ```{note}
  Recall that a function maps exactly 1 output for each input, meaning that the domains can't intersect.
  ```

  ```{note}
  A piecewise function doesn't have to exhaustively list out its cases. It may have infintely many cases? See greatest integer function.
  ```

* `{bm} even function` - A function that reflects across the y-axis: `{kt} f(-x) = f(x)`. For example, `{kt} f(x)=x^2` and `{kt} f(x)=|x|` are both even functions.

  ```{svgbob}
    \ | /  
     \|/   
  ----+----
      |    
      |       
  ```

* `{bm} odd function` - A function that, when `{kt} x<0` reflects across both the x-axis and y-axis: `{kt} f(-x) = -f(x)`. For example, `{kt} f(x)=x^3` and `{kt} f(x)=x` is an even functions.

  ```{svgbob}
      | .-- 
      |/   
  ----+----
     /|    
  --' |       
  ```

* `{bm} increasing function/(increasing function|increasing)/i` - A function is said to be increasing across some interval `{kt} [x1, x2]` if `{kt} f(x_1) < f(x_2)` whenever `{kt} x_1 < x_2`. In other words, the function is increasing across an interval if the y-coordinate raises as the x-coordinate moves to the right.

  ```{svgbob}
  "f(x) increases between [A,B]"

      |     .--.
      |    /    \
      |   /      \
      |--'        '---
  ----+---------------
      |  A  B  C  D
      |       
  ```

* `{bm} decreasing function/(decreasing function|decreasing)/i` - A function is said to be decreasing across some interval `{kt} [x1, x2]` if `{kt} f(x_1) > f(x_2)` whenever `{kt} x_1 < x_2`. In other words, the function is decreasing across an interval if the y-coordinate as the x-coordinate moves to the right.

  ```{svgbob}
  "f(x) decreases between [C,D]"

      |     .--.
      |    /    \
      |   /      \
      |--'        '---
  ----+---------------
      |  A  B  C  D
      |       
  ```

* `{bm} difference quotient` - The expression `{kt} \frac{f(a+h)-f(a)}{h}`. It represents the average rate of change for f(x) between x=a and x=a+h.

* `{bm} step function` - A piecewise function that's finite and each interval is made up of a constant value. For example, ...

  ```{kt}
  f{x} = \begin{cases}
   1 &\text{if } 1 \le x \lt 11 \\
   2 &\text{if } 11 \le x \lt 21 \\
   3 &\text{if } 21 \le x \lt 31 \\
  \end{cases}
  ```

  ```{svgbob}
  3 |                    *----------o
    |
  2 |          *---------o
    |
  1 |*---------o
    |
    +---------------------------------
    0         10         20        30
  ```

  ```{seealso}
  Greatest integer function
  ```

* `{bm} linear function/(linear function|linear)/i` - A polynomial of degree_POLY 1. For example, `{kt} f(x)=10x+3` is a linear function.

  A linear function is the equation of a line written in slope-intercept form `{kt} y=f(x)=mx+b`. Linear functions grow at a constant rate. The rate of growth is dictated by the slope m. For example, `{kt} f(x)=10x+3` has a slope of 10, meaning whenever x increases by 1, `{kt} f(x)` increases by 10.

* `{bm} quadratic function/(quadratic function|quadratic)/i` - A polynomial of degree_POLY 2. For example, `{kt} f(x)=2x^2+4x+4` is a quadratic function.

* `{bm} cubic function/(cubic function|cubic)/i` - A polynomial of degree_POLY 3. For example, `{kt} f(x)=5x^3+2x^2+4x+4` is a cubic function.

* `{bm} power function/(power function|square root function|cube root function|root function|reciprocal function)/i` - A function in the form `{kt} x^a`, where a is a constant.

  * When `{kt} a=n`, where n is a positive integer, the power function is ...
  
    * an even function if n is even.
    * an odd function if n is odd.

    In both cases, as a gets larger, the graph of the power function gets flatter near the base (looks more and more squared off).

    <table><tr><td>
  
      ```{calculus}
      Graph
      funcs: [x^2, x^4, x^6]
      x_lim: [-3, 3]
      y_lim: [-3, 3]
      ```
  
    </td><td>
  
      ```{calculus}
      Graph
      funcs: [x^1, x^3, x^5, x^7]
      x_lim: [-3, 3]
      y_lim: [-3, 3]
      ```
    
    </td></tr></table>
    
    ```{note}
    x^0 is also an even function? It's just a horizontal line at 0.
    ```
  
  * When `{kt} a=\frac{1}{n}`, where n is a positive integer, the power function is sometimes also referred to as a root function: `{kt} x^{\frac{1}{n}} = \sqrt[n]{x}`. The graph is similar to `{kt} x^n` but rotated 90 !!degrees!! to the right.
  
    ```{calculus}
    Graph
    funcs: [x^(1/2), x^(1/4), x^(1/6)]
    x_lim: [-3, 3]
    y_lim: [-3, 3]
    ```

    ```{note}
    If `{kt} x^n` is even, its `{kt} \frac{1}{n}` counterpart will only show one half of the graph. This is because a function can only have 1 output for each input (1 y for each x -- if both halves are kept it'd violate the rules of a function).
    ```
  
    ```{note}
    There's some strangeness when n is odd and > 1. Desmos graphs things out similar to how the book has them graphed out, but for my grapher negative x values are returning complex numbers. Not sure how to handle it. Some discussion [here](https://www.reddit.com/r/learnpython/comments/egd3tt/cube_root_of_a_negative_number_returns_a_complex/).
    ```

  * When `{kt} a=-1`, the power function is sometimes also referred to as a reciprocal function: `{kt} x^{-1}=\frac{1}{x}`. The graph is a hyperbola with its asymptotes at x=0 and y=0.

    ```{calculus}
    Graph
    funcs: [x^-1]
    x_lim: [-3, 3]
    y_lim: [-3, 3]
    ```

  `{bm-error} Remove _POLY from the word root/(root_POLY function)/i`

* `{bm} algebraic function` - A function that can be constructed using algebraic operations (addition, subtraction, multiplication, division, powers, !!roots!!).

  All rational functions are algebraic functions.

* `{bm} rational function` - A function that's a ratio of two polynomials: `{kt} f(x) = \frac{P(x)}{Q(x)}`. The domain consists of all values where `{kt} Q(x) \neq 0`.

  All rational functions are algebraic functions.

* `{bm} periodic function/(periodic function|cyclic function)/i` - A function that repeats its values at regular intervals. For example, sine repeats every `{kt} 2\pi`: `{kt} sin(x+2\pi) = sin(x)`.

  ```{calculus}
  Graph
  funcs: [sin(x)]
  x_lim: [-15, 15]
  y_lim: [-1.1, 1.1]
  fig_size: [6, 2]
  ```

* `{bm} trigonometric function/(trigonometric function|trigonometry function|trig function)/i` - A function which relates an rangle within a right-triangle to the length of two of its sides:

  * sine / arcsine / cosecant
  * cosine / arccosine / secant
  * tangent / arctangent / cotangent.

  ```{svgbob}
          +
         /|
        / |
       /  |
  hyp /   | opp
     /    |
    /     |
   / a    |
  +-------+
      adj
  ```

  In calculus, the convention is to always use radians as opposed to !!degrees!!.

* `{bm} sine` - A trigonometric function that converts right-triangle's angle to the side-length ratio opposite vs hypotenuse: `{kt} sin(\theta)=\frac{opposite}{hypotenuse}`.

  ```{calculus}
  Graph
  funcs: [sin(x)]
  x_lim: [-15, 15]
  y_lim: [-1.1, 1.1]
  fig_size: [6, 2]
  ```

  * Domain: (-inf, inf)
  * Range: [-1, 1]
  * Period: `{kt} sin(x+2\pi) = sin(x)`
  * Inverse: Arcsine
  * Reciprocal: Cosecant
  * Relationships: `{kt} sin(x)=cos(\frac{\pi}{2}-x)=\frac{1}{csc(x)}`

  ```{note}
  The notation ...
  
  * `{kt} sin^k \space x` means `{kt} (sin(x))^k`, but it may mean `{kt} arcsin(x)` if `{kt} k=-1`: `{kt} sin^{-1} \space x`.
  * `{kt} sin \space x^k` means `{kt} sin(x^k)`.
  * `{kt} sin \space cx` means `{kt} sin(cx)`.
  ```

* `{bm} arcsine` - The inverse of sine: `{kt}arcsin(\frac{opposite}{hypotenuse})=\theta` vs  `{kt} sin(\theta)=\frac{opposite}{hypotenuse}`. In other words, arcsine swaps each of sine's (x, y) to (y, x) for where `{kt} \theta` is [-1, 1].

  ```{calculus}
  Graph
  funcs: [arcsin(x), sin(x)]
  x_lim: [-7, 7]
  y_lim: [-3.14, 3.14]
  fig_size: [6, 3]
  ```

  ```{note}
  * Any more than [-1, 1] and there'd be multiple y's for each x (violates definition of function).
  * For a right-triangle, `{kt} \frac{opposite}{hypotenuse}` can't go past (0, 1] anyways?
  ```

  `{kt} arcsin(r)` is sometimes written as `{kt} sin^{-1} \space r`.

  ```{note}
  The notation `{kt} sin^k \space x` means `{kt} (sin(x))^k`, but it may mean `{kt} arcsin(x)` if `{kt} sin^{-1} \space x`.
  ```

  ```{note}
  The notation ...
  
  * `{kt} arcsin^k \space x` means `{kt} (arcsin(x))^k`. Is there a special case for `{kt} k=-1`where `{kt} arcsin^{-1} \space x = sin(x)`?
  * `{kt} arcsin \space x^k` means `{kt} arcsin(x^k)`.
  * `{kt} arcsin \space cx` means `{kt} arcsin(cx)`.
  ```

* `{bm} cosecant` - The reciprocal of sine: `{kt} csc(\theta) = \frac{1}{sin(\theta)} = \frac{hypotenuse}{opposite}`
  
  ```{calculus}
  Graph
  funcs: [csc(x)]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  ```
  
  * Domain: `{kt} x \neq n \frac{pi}{2}`, where n is even
  * Range: (-inf, inf)
  * Period: `{kt} csc(x+2\pi) = csc(x)`
  * Reciprocal: Sine
  * Relationships: `{kt} csc(x)=sec(\frac{\pi}{2}-x)=\frac{1}{sin(x)}`

  ```{note}
  The notation ...
  
  * `{kt} csc^k \space x` means `{kt} (csc(x))^k`.
  * `{kt} csc \space x^k` means `{kt} csc(x^k)`.
  * `{kt} csc \space cx` means `{kt} csc(cx)`.
  ```

* `{bm} cosine` - A trigonometric function that converts right-triangle's angle to a side-length ratio adjacent vs hypotenuse: `{kt} cos(\theta) = \frac{adjacent}{hypotenuse}`.

  ```{calculus}
  Graph
  funcs: [cos(x)]
  x_lim: [-15, 15]
  y_lim: [-1.1, 1.1]
  fig_size: [6, 2]
  ```

  * Domain: (-inf, inf)
  * Range: [-1, 1]
  * Period: `{kt} cos(x+2\pi) = cos(x)`
  * Inverse: Arccosine
  * Reciprocal: Secant
  * Relationships: `{kt} cos(x)=sin(\frac{\pi}{2}-x)=\frac{1}{sec(x)}`

  ```{note}
  The notation ...
  
  * `{kt} cos^k \space x` means `{kt} (cos(x))^k`, but it may mean `{kt} arccos(x)` if `{kt} k=-1`: `{kt} cos^{-1} \space x`.
  * `{kt} cos \space x^k` means `{kt} cos(x^k)`.
  * `{kt} cos \space cx` means `{kt} cos(cx)`.
  ```

* `{bm} arccosine` - The inverse of cosine: `{kt}arccos(\frac{adjacent}{hypotenuse})=\theta` vs `{kt} cos(\theta) = \frac{adjacent}{hypotenuse}`. In other words, arcsine swaps each of cosine's (x, y) to (y, x) for where `{kt} \theta` is [-1, 1].

  ```{calculus}
  Graph
  funcs: [arccos(x), cos(x)]
  x_lim: [-7, 7]
  y_lim: [-3.14, 3.14]
  fig_size: [6, 3]
  ```

  `{kt} arccos(r)` is sometimes written as `{kt} cos^{-1} \space r`.

  ```{note}
  The notation `{kt} cos^k \space x` means `{kt} (cos(x))^k`, but it may mean `{kt} arccos(x)` if `{kt} cos^{-1} \space x`.
  ```

  ```{note}
  The notation ...
  
  * `{kt} arccos^k \space x` means `{kt} (arccos(x))^k`. Is there a special case for `{kt} k=-1` where `{kt} arccos^{-1} \space x = cos(x)`?
  * `{kt} arccos \space x^k` means `{kt} arccos(x^k)`.
  * `{kt} arccos \space cx` means `{kt} arccos(cx)`.
  ```

* `{bm} secant` - The reciprocal of cosine: `{kt} sec(\theta) = \frac{1}{cos(\theta)} = \frac{hypotenuse}{adjacent}`.

  ```{calculus}
  Graph
  funcs: [sec(x)]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  ```

  * Domain: `{kt} x \neq n \frac{pi}{2}`, where n is odd
  * Range: (-inf, inf)
  * Period: `{kt} sec(x+2\pi) = sec(x)`
  * Reciprocal: Cosine
  * Relationships: `{kt} sec(x)=csc(\frac{\pi}{2}-x)=\frac{1}{cos(x)}`

  ```{note}
  The notation ...
  
  * `{kt} sec^k \space x` means `{kt} (sec(x))^k`.
  * `{kt} sec \space x^k` means `{kt} sec(x^k)`.
  * `{kt} sec \space cx` means `{kt} sec(cx)`.
  ```

* `{bm} tangent` - A trigonometric function that converts right-triangle's angle to a side-length ratio opposite vs adjacent: `{kt} tan(\theta) = \frac{opposite}{adjacent}`.

  ```{calculus}
  Graph
  funcs: [tan(x)]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  ```

  * Domain: `{kt} x \neq n \frac{pi}{2}`, where n is odd
  * Range: (-inf, inf)
  * Period: `{kt} tan(x+\pi) = tan(x)`
  * Inverse: Arctangent
  * Reciprocal: Cotangent
  * Relationships: `{kt} tan(x)=\frac{sin(x)}{cos(x)}=cot(\frac{\pi}{2}-x)=\frac{1}{cot(x)}`

  ```{note}
  Why does `{kt} tan(x)=\frac{sin(x)}{cos(x)}`?
  
  1. `{kt} sin(x)=\frac{opp}{hyp}` <br>
     `{kt} hyp*sin(x)=opp`
  2. `{kt} cos(x)=\frac{adj}{hyp}` <br>
     `{kt} hyp*cos(x)=adj`
  3. `{kt} tan(x)=\frac{opp}{adj}` <br>
     `{kt} tan(x)=\frac{hyp*sin(x)}{hyp*cos(x)}` <br>
     `{kt} tan(x)=\frac{sin(x)}{cos(x)}`
  ```

  ```{note}
  The notation ...
  
  * `{kt} tan^k \space x` means `{kt} (tan(x))^k`, but it may mean `{kt} arctan(x)` if `{kt} k=-1`: `{kt} tan^{-1} \space x`.
  * `{kt} tan \space x^k` means `{kt} tan(x^k)`.
  * `{kt} tan \space cx` means `{kt} tan(cx)`.
  ```

* `{bm} arctangent` - The inverse of tangent: `{kt}arctan(\frac{opposite}{adjacent})=\theta` vs `{kt} tan(\theta) = \frac{opposite}{adjacent}`. In other words, arctangent swaps each of tangent's (x, y) to (y, x) for where `{kt} \theta` is [-1, 1].

  ```{calculus}
  Graph
  funcs: [arctan(x), tan(x)]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  fig_size: [6, 6]
  ```

  `{kt} arctan(r)` is sometimes written as `{kt} tan^{-1} \space r`.

  ```{note}
  The notation `{kt} tan^k \space x` means `{kt} (tan(x))^k`, but it may mean `{kt} arctan(x)` if `{kt} tan^{-1} \space x`.
  ```

  ```{note}
  The notation ...
  
  * `{kt} arctan^k \space x` means `{kt} (arctan(x))^k`. Is there a special case for `{kt} k=-1` where `{kt} arctan^{-1} \space x = tan(x)`?
  * `{kt} arctan \space x^k` means `{kt} arctan(x^k)`.
  * `{kt} arctan \space cx` means `{kt} arctan(cx)`.
  ```

* `{bm} cotangent` - The reciprocal of tangent: `{kt} cot(\theta) = \frac{1}{tan(\theta)} = \frac{adjacent}{opposite}`.

  ```{calculus}
  Graph
  funcs: [cot(x)]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  ```

  * Domain: `{kt} x \neq n \frac{pi}{2}`, where n is even
  * Range: (-inf, inf)
  * Period: `{kt} cot(x+\pi) = cot(x)`
  * Reciprocal: Tangent
  * Relationships: `{kt} cot(x)=\frac{cos(x)}{sin(x)}=tan(\frac{\pi}{2}-x)=\frac{1}{tan(x)}`

  ```{note}
  The notation ...
  
  * `{kt} cot^k \space x` means `{kt} (cot(x))^k`.
  * `{kt} cot \space x^k` means `{kt} cot(x^k)`.
  * `{kt} cot \space cx` means `{kt} cot(cx)`.
  ```

* `{bm} exponential function` - A function in the form `{kt} b^x`, where b is a positive constant.

  ```{calculus}
  Graph
  funcs: [2^x, (1/2)^x]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  ```

  * Domain: (-inf, inf)
  * Range: (0, inf)

* `{bm} logarithmic function` - A function in the form `{kt} log_{b}x`, where b is a positive constant.

  ```{calculus}
  Graph
  funcs: ["log(2,x)", "log(1/2,x)"]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  ```

  * Domain: (0, inf)
  * Range: (-inf, inf)

  A logarithmic function inverts an exponential function:
 
  * Exponential function: (base, exponent) ⟶ result (e.g. `{kt} 2^6=64`)
  * Logarithmic function: (base, result) ⟶ exponent (e.g. `{kt} log_{2}64=6`)

  ```{svgbob}
                                    .--------.
                                    v        |
  "(base, exponent) to result"    2^6 = 64   |
                                  ^     ^    |
                                  |     |    |
                                  '---. |    |
                                      | |    |
                                      v v    v
  "(base, result) to exponent"    log 2 64 = 6
  ```

* `{bm} set-builder notation/(set[-\s]builder notation|set[-\s]builder)/i` - A notation for describing the members of a set: {variable | predicate}. For example, `{kt} \{x | x>5 and x \le 10\}`. The values that the variable is confined to may be included on the right-hand side. For example, `{kt} \{x \exists \Z | x>5 and x\le10\}` is equivalent to `{kt} \{x | x \exists \Z and x>5 and x\le10\}`.

  ```{note}
  There are extensions that can include more elaborate expressions on the left-hand side. See [here](https://en.wikipedia.org/wiki/Set-builder_notation#More_complex_expressions_on_the_left_side_of_the_notation).
  ```

* `{bm} interval notation` - A notation for describing a span of numbers by listing out its two endpoints. The two endpoints are listed out in order (lesser comes first), separated by a comma, and wrapped in either square or circular brackets (potentially mismatching). For example, ...

  * `{kt} [a, b]`
  * `{kt} [-5, 10)`
  * `{kt} (-5, x]`
  * `{kt} (-5, 20)`

  If the bracket preceding/succeeding an endpoint is a ...

  * square bracket, it means that endpoint is included in the span (e.g. `{kt} [-5, 10)` includes -5 in the span). 
  * circular bracket, it  means that endpoint isn't included in the span, but everything up to / just before is (e.g. `{kt} [-5, 10)` does not include 10, but everything before 10).

  ```{note}
  If using -∞ / ∞, you must use circular brackets, because infinity isn't something that can be reached. It just indicates a direction that goes on forever. For example, `{kt} (-\infty, 10]` or `{kt} (-\infty, \infty)`.
  ```

* `{bm} transformation/(transformation|transform)/i` - A function that changes the output of some other function in some related way, typically within the context of its graph:

  * Translation shifts the output horizontally / vertically.
  * Scaling expands/compresses/mirrors the output horizontally / vertically.

  ```{calculus}
  Graph
  funcs: [x^7, 100*((x-3)^7)+2]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  fig_size: [4, 4]
  ```

  ```{seealso}
  Complete the square - Convert expression of a quadratic to one that explicitly shows transformations.
  ```

* `{bm} translate/(translation|translate)/i` - A transformation that shifts a function's output vertically and / or horizontally.

  * Shift `{kt} f(x)` vertically: `{kt} g(x)=f(x)+c`, where negative c goes down / positive c goes up.
  * Shift `{kt} f(x)` horizontally: `{kt} g(x)=f(x-d)`, where negative d goes right / positive d goes left.

  <table><tr><td>

  ```{calculus}
  Graph
  funcs: [x^7, (x^7)+3, (x^7)-3]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  fig_size: [4, 4]
  ```

  </td><td>

  ```{calculus}
  Graph
  funcs: [x^2, (x-3)^2, (x+3)^2]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  fig_size: [4, 4]
  ```

  </td></tr></table>

  ```{seealso}
  Complete the square (convert expression of a quadratic to one that explicitly shows transformations)
  ```

* `{bm} scale/(scale|scaling|reflect|reflection)/i` - A transformation that stretches/compresses a function's output and/or mirrors it across the coordinate axes. 

  <table><tr><td>

  * Stretch `{kt} f(x)` vertically: `{kt} g(x)=c \cdot f(x)` where c is `{kt} (1, \infty)`.
  * Compress `{kt} f(x)` vertically: `{kt} g(x)=c \cdot f(x)` where c is `{kt} [0, 1)`.
  * Flip `{kt} f(x)` across x-axis: `{kt} g(x)=c \cdot f(x)` where c is negative.

  ```{calculus}
  Graph
  funcs: [x^2, 2*(x^2), (1/2)*(x^2), -4*(x^2)]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  fig_size: [4, 4]
  ```

  </td><td>

  * Compress `{kt} f(x)` horizontally: `{kt} g(x)=f(bx)` where b is `{kt} (1, \infty)`.
  * Stretch `{kt} f(x)` horizontally: `{kt} g(x)=f(bx)` where b is `{kt} (0, 1)`.
  * Flip `{kt} f(x)` across y-axis: `{kt} g(x)=f(bx)` where b is negative.

  ```{calculus}
  Graph
  funcs: [x^7, (2*x)^7, ((1/2)*x)^7, ((-1/4)*x)^7]
  x_lim: [-6, 6]
  y_lim: [-6, 6]
  fig_size: [4, 4]
  ```

  </td></tr></table>

  ```{seealso}
  Complete the square (convert expression of a quadratic to one that explicitly shows transformations)
  ```

* `{bm} function operation` - Given two functions `{kt} f(x)` and `{kt} g(x)`, ...

  * `{kt} (f+g)(x) = f(x)+g(x)`, referred to as sum of functions.
  * `{kt} (f-g)(x) = f(x)-g(x)`, referred to as difference of functions.
  * `{kt} (f \cdot g)(x) = f(x) \cdot g(x)`, referred to as product of functions.
  * `{kt} (\frac{f}{g})(x) = \frac{f(x)}{g(x)}`, referred to as quotient of functions.
  * `{kt} (f \circ g)(x) = f(g(x))`, referred to as composition of functions.

* `{bm} sum of functions/(sum of functions|function addition)/i` - A function operation where two functions are summed: `{kt} (f+g)(x) = f(x)+g(x)`. The domain of `{kt} (f+g)(x)` is the intersection of `{kt} f(x)`'s domain and `g(x)`'s domain (x must be defined for both functions).

* `{bm} difference of functions/(difference of functions|function subtraction|function difference)/i` - A function operation where two functions are subtracted: `{kt} (f-g)(x) = f(x)-g(x)`. The domain of `{kt} (f-g)(x)` is the intersection of `{kt} f(x)`'s domain and `g(x)`'s domain (x must be defined for both functions).

* `{bm} product of functions/(product of functions|multiplication of functions|function product|function multiplication)/i` - A function operation where two functions are multiplied: `{kt} (f \cdot g)(x) = f(x) \cdot g(x)`. The domain of `{kt} (f \cdot g)(x)` is the intersection of `{kt} f(x)`'s domain and `g(x)`'s domain (x must be defined for both functions).

* `{bm} quotient of functions/(quotient of functions|function division)/i` - A function operation where two functions are divided: `{kt} (\frac{f}{g})(x) = \frac{f(x)}{g(x)}`. The domain of `{kt} (\frac{f}{g})(x)` has the following conditions:

  * x must be defined for both functions (intersection of `{kt} f(x)`'s domain and `{kt} g(x)`'s domain).
  * x resulting in `{kt} g(x)=0` isn't in the domain because the denominator would be 0.

  In set builder notation, the domain is `{kt} \{x \in A \cap B | g(x) \neq 0\}` where A is `{kt} f(x)`'s domain and B is `{kt} g(x)`'s domain.

* `{bm} function composition/(composition of functions|function composition|composite function|composition|composite)/i` - A function operation where one function's output is fed as the input of another function: `{kt} (f \circ g)(x) = f(g(x))`.

  ```{svgbob}
           .-------.                      .-------.    
       ----'       '----              ----'       '----
  x ---->      g      ----> "g(x)" ---->      f      ----> "f(g(x))"
       ----.       .----              ----.       .----
           '-------'                      '-------'    
  ```

  For example, given `{kt} f(u) = |u|` and `{kt} g(w) = w - 1`, the function composition `{kt} (f \circ g)(x^2) = f(g(x)) = f(x^2 - 1) = |x^2 - 1|`.

  ```{svgbob}
              .-------.                      .-------.    
          ----'       '----              ----'       '----
  "x^2" ---->     g      ----> "x^2-1" ---->     f      ----> "|x^2-1|"
          ----.       .----              ----.       .----
              '-------'                      '-------'    
  ```

  The domain of a composite function `{kt} (f \circ g)(x) = f(g(x))` is any x that can pass through the chain and result in an output. For example, imagine that the function ...

  * g is the mapping {1: 3000, 5: 100, 10: 100, 15: 3000}.
  * f is the mapping {10: 1, 100: 2}.

  When x is ...

  * is 5 or 10, g outputs 100, which is then fed into f to output 2.
  * is 1 or 15, g outputs 3000, which can't be fed into f because 3000 isn't in f's domain (undefined).
  * x is some value other than {1,5,10,15}, it isn't in g's domain (undefined).

  ```{svgbob}
             .-------.                  
         ----'   g   '----                  .-------.    
       ---->  1=  3000                  ----'   f   '----
       ---->  5=  100   -----.               10=  1
       ---->  10= 100   -----+------------>  100= 2    ----> 2
       ---->  15= 3000                  ----.       .----
         ----.       .----                  '-------'    
             '-------'                
  ```

  Therefore, `{kt} (f \circ g)(x) = f(g(x))`'s domain is `{kt} x \in \{5,10\}`.

* `{bm} function decomposition/(decomposition of a function|function decomposition|decompose function|decomposition|decompose)/i` - The process of breaking up a function into a composition of smaller functions. For example, `{kt} f(x)=\sqrt{x^2 - 1}` can be decomposed into `{kt} g(x) = x^2` and `{kt} h(x) = \sqrt{x-1}`, such that `{kt} (f \circ g)(x) = f(g(x)) = f(x^2) = \sqrt{x-1}`.

* `{bm} Heaviside function/(Heaviside function|unit step function)/i` - A step function H(x) where ...

  * 0 is returned for negative x values.
  * 1 is returned for non-negative x values.

  ```{kt}
  H(x) = \begin{cases}
   0 &\text{if } x \lt 0 \\
   1 &\text{if } x \ge 0
  \end{cases}
  ```

  ```{svgbob} 
  1         *------------


  0 --------o
            0
  ```

* `{bm} ramp function` - A piecewise function f(x) where ...

  * 0 is returned for negative x values.
  * x is returned for non-negative x values.

  ```{kt}
  f(x) = \begin{cases}
   0 &\text{if } x \lt 0 \\
   x &\text{if } x \ge 0
  \end{cases}
  ```

  The shape of a ramp function resembles a ramp.

  ```{svgbob} 
                .'
              .'
            .'
  --------.'
          0
  ```

* `{bm} tangent line` - A line that touches a curve at a specific point, having the same direction/slope of the curve at that point.

  ```{note}
  The learning material says the Latin word !!tangens!! means to "touching". How is this related to the trig function tangent? How is this related to secant line?

  Go over unit-circle definitions again.
  ```

* `{bm} secant line` - A line that intersects a curve more than once.

  ```{note}
  The learning material says the Latin word !!secan!! means to cut. How is this related to the trig function secant? How is this related to tangent line?
  ```

* `{bm} point-slope form` - The equation of a line written in the form `{kt}y-y_1=m(x-x_1)`, where `{kt} (x_1, y_1)` is a known point on the line and m is the slope.

* `{bm} limit` - The value that a function approaches as its input approaches some other value. For example, given the function `f(x)=x^2-x+2`, `{kt} f(x)` (the output) approaches 4 as x (the input) approaches.

  `{kt} \lim\limits_{x \rarr 2}f(x) = 4`

  | x     | f(x)                  |
  |-------|-----------------------|
  | 1.9   | 3.71                  |
  | 1.99  | 3.9701                |
  | 1.999 | 3.9970                |
  | 2     | *explicitly left out* |
  | 2.001 | 4.0030                |
  | 2.01  | 4.0301                |
  | 2.1   | 4.31                  |

  The table above hints that the closer and closer x gets to 2 (written as `{kt} \lim\limits_{x \rarr 2}`), the closer and closer `{kt} f(x)` gets to 4.

  <u>Limits explicitly exclude the x being approached</u>, and are typically used when it isn't possible to determine `{kt} f(x)` directly for some x. For example, `{kt} g(x)=\frac{x-1}{x^2-1}` has the domain `{kt} x \neq 1`, but `{kt} \lim\limits_{x \rarr 1}g(x) = 0.5`.

  | x     | g(x)                  |
  |-------|-----------------------|
  | 0.9   | 0.5263                |
  | 0.99  | 0.5025                |
  | 0.999 | 0.5002                |
  | 1     | *explicitly left out* |
  | 1.001 | 0.4997                |
  | 1.01  | 0.4975                |
  | 1.1   | 0.4761                |

  Likewise, the example above would be exactly the same had `{kt} g(x)` been the piecewise function ...

  ```{kt}
  g{x} = \begin{cases}
   \frac{x-1}{x^2-1} &\text{if } x \neq 1 \\
   999               &\text{if } x = 1
  \end{cases}
  ```

  If `{kt} \lim\limits_{x \rarr a} f(x)` does not approach a fixed number as x approaches a, the limit does not exist. For example, ...
  
  * `{kt} \lim\limits_{x \rarr 0} sin(\frac{\pi}{x})` does not exist because as x approaches 0, it oscillates quicker and quicker (it doesn't home in on a single number).

    ```{calculus}
    Graph
    funcs: [sin(pi/x)]
    x_lim: [-1, 1]
    y_lim: [-1, 1]
    ```

  * `{kt} \lim\limits_{x \rarr 0} H(x)`, where `{kt} H(x)` is the Heaviside function, does not exist because the limit changes depending on the direction which x approaches 0. If x approaches ...

    * from the left, the limit is 0.
    * from the right, the limit is 1.

    Since it doesn't home in on the same number from both sides, the limit does not exist.

    ```{svgbob} 
    1         *------------
  
  
    0 --------o
              0
    ```

    ```{seealso}
    One-sided limit
    ```
  
  * `{kt} \lim\limits_{x \rarr 0} \frac{1}{x^2}` does not exist because as x approaches 0, it approaches infinity and infinity isn't a number.

    ```{calculus}
    Graph
    funcs: [1/x^2]
    x_lim: [-10, 10]
    y_lim: [-10, 10]
    ```

    Although the limit does not exist, the notation ...
    
    * `{kt} \lim\limits_{x \rarr a} f(x) = \infty` is used to indicate `{kt} f(x)` increases without bound as it approaches a.
    * `{kt} \lim\limits_{x \rarr a} f(x) = -\infty` is used to indicate `{kt} f(x)` decreases without bound as it approaches a.

    ```{seealso}
    Infinite limit
    ```

  ```{seealso}
  Limit laws
  Direct substitution property
  ```

* `{bm} one-sided limit/(one[\s-]sided limit|left[\s-]hand limit|right[\s-]hand limit|left[\s-]handed limit|right[\s-]handed limit|left[\s-]side limit|right[\s-]side limit|left[\s-]sided limit|right[\s-]sided limit)/i` - A limit as approached from a single direction. The limit as approached ...

  * from the left is referred to as the left-hand limit: `{kt} x \rarr a^-`.
  * from the right is referred to as the left-hand limit `{kt} x \rarr a^+`.

  The minus / plus superscript at the end denotes if it's a left-handed limit or a right-handed limit.

  For example, as the Heaviside function approaches x=0 ...

  * from the left, the left-hand limit is 0: `{kt} \lim\limits_{x \rarr 0^-}H(x) = 0`.
  * from the right, the right-hand limit is 1: `{kt} \lim\limits_{x \rarr 0^+}H(x) = 1`.

  ```{svgbob} 
  1         *------------


  0 --------o
            0
  ```

  ```{note}
  The book explicitly mentions that, for a limit to exist, the left-hand limit and right-hand limit must result in the same number.
  ```

  ```{seealso}
  Infinite limit
  ```

* `{bm} infinite limit` - An unbounded increase or decrease as a function approaches some value:

  * `{kt} \lim\limits_{x \rarr a} f(x) = \infty` is used to indicate `{kt} f(x)` increases without bound as it approaches a.
  * `{kt} \lim\limits_{x \rarr a} f(x) = -\infty` is used to indicate `{kt} f(x)` decreases without bound as it approaches a.

  Although the notation for a limit is used, this is not a limit. A limit requires that `{kt} f(x)` approach a fixed number as x approaches a. Infinity is not a number. For example, the limit `{kt} \lim\limits_{x \rarr 0} \frac{1}{x^2} = \infty` does not exist because as x approaches 0, it approaches infinity and infinity isn't a number.

  ```{calculus}
  Graph
  funcs: [1/x^2]
  x_lim: [-10, 10]
  y_lim: [-10, 10]
  ```

  One-sided limit notation also apply to infinite limits. For example, ...
  
  * `{kt} \lim\limits_{x \rarr a^+} \frac{1}{x} = \infty`.
  * `{kt} \lim\limits_{x \rarr a^-} \frac{1}{x} = -\infty`.

  ```{calculus}
  Graph
  funcs: [1/x]
  x_lim: [-10, 10]
  y_lim: [-10, 10]
  ```

  ```{note}
  Another common notation for an infinite limit is `{kt} f(x) \rarr \infty \text{as } x \rarr a`. Change accordingly for the cases/variations discussed above (e.g. negative infinity, and one-sided limits).
  ```

  ````{note}
  When a denominator of a rational function approaches 0, it doesn't automatically mean you get an infinite limit. The learning material says: "When both numerator and denominator approach 0, it may be an infinite limit or some finite value. For example, `{kt} \lim\limits_{x \rarr 1} \frac{x^2-1}{x-1}` is *not* an infinite (if you graph it, it's a straight line where x=1 is undefined) but `{kt} \lim\limits_{x \rarr 0} \frac{sin(x)}{x^3}` is an infinite limit (both the numerator and denominator approach 0).

  ```{calculus}
  Graph
  funcs: [(x^2-1)/(x-1), sin(x)/x^3]
  x_lim: [-5, 5]
  y_lim: [-5, 5]
  fig_size: [3, 3]
  ```

  Why isn't `{kt} \lim\limits_{x \rarr 1} \frac{x^2-1}{x-1}` an infinite limit? `{kt} \frac{x^2-1}{x-1}`'s numerator factors to `{kt} \frac{(x-1)(x+1)}{x-1}` (difference of square). From there, you can eliminate the denominator: `{kt} x+1`.
  ````

* `{bm} vertical asymptote` - A vertical line x=a defined by at least one of the following infinite limits: 

  * `{kt} \lim\limits_{x \rarr a} f(x) = \infty`.
  * `{kt} \lim\limits_{x \rarr a^-} f(x) = \infty`
  * `{kt} \lim\limits_{x \rarr a^+} f(x) = \infty`
  * `{kt} \lim\limits_{x \rarr a} f(x) = -\infty`.
  * `{kt} \lim\limits_{x \rarr a^-} f(x) = -\infty`
  * `{kt} \lim\limits_{x \rarr a^+} f(x) = -\infty`

  For example, the vertical asymptote x=-3 exists in the infinite limit `{kt} \lim\limits_{x \rarr 0} \frac{1}{(x+3)^2} = \infty`.

  ```{calculus}
  Graph
  funcs: [1/(x+3)^2]
  v_asymptotes: [-3]
  x_lim: [-10, 10]
  y_lim: [-10, 10]
  ```

* `{bm} limit law` - A set of the laws that state how a limit may be broken into two limits and vice versa. Given the limits `{kt} \lim\limits_{x \rarr a} f(x)` and `{kt} \lim\limits_{x \rarr a} g(x)` both exist, the limit laws are as follows.

  ```{note}
  Recall that for a limit to exist, both of its one-sided limits must end up at the same number (infinity is not a number).
  ```

  * Sum law: `{kt} \lim\limits_{x \rarr a} [f(x)+g(x)] = \lim\limits_{x \rarr a} f(x) + \lim\limits_{x \rarr a} g(x)`
  * Difference law: `{kt} \lim\limits_{x \rarr a} [f(x)-g(x)] = \lim\limits_{x \rarr a} f(x) - \lim\limits_{x \rarr a} g(x)`
  * Constant multiple law: `{kt} \lim\limits_{x \rarr a} [c \cdot f(x)] = c \cdot \lim\limits_{x \rarr a} f(x)`
  * Product law: `{kt} \lim\limits_{x \rarr a} [f(x) \cdot g(x)] = \lim\limits_{x \rarr a} f(x) \cdot \lim\limits_{x \rarr a} g(x)`
  * Quotient law: `{kt} \lim\limits_{x \rarr a} \frac{f(x)}{g(x)} = \frac{\lim\limits_{x \rarr a} f(x)}{\lim\limits_{x \rarr a} g(x)} \text{ if} \lim\limits_{x \rarr a} g(x) \neq 0`
  * Power law: `{kt} \lim\limits_{x \rarr a} [f(x)]^n = [\lim\limits_{x \rarr a} f(x)]^n \text{ if} n \in \Z+`
  * Root law: `{kt} \lim\limits_{x \rarr a} \sqrt[n]{f(x)} = \sqrt[n]{\lim\limits_{x \rarr a} f(x)} \text{ if} n \in \Z+` -- If n is even, you can assume that `{kt} \lim\limits_{x \rarr a} f(x) > 0`.

  In addition to the limit laws described above, the following are two special limits of note that are often used alongside limit laws:

  * Limit of a constant function: If `{kt} f(x)=c`, then `{kt} \lim\limits_{x \rarr a} f(x)=c`.
  * Limit of the identity function: If `{kt} f(x)=x`, then `{kt} \lim\limits_{x \rarr a} x=a`.

  The laws described above are used to analytically determine a limit by breaking it down. For example, `{kt} \lim\limits_{x \rarr 0} 2x^2-3x+4` can be determined as follows:

  * `{kt} \lim\limits_{x \rarr 0} 2x^2-3x+4`
  * `{kt} \lim\limits_{x \rarr 0} 2x^2-3x + \lim\limits_{x \rarr 0} 4` - Sum law
  * `{kt} \lim\limits_{x \rarr 0} 2x^2 - \lim\limits_{x \rarr 0} 3x + \lim\limits_{x \rarr 0} 4` - Difference law
  * `{kt} 2\lim\limits_{x \rarr 0} x^2 - 3\lim\limits_{x \rarr 0} x + \lim\limits_{x \rarr 0} 4` - Constant multiple law
  * `{kt} 2(\lim\limits_{x \rarr 0} x)^2 - 3\lim\limits_{x \rarr 0} x + \lim\limits_{x \rarr 0} 4` - Power law
  * `{kt} 2(\lim\limits_{x \rarr 0} x)^2 - 3\lim\limits_{x \rarr 0} x + 4` - Limit of a constant function
  * `{kt} 2(0)^2 - 3(0) + 4` - Limit of the identity function
  * `{kt} 4`

  ```{note}
  The book doesn't explicitly mention it, but there seems to be an order when breaking up using limit laws? It should be in the order shown above, which is reverse of BEDMAS/PEMDAS: First apply addition/subtraction, then apply multiplication/division related laws, then power/!!root!! laws? For example, given `{kt} \lim\limits_{x \rarr 0} 5x^3`, you don't want to apply power law before constant multiple law:

  * `{kt} \lim\limits_{x \rarr 3} 5x^3`
  * `{kt} (\lim\limits_{x \rarr 3} 5x)^3` -- Power law
  * `{kt} (5\lim\limits_{x \rarr 3} x)^3` -- Constant multiple law
  * `{kt} (5(3))^3` -- Limit of the identity function
  * `{kt} (5(3))^3 = 15^3 = 3375` -- THIS IS WRONG

  The correct way to do this is to swap the power law and constant multiple law steps:

  * `{kt} \lim\limits_{x \rarr 3} 5x^3`
  * `{kt} 5\lim\limits_{x \rarr 3} x^3` -- Constant multiple law
  * `{kt} 5(\lim\limits_{x \rarr 3} x)^3` -- Power law
  * `{kt} 5(3)^3` -- Limit of the identity function
  * `{kt} 5(3)^3 = 5(9) = 45` -- THIS IS RIGHT

  You can validate that the above is correct through the direct substitution property.
  ```

  ```{note}
  The limit laws above expect both limits to exist. If a limit doesn't exist (e.g. its one-sided limits end up at different numbers (infinity is not a number) / one of its one-sided limits doesn't exist), limit laws may still be applicable for one of its one-sided limits. That is, you may apply limit laws to a one-sided limit provided that one-sided limit exists.
  ```

  **LIMIT LAW VIOLATIONS**

  In cases where a limit can't be broken down using limit laws, it may be possible to do some algebra beforehand such that it can be broken down. For example, `{kt} \lim\limits_{x \rarr 1} \frac{x^2-1}{x-1}` can't be broken down due to the quotient law not being applicable:

  * `{kt} \lim\limits_{x \rarr 1} \frac{x^2-1}{x-1}`
  * `{kt} \frac{\lim\limits_{x \rarr 1} x^2-1}{\lim\limits_{x \rarr 1} x-1}` - Invalid application of quotient law (limit in the denominator is approaching 0, which is not allowed)
  
  However, applying some algebra on `{kt} \frac{x^2-1}{x-1}` before hand results in `{kt} x+1`, which can be broken down:

  * `{kt} \frac{x^2-1}{x-1}`
  * `{kt} \frac{(x-1)(x+1)}{x-1}` - Difference of squares on numerator
  * `{kt} x+1` - Cancel out denominator

  With this new expression, the limit becomes `{kt} \lim\limits_{x \rarr 1} x+1`, which can be broken down as follows:

  * `{kt} \lim\limits_{x \rarr 1} x+1`
  * `{kt} \lim\limits_{x \rarr 1} x + \lim\limits_{x \rarr 1} 1` - Sum law
  * `{kt} 1 + \lim\limits_{x \rarr 1} 1` - Limit of the identity function
  * `{kt} 1 + 1` - Limit of a constant function
  * `{kt} 2`

  In general, `{kt} \lim\limits_{x \rarr a} f(x) = \lim\limits_{x \rarr 1} g(x)` if `{kt} f(x) = g(x) \text{ when } x \neq a`, <u>provided the limit exists</u>. The example above reworked `{kt} f(x)=\frac{x^2-1}{x-1}` to `{kt} g(x)=x+1`, and the two were equal for all x except the x being approached in the limit (`{kt} x \rarr 1`). Therefore, `{kt} \lim\limits_{x \rarr a} \frac{x^2-1}{x-1} = \lim\limits_{x \rarr 1} x+1`.

  ```{seealso}
  Direct substitution property (The property when there are no limit law violations / no algebra is needed).
  Squeeze theorem (Another potential way of solving a limit if algebra and limit laws don't work)
  ```

  ```{note}
  There's a more interesting example in the learning material when it comes to the quotient law: `{kt} \lim\limits_{x \rarr 0} \frac{\sqrt{x^2+9}-3}{x^2}`. The quotient law can't be directly applied because the denominator's limit would approach 0, which is not allowed.

  * `{kt} \lim\limits_{x \rarr 0} \frac{\sqrt{x^2+9}-3}{x^2}`
  * `{kt} \frac{\lim\limits_{x \rarr 0} \sqrt{x^2+9}-3}{\lim\limits_{x \rarr 0} x^2}` - Invalid application of quotient law (limit in the denominator is approaching 0, which is not allowed)

  To get past this, the book reworks the equation by rationalizing the numerator:
  
  * `{kt} \frac{\sqrt{x^2+9}-3}{x^2} \cdot \frac{\sqrt{x^2+9}+3}{\sqrt{x^2+9}+3}`
  * `{kt} \frac{x^2+9+3\sqrt{x^2+9}-3\sqrt{x^2+9}-9}{x^2(\sqrt{x^2+9}+3)}`
  * `{kt} \frac{x^2+9-9}{x^2(\sqrt{x^2+9}+3)}`
  * `{kt} \frac{x^2}{x^2(\sqrt{x^2+9}+3)}`
  * `{kt} \frac{1}{\sqrt{x^2+9}+3}`

  In this updated form, the quotient law doesn't have the same problem. As x approaches 0, the denominator approaches 3. The limit laws can now be applied.

  This isn't something that I would have considered doing had I seen this problem?
  ```

  **PIECEWISE FUNCTION**

  In cases where `{kt} f{x}` is a piecewise function, it may make sense to calculate the left-hand limit and right-hand limit independently. Recall that for the limit to exist, the left-hand limit and right-hand limit must end up at the same number (infinity is not a number).

  For example, `{kt} \lim\limits_{x \rarr 0^+} |x|` and `{kt} \lim\limits_{x \rarr 0^-} |x|` are both 0, meaning that `{kt} \lim\limits_{x \rarr 0} |x|` exists and is 0. However. `{kt} \lim\limits_{x \rarr 0^+} \frac{|x|}{x}` is 0 and `{kt} \lim\limits_{x \rarr 0^-} \frac{|x|}{x}` 1, meaning that `{kt} \lim\limits_{x \rarr 0} \frac{|x|}{x}` does not exist.

  ````{note}
  ```{kt}
  |x| = \begin{cases}
   x  &\text{if } x \ge 0 \\
   -x &\text{if } x < 0
  \end{cases}
  ```
  ````

  ```{seealso}
  Absolute function
  ```

  **PIECEWISE FUNCTION GOTCHA: EXCLUSIONARY CASES**

  In cases where `{kt} f{x}` is a piecewise function, special care needs to be taken: If `{kt} f(x)` is a piecewise function, `{kt} \lim\limits_{x \rarr a} f(x)` should exclude any cases in that piecewise function with the condition `{kt} x=a`. For example, consider `{kt} \lim\limits_{x \rarr 1} f(x)` where ...
  
  ```{kt}
  f(x) = \begin{cases}
   x+1  &\text{if } x \ne 1 \\
   \pi  &\text{if } x = 1
  \end{cases}
  ```

  Recall that <u>limits explicitly exclude the x being approached</u>, which in this case is x=1. If the direct substitution property were used directly on the piecewise function above, the result would be incorrect: As x approaches 1, `{kt} f(x)` does not approach π. Instead, the limit laws should be directly applied to the other case of the piecewise function:
  
  * `{kt} \lim\limits_{x \rarr 1} x+1`
  * `{kt} \lim\limits_{x \rarr 1} x + \lim\limits_{x \rarr 1} 1` - Sum law
  * `{kt} 1 + \lim\limits_{x \rarr 1} 1` - Limit of the identity function
  * `{kt} 1 + 1` - Limit of a constant function
  * `{kt} 2`

* `{bm} sum law` - A limit law that state the limit of a sum is the sum of the limits: `{kt} \lim\limits_{x \rarr a} [f(x)+g(x)] = \lim\limits_{x \rarr a} f(x) + \lim\limits_{x \rarr a} g(x)`.

* `{bm} difference law` - A limit law that states the limit of a difference is the difference of the limits: `{kt} \lim\limits_{x \rarr a} [f(x)-g(x)] = \lim\limits_{x \rarr a} f(x) - \lim\limits_{x \rarr a} g(x)`.

* `{bm} constant multiple law` - A limit law that states the limit of a constant times a function is the constant times the limit of the function: `{kt} \lim\limits_{x \rarr a} [c \cdot f(x)] = c \cdot \lim\limits_{x \rarr a} f(x)`.

* `{bm} product law` - A limit law that states the limit of a product is the product of the limits: `{kt} \lim\limits_{x \rarr a} [f(x) \cdot g(x)] = \lim\limits_{x \rarr a} f(x) \cdot \lim\limits_{x \rarr a} g(x)`.

* `{bm} quotient law` - A limit law that states the limit of a quotient is the quotient of the limits, provided that *the limit of the denominator isn't 0*: `{kt} \lim\limits_{x \rarr a} \frac{f(x)}{g(x)} = \frac{\lim\limits_{x \rarr a} f(x)}{\lim\limits_{x \rarr a} g(x)} \text{ if} \lim\limits_{x \rarr a} g(x) \neq 0`.

* `{bm} power law` - A limit law that states the limit of a power is the power of the limit, provided that *the exponent is a positive integer*: `{kt} \lim\limits_{x \rarr a} [f(x)]^n = [\lim\limits_{x \rarr a} f(x)]^n \text{ if} n \in \Z+`.

* `{bm} root law` - A limit law that states the limit of a !!root!! is the !!root!! of a limit, provided that *the exponent is a positive integer*: `{kt} \lim\limits_{x \rarr a} \sqrt[n]{f(x)} = \sqrt[n]{\lim\limits_{x \rarr a} f(x)} \text{ if} n \in \Z+`

  If n is even, you can assume that `{kt} \lim\limits_{x \rarr a} f(x) > 0`.

* `{bm} limit of a constant function/(limit of a constant function|constant function limit)/i` - The limit of a constant function is always the constant being output: If `{kt} f(x)=c`, then `{kt} \lim\limits_{x \rarr a} f(x)=c`. For example, think of the graph f(x)=5. As x approaches any value, the limit will always be 5: `{kt} \lim\limits_{x \rarr a} f(x)=5`, or in other words `{kt} \lim\limits_{x \rarr a} 5=5`.

* `{bm} limit of the identity function/(limit of the identity function|identity function limit)/i` - The limit of the identity function is always the x being approached: If `{kt} f(x)=x`, then `{kt} \lim\limits_{x \rarr a} x=a`. For example, think of the graph `{kt} f(x)=x`. As x approaches any value, the limit will always be that value: `{kt} \lim\limits_{x \rarr a} f(x)=a`, or in other words `{kt} \lim\limits_{x \rarr a} x=a`.

* `{bm} absolute function` - A piecewise function that determines the distance to some number from 0, typically represented by placing pipes around an expression. For example, ...

  ```{kt}
  |x| = \begin{cases}
   x  &\text{if } x \ge 0 \\
   -x &\text{if } x < 0
  \end{cases}
  ```

  * `{kt} |-43| = 43`
  * `{kt} |43| = 43`
  * `{kt} |x|` is `{kt} \ge 0` for any x
  * `{kt} |x^3|` is `{kt} \ge 0` for any x

  ```{calculus}
  Graph
  funcs: [abs(x)]
  x_lim: [-10, 10]
  y_lim: [-10, 10]
  fig_size: [4, 4]
  ```

* `{bm} greatest integer function/(greatest integer function|floor function)/i` - A piecewise function that maps x to the largest integer that is `{kt} \le x`, typically written as `{kt} ⟦x⟧`. For example, ...

  * `{kt} ⟦48.2⟧ = 48`
  * `{kt} ⟦48⟧ = 48`
  * `{kt} ⟦-1⟧ = -1`
  * `{kt} ⟦-1.2⟧ = -2`

  ```{svgbob}
   1 |            *------o
     |                    
   0 |      *-----o       
     |                    
  -1 |*-----o             
     |                    
     +---------------------
     -1     0     1      2
  ```

  This function is sometimes also referred to as the floor function.

  ```{note}
  The notation I'm seeing in the learning material is what I used here, but I've more often seen this function referred to as the floor function and its written as `{kt} ⌊x⌋`.
  ```

  ```{note}
  Is this a piecewise function? It seems so. It's a piecewise function with infinitely many cases where those cases follow a pattern.
  ```

  ```{seealso}
  Step function
  ```

* `{bm} constant function` - A function whose output value is the same for every input value. For example, `{kt} f(x)=5`.

* `{bm} identity function` - A function whose output value is the same as its input value. For example, `{kt} f(x)=x`.

* `{bm} direct substitution property` - `{kt} \lim\limits_{x \rarr a} f(x)=f(a)` if `{kt} f(x)` is a polynomial function or rational function and a is in the domain of `{kt} f(x)`. For example, consider `{kt} \lim\limits_{x \rarr 5} f(x)` where `{kt} f(x)=2x^2-3x+4`. The domain contains the x being approached (5), meaning the direct substitution property can be used to find the `{kt} f(x)` being approached: `{kt} \lim\limits_{x \rarr 5} f(x)=f(5)=2(5)^2-3(5)+4=39`.

  In contrast, consider `{kt} \lim\limits_{x \rarr 1} f(x)` where `{kt} f(x)=\frac{x^2-1}{x-1}`. The domain *doesn't* contain the x being approached (1), meaning the direct substitution property *can't* be used to find the `{kt} f(x)` being approached: `{kt} \lim\limits_{x \rarr 1} f(x)=f(1)=\frac{1^2-1}{1-1}=\frac{0}{0}=\text{undefined}`.

  ```{note}
  The learning material states: Functions with the direct substitution property are called continuous at a (a is the value that x is approaching).
  ```

* `{bm} radical/(radical|radicand)/i` - The nth !!root!! of some expression. For example, `{kt} \sqrt[2]{x^2+9}` is a radical.

  The expression within a radical is referred to as a radicand (`{kt} x^2+9` in the example above) and the exponent of the radical is referred to as the index (2 in the example above).

* `{bm} rationalize/(rationalize|rationalizing)/i` - Converting a fraction with a radical in it into an equivalent fraction without that radical (becomes rational). This process is typically applied to a fraction's denominator, such that the denominator becomes free of radicals. For example, multiplying `{kt} \frac{x^2}{\sqrt{x^2+9}+3}` by `{kt} \frac{\sqrt{x^2+9}-3}{\sqrt{x^2+9}-3}` removes the radical from the denominator:

  * `{kt} \frac{x^2}{\sqrt{x^2+9}+3}`
  * `{kt} \frac{x^2}{\sqrt{x^2+9}+3} \cdot \frac{\sqrt{x^2+9}-3}{\sqrt{x^2+9}-3}`
  * `{kt} \frac{x^2(\sqrt{x^2+9}-3)}{x^2+9-3\sqrt{x^2+9}+3\sqrt{x^2+9}-9}`
  * `{kt} \frac{x^2(\sqrt{x^2+9}-3)}{x^2+9-9}`
  * `{kt} \frac{x^2(\sqrt{x^2+9}-3)}{x^2}`

  ```{note}
  I've seen at least one example now in the learning material that talks about rationalizing the numerator, so this process isn't exclusive to a fraction's denominator. The example had to do with re-working a limit's function so that the quotient rule could be applied.
  ```

* `{bm} infinity/(infinity|infinite)/i` - A symbol used to indicate that something grows without bound. When ...

  * ∞ is used, it increases without bound.
  * -∞ is used, it decreases without bound.
 
  For example, `{kt} \frac{1}{x^2}` increases without bound as x approaches 0, represented in infinite limit notation as `{kt} \lim\limits_{x \rarr 0} \frac{1}{x^2} = \infty`.

  ```{calculus}
  Graph
  funcs: [1/x^2]
  x_lim: [-10, 10]
  y_lim: [-10, 10]
  ```

* `{bm} squeeze theorem/(squeeze theorem|sandwich theorem|pinching theorem)/i` - A theorem that states if the following two conditions are met ...

  1. `{kt} f(x)` and `{kt} h(x)` approach the same value as x approaches a (not considering x=a itself): `{kt} \lim\limits_{x \rarr a} f(x) = \lim\limits_{x \rarr a} h(x)`.
  2. `{kt} g(x)` is sandwiched between `{kt} f(x)` and `{kt} h(x)` when x is near a (not considering x=a itself): `{kt} f(x) \le g(x) \le h(x)` when x is near a.

  ..., then `{kt} g(x)` approaches the same value as `{kt} f(x)` and `{kt} h(x)` when it also approaches a: `{kt} \lim\limits_{x \rarr a} f(x) = \lim\limits_{x \rarr a} h(x) = \lim\limits_{x \rarr a} g(x)`.

  ```{note}
  The squeeze theorem is sometimes also referred to as the sandwich theorem or pinching theorem.
  ```

  For a trivial example, consider the following 3 functions ...

  * `{kt} f(x) = x^2+1`
  * `{kt} g(x) = \frac{x}{x}` (undefined at 0)
  * `{kt} h(x) = -x^2+1`

  ```{calculus}
  Graph
  funcs: [x^2+1, x/x, -(x^2)+1]
  x_lim: [-5, 5]
  y_lim: [-5, 5]
  ```

  When finding `{kt} \lim\limits_{x \rarr 0} g(x)`, you can see that ...
  
  1. `{kt} g(x)` is sandwiched between `{kt} f(x)` and `{kt} h(x)` when x is near 0 (not considering x=0 itself).
  2. `{kt} f(x)` and `{kt} h(x)` approach the same value as x approaches 0: `{kt} \lim\limits_{x \rarr 0} f(x) = \lim\limits_{x \rarr 0} h(x) = 1`.

  Therefore, `{kt} \lim\limits_{x \rarr a} h(x)` will also approach that same value as x approaches 0: `{kt} \lim\limits_{x \rarr a} f(x) = \lim\limits_{x \rarr a} h(x) = \lim\limits_{x \rarr a} g(x) = 1`.

  ```{note}
  This is a trivial example where the squeeze theorem isn't needed. You can just use limit laws: Apply some algebra to convert `{kt} \frac{x}{x}` into `{kt} 1` and then apply limit of a constant function.
  ```

  ```{note}
  The example above is sandwiched across the entire domain, but the requirement is that it just needs to be sandwiched when x is near a, right?
  ```

  In most cases, you'll only have the function which you're attempting to find the limit for, not the sandwiching functions. For example, consider `{kt} \lim\limits_{x \rarr 0} x^2 \cdot sin(\frac{1}{x})`. It isn't possible to find the limit of this function using just algebra and limit laws:

  * `{kt} \lim\limits_{x \rarr 0} x^2 \cdot sin(\frac{1}{x})`
  * `{kt} \lim\limits_{x \rarr 0} x^2 \cdot \lim\limits_{x \rarr 0} sin(\frac{1}{x})` - Product law
  * `{kt} (\lim\limits_{x \rarr 0} x)^2 \cdot \lim\limits_{x \rarr 0} sin(\frac{1}{x})` - Power law

  At this point, the process is stuck on `{kt} \lim\limits_{x \rarr 0} sin(\frac{1}{x})`:
  
  * The direct substitution property doesn't work here because 0 isn't in the domain of `{kt} sin(\frac{1}{x})`.
  * There is no limit law to further break down `{kt} \lim\limits_{x \rarr 0} sin(\frac{1}{x})`, even if some preliminary algebra was applied on the expression beforehand.

  ```{calculus}
  Graph
  funcs: [x^2*sin(1/x)]
  x_lim: [-0.5, 0.5]
  y_lim: [-0.3, 0.3]
  ```

  In order to use the sandwich theorem to find this limit, two functions `{kt} f(x)` and `{kt} h(x)` need to be found such that ...

  1. `{kt} f(x)` and `{kt} h(x)` approach the same value as x approaches a (not considering x=a itself): `{kt} \lim\limits_{x \rarr a} f(x) = \lim\limits_{x \rarr a} h(x)`.
  2. the function for which the limit is being found (`{kt} x^2 \cdot sin(\frac{1}{x})`), referred to as `{kt} g(x)`, is sandwiched between `{kt} f(x)` and `{kt} h(x)` when x is near a (not considering x=a itself): `{kt} f(x) \le g(x) \le h(x)` when x is near a.

  To do this, you need to rely on  properties of sine, power, and inequalities:
  
  1. For any x, `{kt} sin(x)` results in a number between [-1, 1]:
     
     * `{kt} sin(x) \ge -1`
     * `{kt} sin(x) \le 1`.

     ```{calculus}
     Graph
     funcs: [sin(x)]
     x_lim: [-5, 5]
     y_lim: [-2.5, 2.5]
     fig_size: [3, 1.5]
     ```

  2. For any x, `{kt} \frac{1}{x}` ....
  
     * results in a number `{kt} >1` if `{kt} x<1`.
     * results in a number `{kt} <1` if `{kt} x>1`.
     * results in a number `{kt} =1` if `{kt} x=1`.

     ```{calculus}
     Graph
     funcs: [1/x]
     x_lim: [-5, 5]
     y_lim: [-5, 5]
     fig_size: [3, 3]
     ```

  3. From 1 and 2, you know that for any x, `{kt} sin(\frac{1}{x})` results in a number between [-1, 1]: `{kt} sin(\frac{1}{x}) \ge -1` and `{kt} sin(\frac{1}{x}) \le 1`.

     ```{note}
     Why? The set of possible inputs (domain) into sine is the same here as it is in 1 (except x=0 is not allowed because `{kt} \frac{1}{0}` is undefined). It's just that if ...
     
     * `{kt} x<1` then the number being fed into sine is `{kt} >1`.
     * `{kt} x>1` then the number being fed into sine is `{kt} <1`.
     
     As such, the set of possible outputs (range) is the same.
     ```

     ```{calculus}
     Graph
     funcs: [sin(1/x)]
     x_lim: [-5, 5]
     y_lim: [-2.5, 2.5]
     fig_size: [3, 1.5]
     ```
  
  4. The square of any x is non-negative:
  
     * `{kt} x^2 > 0` if `{kt} x > 0`.
     * `{kt} x^2 < 0` if `{kt} x > 0`.
     * `{kt} x^2 = 0` if `{kt} x = 0`.

     ```{calculus}
     Graph
     funcs: [x^2]
     x_lim: [-5, 5]
     y_lim: [-5, 5]
     fig_size: [3, 3]
     ```
  
  5. An equality remains true if multiplied by a non-negative number:
  
     * `{kt} c \cdot x \ge a \cdot c` if `{kt} x \ge a` and c is a non-negative number.
     * `{kt} c \cdot x \le a \cdot c` if `{kt} x \le a` and c is a non-negative number.

     ```{note}
     Recall from inequality rules that you have to flip the direction of the inequality if the number you're multiplying by is negative.
     ```

  6. From 3, 4, and 5, you know that the inequalities in 3 remain true if both sides are multiplied by `{kt} x^2`:

     * `{kt} x^2 \cdot sin(\frac{1}{x}) \ge x^2 \cdot -1`
     * `{kt} x^2 \cdot sin(\frac{1}{x}) \le x^2 \cdot 1`.

     ```{note}
     Direction of inequalities don't change when multiplied by `{kt} x^2` because `{kt} x^2` will never result in a negative number.
     ```

  The two inequalities in the last point above give the two sandwich functions for `{kt} g(x) = x^2 \cdot sin(\frac{1}{x})`:

  * `{kt} x^2 \cdot sin(\frac{1}{x}) \ge x^2 \cdot -1` says that `{kt} -x^2` is the lower part of the sandwich: `{kt} f(x) = -x^2`.
  * `{kt} x^2 \cdot sin(\frac{1}{x}) \le x^2 \cdot 1` says that `{kt} x^2` is the upper part of the sandwich: `{kt} h(x) = x^2`.

  ```{calculus}
  Graph
  funcs: [x^2, x^2*sin(1/x), -(x^2)]
  x_lim: [-0.5, 0.5]
  y_lim: [-0.3, 0.3]
  fig_size: [6, 6]
  ```

  ```{note}
  This example was the only one listed in the learning material. What's the moral of the story here? If you can't use algebra and limit laws, look to see if the range is bounded on both sides and try to work something out with the squeeze theorem inequalities?

  All the squeeze theorem examples I find online have trigonometric functions involved (they're all a play on the example above). Is this applicable in some other context? I can't think up an example that isn't already solvable by using algebra + limit laws. UPDATE: ChatGPT thought up the following non-trigonometric functions: Logistic function, sigmoid function, and gaussian function (`{kt} e^{-x^2}`). I can't think up of a way to rejigger these the same way as the example above (so that they're only solvable through the sandwich theorem).
  ```

CONTINUE FROM PAGE 70 exercises

CONTINUE FROM PAGE 70 exercises

CONTINUE FROM PAGE 70 exercises

`{bm-ignore} !!([\w\-]+?)!!/i`

`{bm-error} Wrap in !! or apply suffix _POLY/(roots?)/i`
`{bm-ignore} square root`
`{bm-error} Remove _POLY/(square roots?_POLY)/i`
`{bm-error} Remove _POLY/(root_POLY law)/i`

`{bm-error} Wrap in !! or apply suffix _POLY/(degrees?)/i`

`{bm-error} Did you mean discriminant?/(discriminator)/i`

`{bm-error} Did you mean constant MULTIPLE law?/(constant product law)/i`

`{bm-error} Did you mean limit of THE identity function?/(limit of a identity function)/i`

`{bm-error} Did you mean direct substitution PROPERTY?/(direct substitution theorem)/i`

`{bm-error} Missing topic reference/(_TOPIC)/i`

`{bm-error} Use you instead of we/\b(we)\b/i`

`{bm-disable-all}`

<!-- ANSWERS AT A61 -->

BEFORE MOVING ON, DEFINE CONJUGATE PAIR

<!--
-------- 1.6 EXERCISES

1) it wants you to break down using the limit laws and use "limit of a constant function"?
  a) lim_x->2[f(x)+5g(x)]
     lim_x->2[f(x)]+lim_x->2[5g(x)] -- sum law
     5+5*(-2) -- swap in limit values
     5-10
     -5
  b) lim_x->2[g(x)]^3
     -2^3 -- swap in limit values
     -8
  c) lim_x->2[sqrt(f(x))]
     sqrt(lim_x->2[f(x))) -- root law
     sqrt(4) -- swap in limit values
     2
  d) lim_x->2[3f(x)/g(x)]
     lim_x->2[3f(x)]/lim_x->2[g(x)] -- quotient law
     3lim_x->2[f(x)]/lim_x->2[g(x)] -- constant multiple law
     3(4)/-2  -- swap in limit values
     12/-2
     -6
  e) lim_x->2[g(x)/h(x)]
     lim_x->2[g(x)]/lim_x->2[h(x)] -- quotient law
     -2/0 -- swap in limit values
     undefined? but does this mean the limit does not exist or does it mean that you need to use some other means to find the limit (e.g. squeeze theorem) -- the question doesn't give you what the functions, it just gives you the limits of the function as x approaches 2
  f) lim_x->2[g(x)h(x)/f(x)]
     lim_x->2[g(x)h(x)]/lim_x->2[f(x)] -- quotient law
     (lim_x->2[g(x)]*lim_x->2[h(x)])/lim_x->2[f(x)] -- product law
     (-2*0)/4  -- swap in limit values
     0

2)
  a) lim_x->2[f(x)+g(x)] 
     lim_x->2[f(x)]+lim_x->2[g(x)] -- sum law
     -1+2 -- swap in limits from looking at graph
     1
  b) lim_x->0[f(x)-g(x)] 
     lim_x->0[f(x)]-lim_x->0[g(x)] -- difference law
     LIMIT DOES NOT EXIST: lim_x->0[g(x)] doesn't exist because its one-sided limits approach different numbers
  c) lim_x->-1[f(x)g(x)]
     lim_x->-1[f(x)]*lim_x->-1[g(x)] -- product law
     1*2 -- swap in limits from looking at graph
     2
  d) lim_x->3[f(x)/g(x)]
     lim_x->3[f(x)]/lim_x->3[g(x)] -- quotient law
     1/0  undefined? but does this mean the limit does not exist or does it mean that you need to use some other means to find the limit (e.g. squeeze theorem)
  e) lim_x->2[x^2*f(x)]
     lim_x->2[x^2]*lim_x->2[f(x)] -- product law
     lim_x->2[x]^2*lim_x->2[f(x)] -- power law
     2^2*lim_x->2[f(x)] -- limit of an identity function
     2^2*-1 -- swap in limits from looking at graph
     -4
  f) f(-1) + lim_x->-1[g(x)]
     3+2 -- swap in limits/values from looking at graph
     5

3) lim_x->3[5x^3-3x^2+x-6]
   lim_x->3[5x^3-3x^2]+lim_x->3[x-6] -- sum law
   lim_x->3[5x^3]-lim_x->3[3x^2]+lim_x->3[x-6] -- difference law
   lim_x->3[5x^3]-lim_x->3[3x^2]+lim_x->3[x]-lim_x->3[6] -- difference law
   lim_x->3[5x^3]-3lim_x->3[x^2]+lim_x->3[x]-lim_x->3[6] -- constant multiple law
   5lim_x->3[x^3]-3lim_x->3[x^2]+lim_x->3[x]-lim_x->3[6] -- constant multiple law
   5lim_x->3[x^3]-3lim_x->3[x]^2+lim_x->3[x]-lim_x->3[6] -- power law
   5lim_x->3[x]^3-3lim_x->3[x]^2+lim_x->3[x]-lim_x->3[6] -- power law
   5(3)^3-3(3)^2+(3)-lim_x->3[6] -- limit of an identity function
   5(3)^3-3(3)^2+(3)-6 -- limit of constant function
   5(9)-3(9)-6
   24

4) lim_x->-1[(x^4-3x)(x^2+5x+3)]
   (lim_x->-1[x^4-3x])*(lim_x->-1[x^2+5x+3]) -- product law
   (lim_x->-1[x^4]-lim_x->-1[3x])*(lim_x->-1[x^2+5x+3]) -- difference law
   (lim_x->-1[x^4]-lim_x->-1[3x])*(lim_x->-1[x^2+5x+3]) -- sum law 2 twice
   (lim_x->-1[x^4]-lim_x->-1[3x])*(lim_x->-1[x^2]+lim_x->-1[5x]+lim_x->-1[3]) -- sum law 2 twice
   (lim_x->-1[x^4]-3lim_x->-1[x])*(lim_x->-1[x^2]+5lim_x->-1[x]+lim_x->-1[3]) -- constant product law twice
   (lim_x->-1[x]^4-3lim_x->-1[x])*(lim_x->-1[x]^2+5lim_x->-1[x]+lim_x->-1[3]) -- power law twice
   ((-1)^4-3(-1))*((-1)^2+5(-1)+lim_x->-1[3]) -- limit of the identity function
   ((-1)^4-3(-1))*((-1)^2+5(-1)+3) -- limit of a constant function
   (1+3)*(1-5+3)
   -4

5) lim_t->-2[(t^4-2)/(2t^2-3t+2)]
   lim_t->-2[t^4-2]/lim_t->-2[2t^2-3t+2] -- quotient rule
   [lim_t->-2[t^4]-lim_t->-2[2]]/[lim_t->-2[2t^2]-lim_t->-2[3t]+lim_t->-2[2]] -- difference law and sum law
   [lim_t->-2[t^4]-lim_t->-2[2]]/[2lim_t->-2[t^2]-3lim_t->-2[t]+lim_t->-2[2]] -- constant multiple law
   [lim_t->-2[t]^4-lim_t->-2[2]]/[2lim_t->-2[t]^2-3lim_t->-2[t]+lim_t->-2[2]] -- power law
   [-2^4-2]/[2(-2)^2-3(-2)+2] -- limit of a constant function / limit of the identity function
   [14]/[8+6+2]
   14/16=7/8

6) lim_u->-2[sqrt(u^4+3u+6)]
   sqrt(lim_u->-2[u^4+3u+6]) -- root law
   sqrt(lim_u->-2[u^4]+lim_u->-2[3u]+lim_u->-2[6]) -- sum law
   sqrt(lim_u->-2[u^4]+3lim_u->-2[u]+lim_u->-2[6]) -- constant multiple law
   sqrt(lim_u->-2[u]^4+3lim_u->-2[u]+lim_u->-2[6]) -- power law
   sqrt((-2)^4+3(-2)+6) -- limit of a constant function / limit of the identity function
   sqrt(16-6+6)=4

7) lim_x->8[(1+sqrt[3](x))(2-6x^2+x^3)]
   lim_x->8[1+sqrt[3](x)]*lim_x->8[2-6x^2+x^3] -- product law
   (lim_x->8[1]+lim_x->8[sqrt[3](x)])*(lim_x->8[2]-lim_x->8[6x^2]+lim_x->8[x^3]) -- difference law and sum law
   (lim_x->8[1]+lim_x->8[sqrt[3](x)])*(lim_x->8[2]-6lim_x->8[x^2]+lim_x->8[x^3]) -- constant product law
   (lim_x->8[1]+lim_x->8[sqrt[3](x)])*(lim_x->8[2]-6lim_x->8[x]^2+lim_x->8[x]^3) -- power law
   (lim_x->8[1]+sqrt[3](lim_x->8[x]))*(lim_x->8[2]-6lim_x->8[x]^2+lim_x->8[x]^3) -- root law
   (1+sqrt[3](8))*(2-6(8)^2+8^3) -- limit of a constant function / limit of the identity function
   390

8) lim_t->2[(t^2-2)/(t^3-3t+5)^2]
   lim_t->2[(t^2-2)/(t^3-3t+5)]^2 power law
   (lim_t->2[t^2-2]/lim_t->2[t^3-3t+5])^2 quotient law
   ((lim_t->2[t^2]-lim_t->2[2])/(lim_t->2[t^3]-lim_t->2[3t]+lim_t->2[5]))^2 difference law sum law
   ((lim_t->2[t^2]-lim_t->2[2])/(lim_t->2[t^3]-3lim_t->2[t]+lim_t->2[5]))^2 constant multiple law
   ((lim_t->2[t]^2-lim_t->2[2])/(lim_t->2[t]^3-3lim_t->2[t]+lim_t->2[5]))^2 power law
   ((2^2-2)/(2^3-3(2)+5))^2 limit of a constant function / limit of the identity function
   2/7

9) lim_x->2[sqrt((2x^2+1)/(3x-2))]
   sqrt(lim_x->2[(2x^2+1)/(3x-2)]) root law
   sqrt(lim_x->2[(2x^2+1)/(3x-2)]) quotient law
   sqrt(lim_x->2[2x^2+1]/lim_x->2[3x-2]) quotient law
   sqrt(lim_x->2[2x^2+1]/lim_x->2[3x-2]) sum law difference law
   sqrt((lim_x->2[2x^2]+lim_x->2[1])/(lim_x->2[3x]-lim_x->2[2])) sum law difference law
   sqrt((2lim_x->2[x^2]+lim_x->2[1])/(3lim_x->2[x]-lim_x->2[2])) constant multiple law
   sqrt((2lim_x->2[x]^2+lim_x->2[1])/(3lim_x->2[x]-lim_x->2[2])) power law
   sqrt((2(2)^2+1)/(3(2)-2)) limit of a constant function / limit of the identity function
   sqrt(9/4) = sqrt(9)/sqrt(4)=3/2

10a) the domain isn't the same at x=2? this comes off as a confusing question because of basic algebra

  b) the left-hand side can have some preliminary algebra applied to turn it into the right hand-side
      
     (x+3)(x-2)/(x-2) = x+3

     it's okay to make this transformation (assuming the limit actually exists) because limits explicitly exclude the x being approached, which in this case is x=2

11) can't use direct substitution property because divide by 0
    but you can factor numerator and cancel
    lim_x->5[(x^2-6x+5)/(x-5)]
    lim_x->5[(x-1)(x-5)/(x-5)]
    lim_x->5[(x-1)] -- use direct substitution property 5-1=4

12) lim_x->-3[(x^2+3x)/(x^2-x-12)] -- can't use direct substitution property because div by 0
                                      factor denominator and numerator?
    lim_x->-3[(x(x+3))/((x+3)(x-4))]
    lim_x->-3[x/(x-4)]
    lim_x->-3[x/(x-4)] -- use direct substitution 3/(3-4)=3/-1=-3

13) can't use direct substitution property because divide by 0
    lim_x->5[(x^2-5x+6)/(x-5)]
    lim_x->5[(x-2)(x-3)/(x-5)] -- factor num
    nothing to cancel? limit does not exist? graphing this, it looks like infinite limits from both sides (not a real limit)

14) lim_x->4[(x^2+3x)/(x^2-x-12)] -- can't use direct substitution property because div by 0
                                     factor denominator and numerator?
    lim_x->-3[(x(x+3))/((x+3)(x-4))]
    lim_x->-3[x/(x-4)]
    nothing left to do? limit does not exist? graphing seems to confirm this (one-sided infinite limits)

15) lim_t->-3[(t^2-9)/(2t^2+7t+3)] -- can't use direct substitution property because div by 0
    lim_t->-3[((t+3)(t-3))/(2t^2+7t+3)] -- difference of squares on numerator


    2(3)+(1)=7
     (3)*(1)=3

    2x^2+6x+1x+3
    2x(x+3)+1(x+3)
    (2x+1)(x+3)

    lim_t->-3[((t+3)(t-3))/(2t+1)(t+3)] -- sum product rule on denominator
    lim_t->-3[(t-3)/(2t+1)] -- cancel

    lim_t->-3[(t-3)/(2t+1)]
    ((-3)-3)/(2(-3)+1) -- apply direct substitution property
    (-6)/(-6+1)
    (-6)/5

16) lim_x->-1[(2x^2+3x+1)/(x^2-2x-3)] -- can't use direct substitution property because of div by 0
    probably need to factor num an denom and reduce out common factors?

    lim_x->-1[(2x^2+3x+1)/(x-3)(x+1)] sum product rule on denom
    lim_x->-1[(2x+1)(x+1)/(x-3)(x+1)] sum product rule on num
    lim_x->-1[(2x+1)/(x-3)] cancel
    
    lim_x->-1[(2x+1)/(x-3)]
    (2(-1)+1)/((-1)-3) -- apply direct substitution property
    -1/-4
    1/4

17) lim_h->0[((-5+h)^2-25)/h] --can't use direct substitution property because of div by 0

    lim_h->0[(h^2-5h-5h+25)/h]
    lim_h->0[(h^2-10h)/h]
    lim_h->0[(h(h-10)/h]
    lim_h->0[h-10]

    lim_h->0[h-10] -- apply direct substitution property
    0-10
    -10

18) lim_h->0[((2+h)^3-8)/h] -- can't use direct substitution property because of div by 0
    
    lim_h->0[((2+h)(2+h)(2+h)-8)/h]
    lim_h->0[((h^2+4h+4)(h+2)-8)/h]
    lim_h->0[((h^3+4h^2+2h^2+4h+8h+8)-8)/h]
    lim_h->0[(h^3+6h^2+12h)/h]
    lim_h->0[h^2+6h+12]

    lim_h->0[h^2+6h+12]
    0^2+6(0)+12 -- direct substitution
    12

19) lim_x->-2[(x+2)/(x^3+8)] -- can't use direct substitution property
    
    lim_x->-2[(x+2)/(x^3+2^3)] -- sum of cubes
    lim_x->-2[(x+2)/((x+2)(x^2-2x+4)] -- sum of cubes
    lim_x->-2[1/(x^2-2x+4)] -- cancel

    lim_x->-2[1/(x^2-2x+4)] -- direct substitution
    1/((-2)^2-2(-2)+4)
    1/(4+4+4)
    1/12

20) lim_t->1[(t^4-1)/(t^3-1)] -- can't use direct substitution property

    lim_t->1[(t^4-1)/(t-1)(t^2+t+1)] -- difference of cubes on denom
    lim_t->1[(t^2+1)(t^2-1)/(t-1)(t^2+t+1)] -- difference of 4th power on num
    lim_t->1[(t^2+1)(t+1)(t-1)/(t-1)(t^2+t+1)] -- difference of squares on num
    lim_t->1[(t^2+1)(t+1)/(t^2+t+1)] -- cancel
    
    lim_t->1[(t^2+1)(t+1)/(t^2+t+1)] -- direct substitution
    (1^2+1)(1+1)/(1^2+1+1)
    (1+1)(1+1)/(1+1+1)
    4/3

21) lim_h->0[(sqrt(9+h)-3)/h] -- can't use direct substitution property

    lim_h->0[((9+h)^0.5-3)/h] -- rework to exponent
    lim_h->0[((9+h)^0.5-3)((9+h)^0.5+3)/h((9+h)^0.5+3)] -- mul by ((9+h)^0.5+3)/((9+h)^0.5+3) -- conjugate of num
    lim_h->0[(9+h-9)/h((9+h)^0.5+3)] -- simplify
    lim_h->0[h/h((9+h)^0.5+3)] -- simplify
    lim_h->0[1/((9+h)^0.5+3)] -- cancel

    lim_h->0[1/((9+h)^0.5+3)] -- direct substitution
    1/((9+0)^0.5+3)
    1/(9^0.5+3)
    1/6

    THIS ONE WAS TOUGH BECAUSE I COMPLETELY FORGOT ABOUT THE CONCEPT OF CONJUGATES

22) lim_u->2[(sqrt(4u+1)-3)/(u-2)] -- can't use direct substitution property
   
    lim_u->2[(sqrt(4u+1)-3)/(u-2) * (sqrt(4u+1)+3)/(sqrt(4u+1)+3)] -- conjugate

    simplify numerator:
    (sqrt(4u+1)-3)*(sqrt(4u+1)+3) = sqrt(4u+1)*sqrt(4u+1)+3sqrt(4u+1)-3sqrt(4u+1)-9
                                  = sqrt(4u+1)*sqrt(4u+1)-9
                                  = 4u+1-9
                                  = 4u-8
                                  = 4(u-2)

    lim_u->2[4(u-2)/(u-2)(sqrt(4u+1)+3)] -- cancel u-2
    lim_u->2[4/(sqrt(4u+1)+3)]

    lim_u->2[4/(sqrt(4u+1)+3)] -- direct substitution
    4/sqrt(4(2)+1)+3
    4/sqrt(8+1)+3
    4/sqrt(9)+3
    4/6

23) lim_x->3[(1/x-1/3)/(x-3)] -- can't use direct substitution property
    
    lim_x->3[(-3/x+1)/-3(x-3)] -- mult by -3/-3
    lim_x->3[(-3+x)/-3x(x-3)] -- mult by x/x
    lim_x->3[(x-3)/-3x(x-3)] -- commutative on numerator
    lim_x->3[1/-3x] -- cancel numerator

    lim_x->3[1/-3x] -- direct substitution
    1/-3(3)
    1/-9

    I THOUGHT I WOULD HAVE TO USE CONJUGATE PAIRS HERE BUT THAT WASN'T THE CASE

24) lim_h->0[((3+h)^-1-3^-1)/h] -- can't use direct substitution

    lim_h->0[(1/(3+h)-1/3)/h] -- neg exp to frac
    lim_h->0[(1/(3+h)h-1/3h]
    ...
    ... there are too many steps here, i did them in desmos graphing calc
    ...
    lim_h->0[-1/(9+3x)]

    lim_h->0[-1/(9+3x)] -- simplify
    -1/9

25) lim_t->0[(sqrt(1+t)-sqrt(1-t))/t] -- can't use direct substitution property

    lim_t->0[(sqrt(1+t)-sqrt(1-t))*(sqrt(1+t)+sqrt(1-t))/t(sqrt(1+t)+sqrt(1-t))] -- mul by conjugate
    lim_t->0[((1+t)+sqrt(1+t)sqrt(1-t)-sqrt(1+t)sqrt(1-t)-(1-t))/t(sqrt(1+t)+sqrt(1-t))]
    lim_t->0[((1+t)-(1-t))/t(sqrt(1+t)+sqrt(1-t))]
    lim_t->0[(1+t-1+t)/t(sqrt(1+t)+sqrt(1-t))]
    lim_t->0[2t/t(sqrt(1+t)+sqrt(1-t))]
    lim_t->0[2/(sqrt(1+t)+sqrt(1-t))]

    lim_t->0[2/(sqrt(1+t)+sqrt(1-t))] -- direct substitution
    2/(sqrt(1)+sqrt(1))
    2/2
    1

26)
-->

<!--
-------- 1.5 EXERCISES
1) as x approaches 2, f(x) will approach 5
   it is possible, because we aren't considering x=2, we're just considering values for x that approach 2

2) as x approaches 1 from the left (only considering x values left of 1 / smaller than 1), f(x) approaches 3
   as x approaches 1 from the right (only considering x values right of 1 / larger than 1), f(x) approaches 7
   
   NO the limit doesn't exist -- for the limit to exist, both one-sided limits must converge to a fixed number

3a) this is an "infinite limit". in other words, the limit doesn't exist, but the notation is there to tell us that as x approaches -3, f(x) increases without bound (keeps going up and up without end).
 b) this is an "infinite limit". in other words, the limit doesn't exist, but the notation is there to tell us that as x approaches 4 (from the right), f(x) decreases without bound (keeps going down and down without end).

4a) f(x) approaches 3
 b) f(x) approaches 1
 c) limit doesn't exist (because one-sided limits approach different numbers -- see a/b above)
 d) f(2)=3
 e) limit as x approaches 4 is f(x)=4
 f) f(4) is undefined

5a) as x approaches 1, f(x) approaches 2
 b) as x approaches 3 from the left, f(x) approaches 1
 c) as x approaches 3 from the right, f(x) approaches 4
 d) the limit doesn't exist as x approaches 3 (because one-sided limits approach different numbers -- see b/c above)
 e) f(3)=3

6a) as x approaches -3 from the left, h(x) approaches 4
 b) as x approaches -3 from the right, h(x) approaches 4
 c) as x approaches -3, h(x) approaches 4
 d) h(-3) is undefined
 e) as x approaches 0 from the left, h(x) approaches 1
 f) as x approaches 0 from the right, h(x) approaches -1
 g) as x approaches 0, h(x) doesn't approach a limit (because one-sides limits approach different numbers).
 h) h(0)=1
 i) as x approaches 2, h(x) approaches 2
 j) h(2) is undefined
 k) as x approaches 5 from the right, h(x) approaches 3
 l) as x approaches 5 from the left, h(x) doesn't approach a limit (it looks like its an infinitely compressing oscillation, meaning it isn't homing on a single number)

7a) as x approaches 0 from the left, g(x) approaches -1
 b) as x approaches 0 from the right, g(x) approaches -2
 c) as x approaches 0, g(x) doesn't approach a limit (because one-sides limits approach different numbers).
 d) as x approaches 2 from the left, g(x) approaches 2
 e) as x approaches 2 from the right, g(x) approaches 0
 f) as x approaches 2, g(x) doesn't approach a limit (because one-sides limits approach different numbers).
 g) g(2) = 1
 h) as x approaches 4, g(x) approaches 3

8a) inf
 b) -inf
 c) inf
 d) -inf
 e) x=-3, x=-1, x=2

9a) -inf
 b) inf
 c) inf
 d) -inf
 e) inf
 f) x=-6, x=-3, x=0, x=6

10) 150mg every 4 hrs
    as t approaches 12 from the left, f(t) approaches 150
    as t approaches 12 from the right, f(t) approaches 300

    its the saturation of drugs before/after? I don't know what this is asking. Maybe it has something to do with the way the lines bend? the halflife?

11) limit of x doesn't exist when approaching pi -- for all other x, you can get the limit?
12) limit of x doesn't exist when approaching pi -- for all other x, you can get the limit?

13a) exists
  b) exists
  c) does not exist (doesn't home in on the same num from both sides)
14a) exists
  b) exists
  c) looks like it exists -- both sides look like they're homing in on f(x)=0

15-18) skip

19) 0.5
20) doesn't exist? one side decreases without bound while the other increases without bound
21) 0.5
22) if not 80, somewhere around 80

23-26) skip

27a) -1.5
  b) looks fine to me, got hte table of values from the calculator

28) skip

29-39) skip -- whats there to determine, you already said there's an infinite limit at the point -- it just wants you to say if its going down (-inf) or going up (inf)?

40) skip

41a) approaches -inf from left and inf from right
     0.9, -3.6900
     0.99, -33.6689
     0.999, -333.6669
     0.9999, -3333.6667
     1.0001, 3333.0000
     1.001, 333.0002
     1.01, 33.0022
     1.1, 3.0211
  b) x^3-1 != 0
     x^3 != 1
     x != (1)^(1/3)
     x != 1

     x can't be 1
     when coming into 1 from 0 (non-inclusive):
                 x^3 evaluates to (0,1)
                 x^3-1 evaluates to (-1,0)
                 1 over a number between (-1,0) - the denominator is a fraction < -1, flip and negate
                                                  1/(-1/2) becomes -2/1=-2
                                                  1/(-1/3) becomes -3/1=-3
                                                  1/(-1/4) becomes -4/1=-4
                                                  1/(-1/5) becomes -5/1=-5
                                                  the closer it get, the higher the magnitude of the negative
     when going out from 1 from 2 (non-inclusive):
                 x^3 evaluates to (1,2)
                 x^3-1 evaluates to (0,1)
                 1 over a number between (0,1) - the denominator is a fraction > 1
                                                  1/(1/2) becomes 2/1=2
                                                  1/(1/3) becomes 3/1=3
                                                  1/(1/4) becomes 4/1=4
                                                  1/(1/5) becomes 5/1=5
                                                  the closer it gets, the higher the number
 c) graphed it

42a) approaches 4
  b) approaches 4
     -0.1, 4.2279
     -0.01, 4.0021
     -0.001, 4.0000
     -0.0001, 4.0000
     0.0001, 4.0000
     0.001, 4.0000
     0.01, 4.0021
     0.1, 4.2279

43a) looks like it approaches 0?
     0.05, 0.001464735
     0.1, 0.008928227
     0.2, 0.038851302
     0.4, 0.158680492
     0.6, 0.358484283
     0.8, 0.638258899
     1, 0.998000000
  b) looks like it approaches -0.01?
     0.001, -0.000999693
     0.003, -0.000993082
     0.005, -0.000978472
     0.01, -0.000906956
     0.02, -0.000613959
     0.04, 0.000571886

44) skip

45) the closer it gets to 0, the more he oscillations compress, the oscillations seem to be compressing infinitely as it gets closer and closer to 0

46) tan(1/x)

  a) show that tan(1/x) is 0 for x=1/pi,1/2pi,1/3pi,...
     
     tan(1/x) = sin(1/x)/cos(1/x)

     for tan(1/x) to be 0, sin(1/x) should evaluate to 0? sin(1/x) oscillates compress infinitely as they reach x=0. where as sin(x)   has its zeros at x=pi,2pi,3pi
                         sin(1/x) has its zeros at x=1/pi,1/2pi,1/3pi

  b) show that tan(1/x) is 1 for x=4/pi,4/5pi,4/9pi,...

     tan(1/x) = sin(1/x)/cos(1/x)    

     for tan(1/x) to evaluate to 1, sin(1/x) and cos(1/x) need to evaluate to the same number (where they intersect). if you plot out normal sin and normal cos, you see this happens starting at pi/4 and repeats every +/-pi. where as sin(x)=cos(x)=1 is at x=pi/4,5pi/4,9pi/3
                                   sin(1/x)=cos(1/x)=1 is at x=1/(pi/4), 1/(5pi/4), 1/(9pi/4)
                                                               4/pi    , 4/5pi    , 4/9pi

  c) where as before .. sin(x)   has its zeros at x=pi,2pi,3pi
                        sin(1/x) has its zeros at x=1/pi,1/2pi,1/3pi
     where as before .. sin(x)=cos(x)=1     is at x=pi/4,5pi/4,9pi/3
                        sin(1/x)=cos(1/x)=1 is at x=4/pi,4/5pi,4/9pi
     before they were spaced out evenly at intervals of pi
     they've transformed such that each interval is shorter than the next, and it's going towards 0 instead of away from 0

47) from graphing, it looks like ...
      x=2.238
      x=0.903
      x=-0.903
      x=-2.238

    finding exact: tan(2sin(x)) = sin(2sin(x))/cos(2sin(x))
                                  2sin(sin(x))cos(sin(x))/1-2sin(sin(x))^2  "dbl angle identities"
                                                                              ^
                                                                              |
                                                            didn't know what this was, had to look it up

                                  1-2sin(sin(x))^2 != 0
                                  -2sin(sin(x))^2 != -1
                                  2sin(sin(x))^2 != 1
                                  sin(sin(x))^2 != 0.5
                                  sin(sin(x)) != +-sqrt(0.5)
                                  sin(x) != arcsin(+-sqrt(0.5))
                                  x != arcsin(arcsin(+-sqrt(0.5))))

                                  because arcsin isn't periodic but sin is, we only get 1st asymptote closest to 0, 
                                  
                                  arcsin(arcsin(+-sqrt(0.5))))=+-0.9033911
                                  
                                  but our domain is supposed to be [-pi, pi], which means we need to go out 1 more step? NOPE THAT'S WRONG -- THE 

                                  1*arcsin(arcsin(+-sqrt(0.5)))) is the graphed asymp at 0.903
                                  2*arcsin(arcsin(+-sqrt(0.5)))) IS NOT the graphed asymp at 2.238
    
    THIS IS WRONG, NEW ANSWER AFTER ASKING ONLINE + CHATGPT (WHICH ARE ALSO WRONG)

    i did tihs several different ways but i still didn't find the equations for the outer set of asymptotes. the book gives the answer:

    +-arccsin(pi/4) and +-(pi-arcsin(pi/4))

    why add pi for the 2nd set of asymptotes?

48) as v approaches c (from the left?) -- v^2/c^2 gets closer and closer to 1

    the denominator is sqrt(1-(v^2/c^2))

    as v^2/c^2 gets closer and closer to 1 ...
      ... meaning 1-(v^2/c^2) approaches 0
      ... meaning sqrt(1-(v^2/c^2)) approaches 0, which is not defined

49a) graph shows that as x approaches 1, the function approaches 6
  
     0.9, 5.280931738
     0.99, 5.925312187
     0.999, 5.992503125
     0.9999, 5.999250031
     1.0001, 6.000750031
     1.001, 6.007503125
     1.01, 6.075312812
     1.1, 6.781557287

  b) we assume the limit is at (1,6)

     there are two equations to solve here:

     5.5 = (x^3-1)/(sqrt(x)-1)
     6.5 = (x^3-1)/(sqrt(x)-1)

     once found, take the larger x and abs(x-1) to find the distance to 1 (how close it has to be to 1).

     5.5 = (x^3-1)/(sqrt(x)-1)
     5.5sqrt(x)-5.5 = x^3-1
     5.5sqrt(x) = x^3-1+5.5
     5.5sqrt(x) = x^3-4.5
     (5.5sqrt(x))^2 = (x^3-4.5)^2
     30.25x = (x^3-4.5)^2
     30.25x = x^6-9x^3+20.25
     0 = x^6-9x^3+20.25 - 30.25x
     0 = x^6-9x^3-30.25x+20.25

     I don't know what to do at this point. I can graph it and see the zeros but I can't really factor it? I can use polynomial division maybe but I need to know a root beforehand? I tried asking online, asking chatgpt4 and tried getting sympy to show me the steps when it solves. nothing seems to work
     
     5.5 = (x^3-1)/(sqrt(x)-1) * (sqrt(x)+1)/(sqrt(x)+1)
     5.5 = (x^3-1)(sqrt(x)+1)/((sqrt(x)-1)(sqrt(x)+1))
     5.5 = (x^3-1)(sqrt(x)+1)/(x-1)
     5.5(x-1) = (x^3-1)(sqrt(x)+1)
     5.5(x-1) = (x^3-1)(x^0.5+1)
     (5.5(x-1))/(x^3-1) = x^0.5+1
     (5.5(x-1))/(x^3-1)-1 = x^0.5
     ((5.5(x-1))/(x^3-1)-1)^2 = (x^0.5)^2
     (-2x^3+11x-9)^2/(4(x^3-1)^2) = x <-- simplified using sympy: (((Rational(55, 10)*(x-1))/(x**3-1))-1)**2
     (-2x^3+11x-9)^2 = 4x(x^3-1)^2
     (-2x^3+11x-9)^2 = 4x^7-8x^4+4x
     4x^6-44x^4+36x^3+121x^2-198x+81 = 4x^7-8x^4+4x
     4x^7-4x^6-44x^4+36x^3+121x^2-198x+81 = -8x^4+4x
     4x^7-4x^6-52x^4+36x^3+121x^2-198x+81 = 4x
     4x^7-4x^6-52x^4+36x^3+121x^2-194x+81 = 0

     I can use polynomial division for this? but I need to know at least 1 root to begin with? Use rational root theorem. But, after graphing, none of the zeros I'm seeing in the graph aren't showing up as potential options provided by the rational root theorem? NONE OF THEM WORK.

     Try again

     5.5 = (x^3-1)/(sqrt(x)-1)
     5.5sqrt(x)-5.5 = x^3-1
     5.5sqrt(x) = x^3-1+5.5
     5.5sqrt(x) = x^3+4.5
     sqrt(x) = (x^3+4.5)/5.5
     x^0.5 = (x^3+4.5)/5.5
     x = ((x^3+4.5)/5.5)^2   <- chatgpt says this step is wrong? squaring can lead to "complex polynomial"?
     x = (x^3+4.5)/5.5 * (x^3+4.5)/5.5
     x = (x^3+4.5)(x^3+4.5)/5.5*5.5
     x = (x^3+4.5)(x^3+4.5)/30.25
     30.25x = (x^3+4.5)(x^3+4.5)
     30.25x = x^6+9x^3+20.25
     0 = x^6+9x^3-30.25x+20.25  <- when graphing, this looks like the correct (zero is what i expect)
                                   but how do I get this through algebra?

                                   * the polynomial is too high degree to use something like quadratic equation
                                   * i can't use polynomial division because i don't already have a factor, and i can't use rational roots theorem because the constant is not an integer (factors of 20.25?)

     0 = x^6+9x^3-30.25x+20.25
     -20.25 = x^6+9x^3-30.25x
     -20.25*100 = (x^6+9x^3-30.25x)*100
     0 = 100x^6+900x^3-3025x+2025

     rational root theorem shows that there's root of x=1, meaning (x-1) is a factor -- use polynomial division

           100x^5+100x^4+100x^3+1000x^2+1000x-2025
         .----------------------------------------
     x-1 | 100x^6+0x^5  +0x^4  +900x^3 +0x^2   -3025x+2025
           100x^6-100x^5
           -------------
                 +100x^5+0x^4
                 +100x^5-100x^4
                 --------------
                        +100x^4+900x^3
                        +100x^4-100x^3
                        --------------
                                1000x^3+0x^2
                                1000x^2-1000x^2
                                ---------------
                                       +1000x^2-3025x
                                       +1000x^2-1000x
                                       --------------
                                               -2025x+2025
                                               -2025x+2025
                                               -----------
                                                      0

       using the rational root theorem on the second part (100x^5+100x^4+100x^3+1000x^2+1000x-2025) yields no results? WHAT DO I DO HERE? I can factor out 25 but it makes no difference

       0 = (x-1)(100x^5+100x^4+100x^3+1000x^2+1000x-2025)
       0 = (x-1)25(4x^5+4x^4+4x^3+40x^2+40x-81)

       they intentionally made this the last question to force you to eat shit?
                                      
-->

<!--
-------- 1.4 EXERCISES

1) 1000 gallons, drains fully out of the bottom in 30 mins
   t=time in minutes
   V=volume of water in tank

   
 a) slope=(y2-y1)/(x2-x1)
          (y2-250)/(x2-15)

    5->(694-250)/(5-15)-44.4
    10->(444-250)/(10-15)=-38.8
    15->THIS
    20->(111-250)/(20-15)-27.8
    25->(28-250)/(25-15)=-22.2
    30->(0-250)/(30-15)=-16.666

  b) change_in_volume/time_elapsed = (444-111)/-10=-33.3
  c) ??? graphed it in desmos, not sure what this is asking for because the answer would be the same as b?

2) cardiac monitor -- counts the num of heartbeats after t minutes
   when graphed, tangent line represents heartrate in beats-per-min
   estimate heart rate between the given time points

   the heart rate estimate is the slope between the two points?

 a) m=(2948-2530)/(42-36)=69.666
 b) m=(2948-2661)/(42-38)=71.75
 c) m=(2948-2806)/(42-40)=71
 d) m=(3080-2948)/(44-42)=66

3a) P=(2,-1)  Q=(x, 1/(1-x))
    m=(y2-y1)/(x2-x1)=((-1)-(1/(1-x)))/(2-x)
    [2.0, 1.111, 1.010, 1.001, 0.666, 0.909, 0.990, 0.999]
3b) 1
3c) m=1 and (2,-1) is on the line
    y=mx+b
    -1=1(2)+b
    -1=2+b
    -1-2=b
    -3=b
    y=1x-3

4a) P=(0.5,0) y=math.cos(math.pi*x)
    x=0.000000 y=1.000000 m=-2.000000
    x=0.400000 y=0.309017 m=-3.090170
    x=0.490000 y=0.031411 m=-3.141076
    x=0.499000 y=0.003142 m=-3.141587
    x=1.000000 y=-1.000000 m=-2.000000
    x=0.600000 y=-0.309017 m=-3.090170
    x=0.510000 y=-0.031411 m=-3.141076
    x=0.501000 y=-0.003142 m=-3.141587
4b)-pi
4c)y=(-pi)x+b
   0=(-pi)0.5+b
   0=-0.5pi+b
   0.5pi=b
   y=(-pi)x+0.5pi
4d) skip

5) ball thrown @ 40ft/s
   height @ t secs = 40t-16t^2
   a) find avg velocity @ t=2 and lasting...
    1) 0.5secs
       t=2    40*2-16*2^2=80-64=16
       t=0.5  40*0.5-16*0.5^2=20-4=16
       slope=(16-16)/(2-0.5)=0/1.5=0
    2) 0.1secs
       t=2    40*2-16*2^2=80-64=16
       t=0.1  40*0.1-16*0.1^2=3.84
       slope=(16-3.84)/(2-0.1)=6.4
    3) 0.05secs
       t=2    40*2-16*2^2=80-64=16
       t=0.05 40*0.05-16*0.05^2=1.96
       slope=(16-1.96)/(2-0.05)=7.2
    4) 0.01secs
       t=2    40*2-16*2^2=80-64=16
       t=0.01 40*0.01-16*0.01^2=0.3984
       slope=(16-0.3984)/(2-0.01)=7.84
   b) t=1.9    y=18.24    slope=(16-18.24)/(2-1.9)=-22.4
      t=1.99   y=16.2384  slope=(16-16.2384)/(2-1.99)=−23.84
      t=2.01   y=15.7584  slope=(16-15.7584)/(2-2.01)=−24.16
      t=2.1    y=13.44    slope=(16-13.44)/(2-2.1)=−25.6
      it looks like at t=2 the slope will be exactly 24?

6) rock thrown @ 10m/s
   height @ t secs = 10t-1.86t^2
   a1) t=1     10*1-1.86*1^2=8.14
       t=2     10*2-1.86*2^2=12.56
       slope=(8.14-12.56)/(1-2)-4.42
   a2) t=1     10*1-1.86*1^2=8.14
       t=1.5   10*1.5-1.86*1.5^2=10.815
       slope=(8.14-10.815)/(1-1.5)=5.35
   a3) t=1     10*1-1.86*1^2=8.14
       t=1.01  10*1.01-1.86*1.01^2=8.202614
       slope=(8.14-8.202614)/(1-1.01)=6.2614
   a4) t=1     10*1-1.86*1^2=8.14
       t=1.001 10*1.001-1.86*1.001^2=8.14627814
       slope=(8.14-8.14627814)/(1-1.001)=6.2781
   b) t=0.9   y=7.4934      slope=(8.14-7.4934)/(1-0.9)=6.466
      t=0.99  y=8.077014    slope=(8.14-8.077014)/(1-0.99)=6.2986
      t=0.999 y=8.13371814  slope=(8.14-8.13371814)/(1-0.999)=6.28186
      t=1.001 y=8.14627814  slope=(8.14-8.14627814)/(1-1.001)=6.27814
      t=1.01  y=8.202614    slope=(8.14-8.202614)/(1-1.01)=6.2614
      t=1.1   y=8.7494      slope=(8.14-8.7494)/(1-1.1)=6.094
      it looks like at t=1 the slope is around 6.28? maybe just under 6.28?

7) a1) (20.6-79.2)/(2-4)=29.3
   a2) (46.5-79.2)/(3-4)=32.7
   a3) (79.2-124.8)/(4-5)=45.6
   a4) (79.2-176.7)/(4-6)=48.75
   b) i can eyeball it from the graph -- not gonna estimate a number

8) skip

9) P=(1,0) is on y=sin(10pi/x)
 a) Q=(x,sin(10pi/x))
    0.0000, 1.7321, -1.0847, -2.7433, 4.3301, -2.8173, 0.0000, -2.1651, -2.6061, -5.0000, 3.4202
    no they don't appear to be approaching a limit? its oscillating? this is a periodic function?
 b) ??? i don't understand what this is getting at? maybe it has tsomething to do with the fact that the graph looks like it's infinitely compressing the closer it gets to x=0 (period is getting shorter and shorter)
 c) P=(1,0), so maybe get slope at x=0.999 and x=1.001 and average out to get hte slope?
    (-31.4422 + -31.3794) / 2 = −31.4108
-->

<!--
-------- 1.3 EXERCISES

1a) f(x)+3
 b) f(x)-3
 c) f(x-3)
 d) f(x+3)
 e) -f(x)
 f) f(-x)
 g) 3f(x)
 h) (1/3)f(x)

2a) move it up by 8
 b) move it left by 8
 c) scale it vertically by 8
 d) compress it horizontally by 8
 e) flip it across the x-axis and move it down by 1
 f) blow it up 8x

3a) 3
 b) 1
 c) 4
 d) 5
 e) 2

4-5) skip

6) y=2sqrt(3x-x^2)

7) y=-sqrt(3x-x^2) - 1

8a) former has been stretched out horizontally 2x. not graphing.
 b) former has been shifted up by 1. not graphing.

9) parabola flipped
10) parabola shifted right by 3
11) shifted down up by 1
12) the 2 curves and their asymptotes get flipped across x and shifted up by 1
13) cos curve is squeezed horizontally by 3 and stretched vertically by 2x.
    - where as cos curve's x-intercepts are pi/2+(pi)*n, the new x-intercepts will be (pi/2+(pi)*n)/3
    - high/low points are not 2/-2
14) move sqrt(x) left by 1 and stretch it vertically 2x
    - point 0,0 on x now becomes -1,0
    - point 1,1 on sqrt(x) now becomes 0,2
15) you need to try to factor this (or use quadratic equation) and complete the square.
    - factoring/quadratic formula will give you x-intercepts 
      - not possible, discriminant says there's no root
    - completing the square will give you origin, translation, and scaling
        x^2-4x+5
        (x^2-4x)+5
        (x-2x-2x+4)+5-4
        (x-2)^2+1
        x^2 shift right 2 and up 1
16) graph of sin is compressed by pi, meaning ...
    * where as sin's x-intercepts are at n*pi, sin(pi*x) compresses it by horizontally pi, meaning it scales it by 1/pi -- (n*pi)/pi = n, meaning the x-intercepts of sin(pi*x) are integers
    * shift it up by 1
17) sqrt graph flipped over x-axis and moved up by 2
18) cos graph flipped over x-axis and stretched vertically by 2, shift up by 3
19) sin graph by is stretched by 2, meaning x-intercepts are now at 2n*pi rather than n*pi (where n is an integer)
20) |x| is a V shape at origin 0,0 -- shift it down by 2
21) |x| is a V shape at origin 0,0 -- shift it right by 2
22) tan's asymptotes are at (pi/2)+n*(pi) and is an "odd function" (center at 0,0)
    - shift it over by pi/4, meaning asymptotes ar know at (pi/4)+(pi/2)+n*(pi)
                                                           (pi/4)+(2pi/4)+n*(pi)
                                                           (3pi/4)+n*(pi)
    - squish vertically to a quarter of original size, meaning make hte curve a bit steeper?
      there's no hard and fast coordinates (that don't sit on x-axis) to use as reference points for drawing horizontally scaled
23) shift sqrt(x) down by 1, and reflect the points that are below x-axis (x between 0 and 1)
24) cos x-intercepts scaled horizontally from pi/2+n*pi to (pi/2+n*pi)/pi
                                                           (pi/2)/pi+(n*pi)/pi
                                                           (pi/2)*(1/pi)+n
                                                           (1/2)+n
    then, any point below the x-axis is reflected, meaning you're going to get a bunch of humps with sharp edges

25) skip

26) variable star, brightness oscillates
    delta cephei, 5.4 days to oscillate 1 time
                  4.0 avg brightness, +/- 0.35 brightness, so brightness goes form 4.35 to 3.65

    
    since it oscillates, you can start with cos(x)
    1. 0.35cos(x) to get wave between +0.35 and -0.35
    2. 0.35cos(x)+4 to get wave between +4.35 and -4.35
    3. 0.35cos(2pi*x)+4 to get 1 full wave in 1 unit
    4. 0.35cos(2pi*x)+4 to get 1 full wave in 1 unit
    5. 0.35cos((10/54)*2pi*x)+4 to get 1 full wave in 5.4 units

27) low = 2 and high = 12, difference = 12-2=10, middle = (12-2)/2+2=5+2=7
    1 full oscillation = 12 hours

    1. 5cos(x) to get it between -5 and 5
    2. 5cos(x)+7 to get it between 2 and 12
    3. 5cos(2pi*x)+7 to get 1 full cycle per unit
    4. 5cos((1/12)*2pi*x)+7 to get a full cycle in 12 units (12 hours)

    at this point x=0 is midnight and is also high tide, but the problem says high tide happens at 6:45AM. That means we need to shift x such that the top is at x=6.75 (6:45 -- 60 mins in an hour, 45/60=0.75)

    5cos((1/12)*2pi*x-6.75)+7

28) low=2000 high=2500 1cycle=4seconds
    this is exactly like prev question

    250sin(x)+2250 -- make it go from 2000 to 2500
    250sin((1/4)2pi*x)+2250 -- 1 cycle = 4 seconds

29a) y=f(|x|) -- when x=-1, it's the same as x=1
                 when x=-2, it's the same as x=2
                 etc..

                 so the function mirrors the positive side of the graph f onto the negative side?

  b) already did it, it mirrors as described above
  c) already did it, it mirrors as described above

30) 1/f(x) -- x can't = 0? so i'd imagine there'd be asymptotes or something at the roots?

    i didn't know enough about this to do it, but i graphed it and it looks like the asymptotes are right. the graph has curves that hug the asymptotes, where the prongs of those curves point in the direction that y is going on the original graph for those sections?

31a) x^3+2x^2+3x^2-1
     x^3+2x^2+3x^2-1
     -- TODO: i need to factor this to find its roots? which gives the domain?
              NO - you would need to do this if this polynomial were part of a denominator
     domain is (-inf, inf)
  b) x^3+2x^2-3x^2-1  domain: (-inf, inf)
  c) (x^3)(3x^2-1)  domain: (-inf, inf)
  d) (x^3)/(3x^2-1)  domain: 3x^2-1 != 0   3x^2+0x-1 !=0
                                           use quadratic formula?
                                           (-0+/-sqrt(0^2-4(3)(-1)))/(2(3))
                                           +/-sqrt(0^2-4(3)(-1))/6
                                           +/-sqrt(-4(3)(-1))/6
                                           +/-sqrt(-4(-3))/6
                                           +/-sqrt(12)/6
                                           x is undefined on sqrt(12)/6=0 and -sqrt(12)/6
                                           x!=sqrt(12)/6=0 and x!=-sqrt(12)/6

32a) sqrt(3-x)+sqrt(x^2-1)  domain 3-x>=0         x^2-1>=0
                                   -x>=-3         x^2>=1
                                   x<=3           x>=1 and x>=-1
                                   x<=3     and   x>=1 and x>=-1

                                             *------*-----*
                                   ---------------------------
                                             -1  0  1  2  3
                                   
                                   THE SECOND INEQUALITY IS WRONG:

                                   x^2>=1
                                   sqrt(x)>=sqrt(1)  -- sqrt(x) means x could be -x or x (-5^2 = 5^2 = 25)
                                   -x>=1 and x>=1
                                   x<=-1 and x>=1

                                   so the real answer is x<=3 and x<=-1 and x>=1

                                      <-------*      *-----*
                                   ---------------------------
                                             -1  0  1  2  3

  b) sqrt(3-x)-sqrt(x^2-1)  domain is the same as above, for the same reason as above.

  c) sqrt(3-x)*sqrt(x^2-1)  domain is the same as above, for the same reason as above
                            i'd originally thought there'd be some exponent/root rules applied but this wasn't the case

  d) sqrt(3-x)/sqrt(x^2-1)  for numerator: x<=3 for same reason as above
                            for denominator: x<=-1 and x>=1 for same reason as above
                                             BUT, denom can't be 0, meaning sqrt(x^2-1)!=0
                                                  sqrt(a)=0 when a=0 -- when does x^2-1=0?
                                                                                  (x+1)(x-1)=0
                                                  when x=1 and x=-1, x^2-1=0
                                                  x=1 and x=-1 need to be removed from domain
                                                  MEANING ...
                                                  x<=-1 and x>=1 BUT x!=1 and x!=-1
                                                  SIMPLIFYING TO...
                                                  x<-1 and x>1
                                             x<-1 and x>1 

                            domain is x<=3 and x<-1 and x>1

33a) f(g(x)) = g(x^2+x) = 3(x^2+x)+5 = 3x^2+3x+5 domain:all x
  b) g(f(x)) = g(3x+5) = (3x+5)^2+(3x+5)
                         (3x+5)(3x+5)+(3x+5)
                         9x^2+15x+15x+25+3x+5
                         9x^2+33x+30 domain: all x
  c) f(f(x)) = f(3x+5) = 3(3x+5) = 6x+15 domain:all x
  d) g(g(x)) = g(x^2+x) = (x^2+x)^2+(x^2+x)
                        = (x^2+x)(x^2+x) + x^2+x
                        = x^4+x^3+x^3+x^2+x^2+x
                        = x^4+2x^3+2x^2+x domain: all x

34) skip -- no operation in here indicates that the domain will be anything other than all x for all sub-questions

35a) f(g(x)) = f(4x-3) = sqrt((4x-3)+1)
                       = sqrt(4x+2)  domain: 4x+2>=0
                                             4x>=-2
                                             x>=-1/2
  b) g(f(x)) = g(sqrt(x+1)) = 4(sqrt(x+1))-3  domain: x+1>=0
                                                      x>=-1
  c) f(f(x) = f(sqrt(x+1)) = sqrt(sqrt(x+1)+1)
                             ((x+1)^(1/2)+1)^(1/2)
                             ((x+1)^(1/2)+1^(1/2))^(1/2)
                             (x+1)^(1/4)+1^(1/4)
                             (x+1)^(1/4)+1
                             root(4, x+1)+1  domain: x+1>=0
                                                     x>=-1
  d) g(g(x)) domain: all x

36a) f(g(x)) = f(x^2+1) = sin(x^2+1)  domain: all x
  b) g(f(x)) = g(sin(x)) = sin(x)^2+1 domain: all x
  c) domain: all x
  d) domain: all x

37a) f(g(x)) = f((x+1)/(x+2)) = (x+1)/(x+2)+1/(x+1)/(x+2)  domain: x!=-2 and (x+1)/(x+2)!=0
                                                                             x!=-1
                                 
                              
                              REMEMBER: the convention is to take the domain from the source expression -- don't re-work it?
  b) g(f(x)) = g(x+(1/x)) = ((x+(1/x))+1)/((x+(1/x))+2)  x != 0 AND (x+(1/x))+2!=0
                                                                    (x+(1/x))!=-2
                                                                    1/x!=-2-x
                                                                    1!=-2x-x^2
                                                                    0!=-2x-x^2-1
                                                                    0!=-x^2-2x-1
                                                                    0!=-(x^2+2x+1)
                                                                    0!=-(x+1)^2
                                                          x !=0 AND x!=-1
                                                          I HAD A VERY HARD TIME WITH THIS
  c) f(f(x)) = f(x+(1/x)) = (x+(1/x))+(1/(x+(1/x))) x != 0 AND x+(1/x) != 0
                                                               x != -1/x
                                                               x^2 != -1
                                                               x != sqrt(-1)
                                                               x IS NOT A REAL NUMBER, meaning that for this case,there is no situation where the denom will be 0
                                                    x != 0 AND (other case is invalid)
  d) g(g(x)) = g((x+1)/(x+2)) = (((x+1)/(x+2))+1)/(((x+1)/(x+2))+2)
                                                    x+2!=0  AND ((x+1)/(x+2))+2!=0
                                                    x!=-2       (x+1)/(x+2)!=-2
                                                                x+1!=-2(x+2)
                                                                x+1!=-2x-4
                                                                x!=-2x-4-1
                                                                x!=-2x-5
                                                                x+2x!=-5
                                                                3x!=-5
                                                                x!=-5/3
                                                    x!=-2 AND x!=-5/3

38a) f(g(x))=f(sin(2x))=sin(2x)/(1+sin(2x))    1+sin(2x) != 0
                                               sin(2x) != -1
                                               sin2x does 1 full cycle every pi
                                               sin2x=-1 is its min point and at (n*pi)+3pi/4
                                               that means, x!=(n*pi)+3pi/4 for any integer n

  b) g(f(x))=g(x/(1+x))=sin(2(x/(1+x)))        x!=-1

  c) f(f(x))=f(x/(1+x))=(x/(1+x))/(1+(x/(1+x))) x!=-1 AND 1+(x/(1+x))!=0
                                                          x/(1+x)!=-1
                                                          x=-(1+x)
                                                          x=-1-x
                                                          2x=-1
                                                          x=-1/2
  
  g) g(g(x))=g(sin(2x))=sin(2(sin(2x)))  domain is all x

39-42) skip -- not useful

43) f(x)=x^4 g(x)=2x+x^2 
44) f(x)=x^2 g(x)=cos(x)
45) f(x)=x/(1+x) g(x)=root(3,x)
46) f(x)=root(3,x) g(x)=x/(1+x)
47) f(x)=sec(x)tan(x) g(x)=x^2
48) f(x)=x/1+x g(x)=tan(x)

49) f(x)=sqrt(x) g(x)=x-1 h(x)=sqrt(x)
50) f(x)=root(8,x) g(x)=2+x h(x)=|x|
51) f(x)=x^2 g(x)=sin(x) h(x)=cos(x)

52) skip -- not useful, you're just mapping numbers

53a)4
  b)3
  c)0
  d)undefined -- no g(x) at x=6
  e)4
  f)-2

54) skip

55a) r(t)=60t
  b) A(t)=pi*r(t)^2

56a) r(t)=2t
  b) V(t)=I DONT KNOW HOW TO CALCULATE VOLUME OF A SPHERE

57a) sin(x)=opposite/hypotenuse cos=adjacent/hypotenuse tan=opposite/adjacent
     we know ...
        opposite = 6km, the distance from the shoreline
        adjacent = distance traveled since noon
      tan(x)=6/d
      x=arctan(6/d) -- x is the angle
     now that you know x (the angle), you know ...
      sin(x)=6/hypotenuse
      hypotenuse*sin(x)=6
      hypotenuse=6/sin(x)
     the hypotenuse is the distance from the boat to the lighthouse
     all together, that makes ...
      f(d)=6/sin(arctan(6/d))
  b) g(t)=30t=d
  c) f(g(t)) where t is hours past noon calculates distance from lighthouse at t hours

58) airplane height=1mile speed=350mile/hr, at t=0 it's over radar station
  a) d(t)=350t
  b) radar station is on the ground, so you have to use a trig function
     1. you know the altitude is 1 mile (vertical, adjacent side)
     2. you know the length flown is 350t (horizontal. opposite side)

     tan(angle) = opposite/adjacent
     tan(angle) = 350t/1
     tan(angle) = 350t
     angle = arctan(350t)

     cos(angle) = adjacent/hypotenuse
     cos(angle) = 1/hypotenuse
     hypotenuse*cos(angle) = 1
     hypotenuse=1/cos(angle)
     hypotenuse=1/cos(arctan(350t))

     f(t)=1/cos(arctan(350t))
  c) d(t)=350t
     f(z)=1/cos(arctan(z))
     f(d(t))=1/cos(arctan(350t))

59a) sketched it
  b) V(t)=120 if t>=0
         =0   if t<0
     V(t) in terms of H(t) is V(t)=120H(t)?
  c) V(t)=240 if t>=5
         =0   if t<5
     V(t)=240H(t)
          240H(t-5)

60a) it's flat up until 0, then its slope changes to 1
  b) skip
  c) skip -- this is just a transformation function

61) f(x)=mx+b g(x)=ax+c f(g(x))=m(ax+c)+b=max+mc+b
    yes it is a linear function
    its slope is ma -- the slope from f(x) and g(x) multipled together

62) A(x)=1.04x
    A(A(x)) = 1.04(1.04x)=(1.04)^2x
    A(A(A(x)))=1.04^3x
    A(A(A(A(x))))=1.04^4x

    1.04^kx, where k is some integer >=1
  
63a) (2x+1)*something=4x^2+4x+7
     you can use polynomial division here?
           2x  +1
     2x+1| 4x^2+4x+7
         - 4x^2+2x
                2x+7
                2x+1
                   6
     i'm not an expert in polynomial division, but just like regular division, the remainder is extra
     this becomes (2x+1)^2+6 -- graphing both the original and this shows that they're the same
    
     g(x)=2x+1
     f(x)=x^2+6
     f(g(x))=(2x+1)^2+6=4x^2+4x+7=h(x)

  b) COULD NOT FIGURE OUT HOW TO DO THIS so i just graphed out the original and transformed g(x)=x^2 until I found a fit
      f(x)=3x+5
      g(x)=(x+0.5)^2-15/12
      f(g(x))=3((x+0.5)^2-15/12)+5

64) f(x)=x+4 h(x)=4x-1
    g(x)=4x-17   <--- found this by playing with graph
    g(f(x))=g(x+4)=4(x+4)-17=4x+16-17=4x-1

65) no? -- g(x)=x^2 f(x)=sqrt(x)  h(x)=f(g(x))
                                      =f(x^2)
                                      =sqrt(x^2)
                                      =x  <--   not even?

66) no? -- g(x)=x  f(x)=x^2       h(x)=f(g(x))
                                      =f(x)
                                      =x^2 <-- not odd?
-->

<!--
---- 1.2 EXERCISES

1a) logarithmic function
 b) root function
 c) rational function
 d) polynomial function of degree 2
 e) exponential function
 f) trigonometric function

2a) exponential function
 b) power function
 c) algebraic function
 d) trigonometric function
 e) rational function
 f) rational function

3a) blue line, even exponent means both prongs pointing up and an exponent of 2 is less steep than an exponent of 8
 b) red line, odd function reflects across both axis
 c) green line, exponent of 8 means more squared off than exponent of 2

4a) G -- only straight line
 b) f -- shape of a exponential function
 c) F -- only odd function, power of 3
 d) g -- root 3 is inverted version of power of 3 (F)

5) 1-sin(x) != 0
   when does sin(x) = 1? pi/2 + n*2pi, for all integers n
   so x!=pi/2+n*2pi where n is an integer

6) 1-tan(x) != 0
   when does tan(x) = 1? pi/4 + n*pi, for all integers n
   so x!=pi/4+n*pi where n is an integer

7a) y=2x+b  -- no need to sketch they're all parallel to each other because the slope is the same
 b) 1=m2+b  -- no need to sketch
 c) 1=2(2)+b
    1-4=b
	-3=b
	y=2x-3

8) f(x)=m(x+3)+1
   if it was just x, the y intercept would be at 1
   since it's x+3, the graph moves to the right by 3 units (where x=0, which was previously the y-intercept, is now x=3)
   meaning that regardless of the slope, the lines intercept at x=3 (instead of x=0)

9) they're all parallel (same slope)?

10) y=x^2  x=0 y=0
           x=1 y=1
		   x=2 y=4
		   x=3 y=9

    y=(x-3)^2  x=3 y=0
	           x=4 y=1
			   x=5 y=4
	
	y=2(x-3)^2  x=3 y=0
	            x=4 y=2

    ----------

	y=-x^2  x=0 y=0
	        x=1 y=-1
			x=2 y=-4
	
	y=-x^2+2  x=0 y=2
	          x=1 y=1
			  x=2 y=-2
	
	y=-n(x+2)^2+2
	1=-n(0+2)^2+2
	1=-n2^2+2
	1=-4n+2
	1-2=-4n
    -1=-4/n
	1/4=n

	y=-(1/4)(x+2)^2+2

11) f(x)=ax^3+bx^2+cx+d

    6=a(1)^3 +b(1)^2 +c(1) +(1)
	0=a(-1)^3+b(-1)^2+c(-1)+(-1)
	0=a(0)^3 +b(0)^2 +c(0) +(0)
	0=a(2)^3 +b(2)^2 +c(2) +(2)

	4 equations with 4 variables, you can solve this?

12a) slope is the rate at which temp is increasing
     t-intercept is temp at 1900?
  b) 0.02(200)+8.50 -- 12.5 celsius

13a) c=0.0417D(a+1)
     c=0.0417(200)(a+1)
	 c=8.34a+8.34

	 slope=8.34, its the shift in dosage by age?
  b) 8.34mg?

14a) y=-4x+200  (x dollars means he can rent out y spaces)
     no point in graphing

  b) y-intercept: x=0 is the x (dollar amount) at which all spaces will be rented out
     x-intercept: y=0 is the x (dollar amount) at which no spaces will be rented out
	 slope: the ratio of dollar amount to space rented out (e.g. for each every 4 dollar increase, 1 less space can be rented out?)

15a) no
  b) ratio of celsius to fahrenheit
     F-intercept is fahrenheit at 0 celsius?

16a) x=50 y=40 -- y=mx+b -- y=4x/5+0
  b) done
  c) 4/5 -- 4 miles traveled every 5 mins

17a) m=(173-113)/(80-70)=60/10=6/1=6
     y=6x+b             y=6x+b
     173=6(80)+b        113=6(70)+b
     173-6(80)=b        113-6(70)=b
     -307=b

     y=6x-307
   b) 6
   c) 150=6(x)-307
      150+307=6x
	  (150+307)/6=x

18a) y=$2200 makes x=100 chairs, y=$4800 makes x=300 chairs
     m=(4800-2200)/(300-100)=13

	 y=13x+b
	 2200=13(100)+b
	 2200=1300+b
	 2200-1300=b
	 900=b

	 y=13x+900

  b)13/1 -- dollars spent for each chair
  c)the dollar amount at which you'll make no chairs

19) surface, water pressure = air pressure -- 15lb/in^2
    below surface, water pressure increases by 4.34lb/in^2 for every 10 feet

  a) m=4.34/10=0.434
     y=0.434x+b
	 15=0.434(0)+b
	 15=b

	 y=0.434x+15

  b) 100=0.434x+15
     100-15=0.434x
	 85=0.434x
	 x=85/0.434=~195.85 feet

20)  monthly cost depends on miles driven
     drive 480, cost 380
	 drive 800, cost 460

  a) C(d)=md+b
     m=(460-380)/(800-480)=0.25
      
     C(d)=0.25d+b
	 380=0.25(480)+b
	 260=b

	 C(d)=0.25d+260

   b) C(1500)=635
   c) not graphing, but slope is dollars per mile?
   d) the point at which you can't drive? you need more than this to operate the car
   e) maybe? depends what costs you're factoring in, some of htem might not be linear (e.g. the cost to repair a car gets more and more the more wear you put on the car)

21a) trig function
  b) linear function (polynomial function of degree 1 aka algebraic function?)

22a) polynomial function of degree 2 (aka algebriac function?)
  b) logarithmic function

23a) linear is appropriate
  b) m=(8.2-14.1)/(60-4)=−0.105357143
     y=−0.105357143x+b
	 8.2=−0.105357143(60)+b
	 8.2=−6.32142858+b
	 8.2+6.32142858=+b
	 14.52142858=b
	 y=−0.105357143x+14.52142858
  c) done
  d) 11.45
  e) 6 in 100, or 6%
  f) no, at some point it probably starts to flatten

24-25) skip -- same thing as 23

26c) the number of mice that develop tumors when there's no asbestos?

27-28) skip

29) I guess it depends on how far back you're starting point is? closer you get to x=0, the more illumination you get? thats what the curve looks like

30) larger, more species
    S is num of bats
	A is area
	S=0.7A^0.3

  a) S=0.7(60)^0.3
     S=2.39
  b) 4=0.7(A)^0.3
     5.714=A^(3/10)
	 5.714^(10/3)=A
	 333.529=A

31a) am i supposed to do this through trial-and-error? if so, i got 0.00067*x^1.15
  b) 0.456 -- this is wrong, the function 0.00067*x^1.15 is a poor fit

  it sounds like you can use linear regression to for a power function, but you need to apply logarithms to various parts of the equation to get it linear? this is for exponential and power functions. there's also polynomial regression, logistic regression, etc..

32) skip
-->

<!--
---- 1.1 EXERCISES

1. yes
2. no

3a) 3
3b) -0.25
3c) 3
3d) -0.75
3e) domain=[-2,4] range=[-1,4]

4a) -2 4
 b) -2 2
 c) -3 and 4
 d) [0,4]
 e) [-4,4]
 f) [-4,3]

5) [-75,140]

7) no
8) yes
9) yes
10)no

11a)13
  b) ~1990-1995
  c) smallest=~1910 largest=final year in graph
  d) [-11.5,16]

12a) (0,1.6]
  b) trees growing faster in 1900s; yes?

13) ice melts making the water colder, water gets cold relatively rapidly? then reaches a low point, then moves back to room temp

14) A win, everyone finished (reached 100 meters).
    C kept a consistent pace
    B bursted in the beginning, stopped, then bursted again
	C started slow and sped up in the middle

15a) 500mw
  b) around 3-4am -- yes they seem reasonable

23b) ~68.5

26) v(r)=1.25pir^3
    v(r+1)1.25pi(r+1)^3

	1.25pi(r+1)^3-1.25pir^3=a
	(r+1)^3-r^3=a/(1.25pi)
	(r^2+2r+1)(r+1)-r^3=a/(1.25pi)
	(r^3+2r^2+r+r^2+2r+1)-r^3=a/(1.25pi)
	(r^3+3r^2+3r+1)-r^3=a/(1.25pi)
	3r^2+3r+1=a/(1.25pi)
	(3r^2+3r)+1=a/(1.25pi)
	3(r^2+r)+1=a/(1.25pi)
	3(r^2+r-2)+1-6=a/(1.25pi)
	3(r^2-1r+2r-2)+1-6=a/(1.25pi)
	3(r(r-1)+2(r-1))+1-6=a/(1.25pi)
    3(r-1)(r+2)+5=a/(1.25pi)
	4pi/3*3(r-1)(r+2)+5=a
	4pi(r-1)(r+2)+5=a

	I think this is right? a is the amount of extra air needed to go for r to r+1

27) f(x)=-x^2+3x+4

    (f(3+h) - f(3)) / h
    (f(3+h) - 4) / h
	(-9-6h-h^2+9+3h+4 - 4) / h
	(-3h-h^2) / h
	h(-3-h) / h
	-3-h

30) f(x)=(x+3)/(x+1)

    (f(x)-f(1))/(x-1)
    (((x+3)/(x+1))-2)/(x-1)
	(((x+3)/(x+1))-2(x+1)/(x+1))/(x-1)
	(((x+3)-2(x+1))/(x+1))/(x-1)
	... dont want to bother with the rest of this, but i think i know what i have to do

31) x!=-3,+3
32) x^2+x-6=(x+3)(x-2)  x!=-3,2
33) root(3, 2t-1) -- x in reals?
34) t>=3
35) x^2-5x=x(x-5)  x!=0 (because of 1st factor) AND x>=5 (because of 2nd factor) AND x>5 (because quad root will be 0 when x=5, meaning the denominator will be 0 which is invalid).  x>5 covers all the other cases, so x>5 is the domain
36) u != -1  AND 1+1/u+1 != 0, which means u != -2 -- so, u != -1 and -2
37) p >= 0 AND p >= 4

38) sqrt(4-x^2)
    sqrt(-(-4+x^2))
    sqrt(-(x^2-4))
	sqrt(-(x+2)(x-2))  -- the domain is [-2,2]

39) all reals
40) t!=-1

51-52) these are lines -- subtract to get the slope, then solve the y-intercept (b)
       limit the domain explicit to the bounds given
53) (y-1)^2=-x
    y-1=sqrt(-x)
	y=sqrt(-x) + 1

	this is the top half, so the bottom half would be ...

	y=-(sqrt(-x) - 1) you subtract 1 to get the origin to the same place

    THIS IS WRONG. ocrrect answer is 1-sqrt(-x)?? looks like i almost got it right?

54) (y-2)^2=4-x^2
    y-2=+-(4-x^2)^0.5
	y=+-(4-x^2)^0.5+2

    you want the top one, so the answer is y=(4-x^2)^0.5+2?

55-56) unsure about these? but looks like abs is involved

57) 2w+2h=20
    2h=20/w
	h=10/w

	so the answer is f(w)=2w+10/w

58) w*h=16
    h=16/w

	so the answer is f(w)=w*16/w

59) area of an equilateral traingle is A=sqrt(3)a^2/4

    f(a)=sqrt(3)a^2/4

60) w*2w*h=8
   2w^2*h=8
   h=8/(2w^2)
   h=4/(w^2)

   f(w)=4/(w^2)

61) w*w*h=2
    h=2/(w^2)
    
	f(w)=w*w+4(w*h)
	f(w)=w^2+4(w*(2/(w^2)))
	f(w)=w^2+4(2w/w^2)
	f(w)=w^2+4(2/w)
	f(w)=w^2+(8/w)

62) perimeter: 2x+h+pir=30
    area:      x*h+pir^2

	r=x/2

    perimeter: 2x+h+pi(x/2)=30
    area:      x*h+pi(x/2)^2

	2x+h+pi(x/2)=30
	h+pi(x/2)=30-2x
	h=30-2x-pi(x/2)

    f(x) = x*(30-2x-pi(x/2))+pi(x/2)^2
	     = 30x-2x^2-(pix^2)/2 + pi(x/2)^2
		 = 30x-2x^2-(pix^2)/2 + pi(x^2/4)
		 = 30x-2x^2-(2pix^2)/4 + pi(x^2/4)

		 something like this, there's probably more simplication that can be done

63) area with cutouts: 12*20-4x^2
    volume: (20-2x)*(12-2x)*x

	f(x)=(20-2x)*(12-2x)*x

64) $35/month 400mins free + 10cents per min'

    f(x) = 35      if x in [0,400]
	       35+0.1x if x in (400,600]

65) 65mi/h max on freeway, $15 for each mile above max
    
    F(x) = 0    if x in [0,65]
	       x*15 if x in (65,100]

69) f is odd (symmetric across y, where mirroed portion is flipped across x) and g is even (symmetric across y-axis)

70) f is neither odd nor even? mirrored portion needs to be flipped across x, g is even
pg23

71a) (-5,3)
  b) (-5,-3)

72) skipped as too obvious

73) odd
74) even 
75) none? got it right
76) odd  -- got it wrong, forgot to apply negative sign properly
77) 1+ 3x^2-x^4 -- i don't know, if i were to guess i'd say even because exponents are eve n
78) 1+ 3x^4-x^5 -- gonna say odd, same reason as above

79) yes? -- you're jsut adding the y coordinates together, both of which are even meaning the result will also be even
    yes? -- you're just adding the y coordinates together
	no? -- uneven displacement between the quadrants

80) yes? -- you're jsut multing the y coordinates together, both of which are even meaning the result will also be even
    yes? -- same reasoning, you're displacing the similarly across the relevant quadrants
	no? -- looks like i mightb e wrong on this one
-->

<!--
Diagnostic tests

1a) (-3)^4  = -3*-3*-3*-3=9*9=81
1b)  -(3^4) = -(3*3*3*3)=-91
1c) 3^(-4) = 1/(3^4) = 1/91
1d) 5^23 / 5^21 = 5^2 = 25
1e) (2/3)^(-2) = 1/((2/3)^(2)) = 1/(4/9) = 9/4
1f) 16^(-3/4) 
    16^(-2/4) * 16^(-1/4)
	1/(16^(2/4)) * 1/(16^(1/4))
	1/(16^(1/2)) * 1/(16^(1/4))
	1/sqrt(16)*+ 1/root(4, 16)
	1/4 * 1/2
	1/8
	
	difficult - screwed it up a few times but got at it the end
	
2a) sqrt(200) - sqrt(32)
	200^(1/2) - 32^(1/2)
	(2*2*2*25)^(1/2) - (2*2*2*2*2)^(1/2)
	(4*2*25)^(1/2) - (4*4*2)^(1/2)
	(4*2*25)^(1/2) - (4*4*2)^(1/2)
	(4^(1/2))*(2^(1/2))*(25^(1/2)) - (4^(1/2))*(4^(1/2))*(2^(1/2))  WHAT IS THIS RULE? WHERE EXPONENT IS BEING DISTRIBUTED?
      i've went through this and this makes sense: x^2*y^2 = (x*y)^2
                                                   x*x*y*y
                                                   x*y*x*y
                                                   (x*y)*(x*y)
                                                   (x*y)^2
	2*(2^(1/2))*5 - 2*2*(2^(1/2))
	10*(2^(1/2)) - 4*(2^(1/2))
	(2^(1/2))*(10-4)
	(2^(1/2))*6
	6*sqrt(2)
2b) (3a^3b^3)*(4ab^2)^2
    (3a^3b^3)*(16a^2b^4)
	3*a^3*b^3*16*a^2b^4
	48*a^3*b^3*a^2b^4
	48*a^5*b^7
2c) ((3*x^(3/2)*y^3)/(x^2*y^(-1/2)))^-2
    1/(((3*x^(3/2)*y^3)/(x^2*y^(-1/2)))^2)
	1/((9*x^3*y^6)/(x^4*y^-1))
	1/(9*x^-1*y^7)
	1/(9*(1/x)*y^7)
	1/((9*y^7)/x)
	x/(9*y^7)

3a) 3(x+6)+4(2x-5)
    3x+18+8x-20
	11x-2
	
3b) (x+3)(4x-5)
    4x^2-5x+12x-15
	4x^2+7x-15

3c) (sqrt(a)+sqrt(b))(sqrt(a)-sqrt(b))
	a-sqrt(a)sqrt(b)+sqrt(a)sqrt(b)-b
	a-b

3d) (2x+3)^2	
    (2x+3)(2x+3)
	4x^2+6x+6x+9
	4x^2+12x+9

3e) (x+2)^3
    (x+2)(x+2)(x+2)
	(x^2+4x+4)(x+2)
	x^3+4x^2+4x+2x^2+8x+8
	x^3+6x^2+12x+8
	
FACTORING FAIL: SECTION 4 NEEDS REVIEW
	
4a) 4x^2-25
    4x^2+0x-25
    (x+5)(x-5)
    
4b) 2x^2+5x-12
    2x^2+5x-12                a*c=-12  a+c=5   -24=1,24,2,12,3,8
	2x^2+8x-3x-12
	2x(x+4)-3(x+4)
	(2x-3)(x+4)
	
	DIFFICULT - LOOK UP THE GROUPING METHOD FOR FACTORING

4c) x^3-3x^2-4x+12
    x^2(x-3)-4(x-3)
	(x^2-4)(x-3)
	(x+2)(x-2)(x-3)

4d) x^4+27x
    x(x^3+27)
	x(x^3+3^3)
	
	NOT SURE WHAT TO DO HERE -- answer is x(x+3)(x^2-3x+9)
	
4e) 3x^(3/2)-9x^(1/2)+6x^(-1/2)
    x^1/2*(3x^3-9x+6x^(-1))
    x^1/2*(3x^3-9x+6/x)
	
	NOT SURE WHAT TO DO HERE -- 3x^(-1/2)(x-1)(x-2)
	
4f) x^3y-4xy
    xy(x^2-4)
	xy(x+2)(x-2)
	
	
5a) (x^2+3x+2)/(x^2-x-2)
    ((x+1)(x+2))/((x+1)(x-2))
	(x+2)/(x-2)
	
5b) (2x^2-x-1)/(x^2-9) * (x+3)/(2x+1)
	(2x^2-x-1)/((x+3)(x-3)) * (x+3)/(2x+1)
	((2x+1)(x-1))/((x+3)(x-3)) * (x+3)/(2x+1)
	((x+3)(2x+1)(x-1))/((x+3)(x-3)(2x+1))
	((2x+1)(x-1))/((x-3)(2x+1))
	(x-1)/(x-3)
	
5c) x^2/(x^2-4) - (x+1)/(x+2)
    x^2/((x+2)(x-2)) - (x+1)/(x+2)
	x^2/((x+2)(x-2)) - ((x+1)(x-2))/((x+2)(x-2))
	(x^2-(x+1)(x-2))/((x+2)(x-2))
	(x^2-(x^2-1x-2))/((x+2)(x-2))
	(x^2-x^2+1x+2)/((x+2)(x-2))
	(x+2)/((x+2)(x-2))
	1/(x-2)
	
5d) (y/x-x/y)/(1/y-1/x)
    (yy/xy-xx/xy)/(1/y-1/x)
	(y^2/xy-x^2/xy)/(1/y-1/x)
	((y^2-x^2)/xy)/(1/y-1/x)
	((y^2-x^2)/xy)/(1x/yx-1y/xy)
	((y^2-x^2)/xy)/(x/yx-y/xy)
	((y^2-x^2)/xy)/((x-y)/xy)
	((y^2-x^2)/xy)/((x-y)/xy)
	((y^2-x^2)/xy)*(xy/(x-y))
	(y^2-x^2)/(x-y)     I GOT UP TO HERE, THEN I HAD TO LOOK AT THE ANSWER TO FIGURE OUT HTERES MORE TO DO
	(y-x)(y+x)/(x-y)
	(y-x)(y+x)/(-y+x)
	(y-x)(y+x)/-(y-x)
	(y+x)/-1
	-(y+x)
	
6a) sqrt(10)/(sqrt(5)-2)
    10^(1/2)/(5^(1/2)-2)
	((2*5)^(1/2))/(5^(1/2)-2)
	(2^(1/2)*5^(1/2))/(5^(1/2)-2)  HOW DOES THIS LEAP HAPPEN?
	(2^(1/2)*5^(1/2)*(5^(1/2)+2))/((5^(1/2)-2)*(5^(1/2)+2))
	(2^(1/2)*5^(1/2)*(5^(1/2)+2))/(5+2*5^(1/2)-2*5^(1/2)-4)
	(2^(1/2)*5^(1/2)*(5^(1/2)+2))/(5-4)
	(2^(1/2)*5^(1/2)*(5^(1/2)+2))/1
	(2^(1/2)*5^(1/2)*(5^(1/2)+2))
	(2^(1/2)*(5+2*5^(1/2)))
	((5*2^(1/2)+2*5^(1/2)*2^(1/2)))
	((5*2^(1/2)+2*10^(1/2)))
	((5*sqrt(2)+2*sqrt(10)))
	
6b) (sqrt(4+h)-2)/h
    ((4+h)^(1/2)-2)/h
	
	UNSURE WHAT THIS IS ASKING FOR -- "Rationalize the expression and simplify"?
	
7a) x^2+x+1
    x^2+x=-1
	x^2+x+0.25=-1+0.25
	x^2+0.5x+0.5x+0.25=-1+0.25
	x(x+0.5)+0.5(x+0.5)=-1+0.25
	(x+0.5)*(x+0.5)=-1+0.25
	(x+0.5)^2=-1+0.25
	(x+0.5)^2=-0.75
	(x+0.5)^2+0.75

    I FORGOT WHAT COMPLETING THE SQUARE IS ACTUALLY FOR? THIS IS A GRAPH TRANSFORMATION OR SOMETHING?
	LOOK UP COMPLETING THE SQUARE
	
7b) 2x^2-12x+11
    2x^2-12x=-11
	2(x^2-6x)=-11
	2(x^2-3x-3x+9)=-11+2*9
	2(x(x-3)-3(x-3))=-11+2*9
	2((x-3)(x-3))=-11+2*9
	2(x-3)^2=-7
	2(x-3)^2-7
	
	LOOK IN TO COMPLETING THE SQUARE AGAIN
	
8a) x+5=14-0.5x
    x=14-0.5x-5
	x+0.5x=14-5
	1.5x=9
	3x/2=9
	3x=18
	x=6
	
8b) 2x/(x+1) = (2x-1)/x
    2x^2/(x+1) = (2x-1)
	2x^2 = (2x-1)(x+1)
	2x^2 = 2x^2+2x-x-1
	2x^2 = 2x^2+x-1
	0 = x-1
	x = 1
	
8c) x^2-x-12=0
    x^2+3x-4x-12=0
	x(x+3)-4(x+3)=0
	(x-4)(x+3)=0
	x=4 or -3
	
8d) 2x^2+4x+1=0
    2x^2+4x=-1
	2(x^2+2x)=-1
	2(x^2+1x+1x+1)=-1+2
	2(x(x+1)+1(x+1))=-1+2
	2((x+1)(x+1))=-1+2
	2(x+1)^2=1
	(x+1)^2=1/2
	x+1=+/-sqrt(1/2)
	x=+/-sqrt(1/2)-1
	
	I THINK THE IDEA IS RIGHT BUT THE ANSWER IS WRONG
	
8e) x^4-3x^2+2=0
    x^4-3x^2=-2
	x^2(x^2-3)=-2
	x^2(x^2-3)+2=0
	
	?????????? UNABLE TO FIND x
	
8f) ?????????? Unsure how to deal with abs() in equality

8g) 2x(4-x)^(-1/2)-3sqrt(4-x)=0
    1/(2x(4-x)^(1/2))-3sqrt(4-x)=0
	1/(2x(4-x)^(1/2))-3*((4-x)^(1/2))=0
	1/(2x(4-x)^(1/2))=3*((4-x)^(1/2))
	1/(2x(4-x)^(1/2))*1/3=((4-x)^(1/2))
	1/3*(2x(4-x)^(1/2))=((4-x)^(1/2))
	1=((4-x)^(1/2))*3*(2x(4-x)^(1/2))
	1=3*((4-x)^(1/2)*2x(4-x)^(1/2))
	1=3*(4-x)^(1/2)*(1*2x)
	1=3*(4-x)^(1/2)*2x
	1=2x*3*(4-x)^(1/2)
	1=6x*(4-x)^(1/2)
	1/6x=(4-x)^(1/2)
	(1/6x)^2=4-x
	1/6x^2=4-x
	1=(4-x)6x^2
	1=24x^2-6x^3
	1=-6x^3+24x^2
	1=-6x(x^2+4x)
	1-24x=-6x(x^2+2x+2x+4)
	1-24x=-6x(x(x+2)+2(x+2))
	1-24x=-6x((x+2)(x+2))
	1-24x=-6x(x+2)^2
	
	UNSURE WHAT TO DO AFTER THIS POINT TO SOLVE x?
	
9) STUDY INEQUALITIES
	
10a) false

10b) THOUGHT THIS WAS FALSE BUT ITS TRUE? LOOK AT ITuP

     sqrt(ab) = sqrt(a)sqrt(b)
	 (ab)^(1/2) = a^0.5*b^0.5

10c) false -- distance

10d) false
	
10e) false

10f) (1/x)/(a/x-b/x)
     (1/x)/(a*1/x-b*1/x)
	 (1/x)/((1/x)*(a-b))
	 1/(1*(a-b))
	 1/(a-b)
	 
	 it's true but it's tough to know just by looking at it
	 
	 
	 
1a) -5=-3*2+b
    -5=-6+b
	-5+6=b
	1=b
	y=-3x+b
	
1b) y=0x-5

1c) x=2

1d) -4y=3-2x
    -4y=-2x+3
	y=0.5x-0.75
	
	y=0.5x+b
	-5=0.5(2)+b
	-5=1+b
	-6=b
	
	y=0.5x-6
	
2) (x-h)^2+(y-k)^2 = r^2
   (x+1)^2+(y-4)^2 = r^2
   
   r=sqrt((3--1)^2+(-2-4)^2)
   r=sqrt(4^2+(-6)^2)
   r=sqrt(16+36)
   r=sqrt(52)
   r^2=52
   
   (x+1)^2+(y-4)^2 = 52

3) x^2 +y^2 - 6x + 10y + 9 = 0
   x^2-6x + y^2+10y + 9 = 0 
   x^2-6x+9 + y^2+10y+25 = 25
   (x-3)^2 + (y+5)^2 = 25
   
   x=3 y=-5 r=5
   
 
4a) -12-4 / 5--7
    -16/12
    -4/3

4b) y=(-4/3)x+b
    -12=-(4/3)5+b
	-12=-20/3+b
	-12+(20/3)=b
	-36/3+20/3=b
	-16/3=b
	y=(-4/3)x-(16/3)
	
	y-intercept=b=-16/3
	x-intercept=(4x/3)=-16/3
	            4x=-16
				x=-4
				
4c) diff-x=(5--7)/2=(5+7)/2=12/2=6   mid-x = -7+6=-1
    diff-y=(-12-4)/2=-16/2=-8        mid-y = 4+(-8)=-4
	
4d) sqrt((5--7)^2+(-12-4)^2)
    20
	
4e) perpendicular slope = 4/3
    midx=-1 mid-y=-4
	
	y=4/3x+b
	-4=(4/3)(-1)+b
	-4=-4/3+b
	-4+4/3=b
	-12/3+4/3=b
	-8/3=b
	
	y=(4/3)x-(8/3)
	y-(4/3)x=-8/3
	3y-4x=-8?
	
	ALMOST RIGHT? b is wrong but maybe I miscalculated slope?
	
5) ALL QUESTIONS UNDERSTOOD

1a) -2
1b) 2.75
1c) -3,1
1d) -2.5,0.4
1e) domain=[-3,3] range=[-2,3]

2) ((2+h)^3 - 2^3)/h
   ((2+h)(2+h)(2+h)-8)/h
   ((4+4h+h^2)(2+h)-8/h
   ((8+8h+h^2+4h+4h^2+h^3)-8)/h
   (8h+h^2+4h+4h^2+h^3)/h
   (12h+5h^2+h^3)/h
   h^2+5h+12
   
3a) x^2+x-2
    x^2+1x-2x-2
	(x+1)(x-2)
	
	x can't be -1 or 2
	
3b) denominator is okay
    root(3, x) is okay
	
3c) (4-x)^0.5 + (x^2-1)^0.5
    (4-x)^0.5 + ((x+1)(x-1))^0.5
	(4-x)^0.5 + ((x+1)^1(x-1)^1)^0.5
	(4-x)^0.5 + (x+1)^0.5(x-1)^0.5
	
	x can't be 4,-1,or 1?
	
	THIS IS WRONG
	
4a) flip across x-axis
4b) smoosh it horizontally by half and shiftdown by 1
4c) move it right by 3 and shift up by 1

5a-f) OKAY
5g) FAILED TO IDENTIFY GRAPH
5h) FAILED TO IDENTIFY GRAPH

6a) f(-2)=1--2^2=1-4=3
    f(1)=2(1)+1=2+1=3
	
6b) GOT THIS CORRECT

7) FAILED THIS. UNFAMILIAR NOTATION

1a) pi=180
    pi/180=1
    300*(pi/180)
   
1b) (360-18)*(pi/180)

2a) pi=180
    5pi/6
	5*180/6
	900/6
	300/2
	150
	
2b) pi/180 is the radians for 1 degree
    x*(pi/180)=2
	x*pi=360
	x=360/pi
	
FAILED BOTH 1 AND 2

3) FAIL I DONT KNOW THIS

4) FAIL I DONT KNOW THIS

FAILED BOTH 3 AND 4

5) soh cah toa
   sin(theta)=a/24
   24*sin(theta)=a
   
   cos(theta)=b/24
   24*cos(theta)=b
   
6) FAIL I DONT KNOW THIS

7) FAIL I DONT KNOW THIS

8) FAIL I DONT KNOW THIS

9) almost
-->
