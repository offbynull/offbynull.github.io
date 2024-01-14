```{toc}
```

# Review

## Factoring Polynomials

To factor a quadratic `{kt} ax^2+bx+c`, find two numbers r and s such that when ...

 * added, `{kt} ar+s=b`.
 * multiplied, `{kt} rs=c`.

`{kt} ax^2+arx+sx+rs = ax(x+r)+s(x+r) = (ax+s)(x+r)`

For example, `{kt} 2x^2-7x-4 = 2x^2-8x+1x-4 = (2x+1)(x-4)`.

Factoring quadratics is useful for finding their roots_POLY (where x=0) as well as algebraic manipulations such as simplifying.

```{note}
You often see explained online for the special case where a=1: `{kt} x^2+bx+c`, which means you're trying to find two numbers r and s where `{kt} r+s=b` and `{kt} rs=c`...

 * added, equal b: `{kt} r+s=b`.
 * multiplied, equal c: `{kt} rs=c`.

`{kt} x^2+rx+sx+rs = x(x+r)+s(x+s) = (x+r)(x+s)`.
```

Expressions that follow the pattern ...

 * `{kt} a^2-b^2`, called difference of squares, factor as `{kt} a^2-b^2 = (a-b)(a+b)`.
 * `{kt} a^3-b^3`, called difference of cubes, factor as `{kt} a^3-b^3 = (a-b)(a^2+ab+b^2)`.
 * `{kt} a^3+b^3`, called sum of cubes, factor as `{kt} a^3+b^3 = (a+b)(a^2-ab+b^2)`.

## Completing the Square

To complete the square for a `{kt} ax^2+bx+c`, begin by pulling out a from first two terms: `{kt} a(x^2+\frac{b}{a}x)+c`.

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

Completing the square is useful because it gets your equation into graph transformation format. For the example above, just by looking at the completed formula `{kt} 2(x-3)^2-7` you can tell that it's a parabola ...

 * shifted down by 7.
 * shifted right by 3.
 * stretched up by 2 times.

```{note}
The material also mentions that this is useful for integrating rational functions.
```

## Quadratic Formula

The quadratic formula determines the x-intercepts of a quadratic (where `{kt} ax^2+bx+c=0`, as in where the quadratic evaluates to 0, also called roots_POLY): `{kt} x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}`. For example, the quadratic `{kt} 2x^2-7x-4` has the x-intercepts `{kt} x=\frac{-(-7)\pm\sqrt{(-7)^2-4(2)(-4)}}{2(2)}=\frac{7\pm\sqrt{81}}{4}=\frac{7\pm9}{4}=\{-0.5,4\}`.

`{kt} b^2-4ac` is referred to as the discriminant. When the discriminant is ...

 * `{kt} b^2-4ac > 0`, there are two real roots_POLY.
 * `{kt} b^2-4ac = 0`, there's one real root_POLY.
 * `{kt} b^2-4ac < 0`, there's no real root_POLY.

The last case is a quadratic that can't be factored. A quadratic that can't be factored is called irreducible.

The quadratic formula is derived by completing the square:

```{kt}
ax^2+bx+c=0 \\
ax^2+bx=-c \\
x^2+\frac{b}{a}x=\frac{-c}{a} \\
x^2+\frac{b}{a}x+(\frac{b}{2a})^2=\frac{-c}{a}+(\frac{b}{2a})^2 \\
(x+\frac{b}{2a})^2=\frac{-c}{a}+(\frac{b}{2a})^2 \\
(x+\frac{b}{2a})^2=\frac{-c}{a}+\frac{b^2}{4a^2} \\
(x+\frac{b}{2a})^2=\frac{-4ac}{4a^2}+\frac{b^2}{4a^2} \\
(x+\frac{b}{2a})^2=\frac{-4ac+b^2}{4a^2} \\
(x+\frac{b}{2a})^2=\frac{b^2-4ac}{4a^2} \\
x+\frac{b}{2a}=\pm\sqrt(\frac{b^2-4ac}{4a^2}) \\
x=\pm\sqrt(\frac{b^2-4ac}{4a^2})-\frac{b}{2a}
```

```{note}
The completing the square step is from step 2 to 3.
```

## Binomial Theorem

The binomial theorem is used for quickly expanding expressions in the form `{kt} (a+b)^n` where k is a positive integer: `{kt} (a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k`.

```{note}
`{kt} \binom{n}{k}` is "k choose n", something covered in statistics / probability theory / combinatorics. For now, just know `{kt} \binom{n}{k} = \frac{n!}{k!(n-k)!}`.
```

For example, ...

 * `{kt} (a + b)^2 = a^2+2ab+b^2`
 * `{kt} (a + b)^3 = a^3+3a^2b+3ab^2+b^3`
 * `{kt} (a + b)^4 = a^4+4a^3b+6a^2b^2+4ab^3+b^4`
 * etc..

## Polynomial Division

Polynomial division is a process that breaks a polynomial into two factors, given that one of the factors is already known. The process works similarly to long division in that you're dividing the polynomial by that known factor to determine the other factor. For example, consider the polynomial `{kt} 2x^3+x^2-6x-8`. If you already know that `{kt} (x-2)` is a factor, you can divide the polynomial by that known factor to determine the other factor:

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

 * Rational root theorem: Assuming `P(x)` is a polynomial with integer coefficients, a root_POLY of the equation `{kt} P(x)=0` can be expressed in the form `{kt} \frac{p}{q}`, where ...
 
   * p is a factor of the constant term.
   * q is a factor of the leading coefficient.
 
   In other words, you can find a factor by testing all possible `{kt} \frac{p}{q}` to see if it's a root_POLY / factor of the polynomial. For example, the polynomial `{kt} P(x)=2x^3+x^2-6x-8` has ...

   * constant term factors p={-8,-6,-4,-2,-1,1,2,4,6,8}.
   * leading coefficient factors q={1,2}.

   Testing possible `{kt} \frac{p}{q}` within `P(x)` shows that `{kt} \frac{4}{2}=2` is a root_POLY: `{kt} P(2) = 0`. Since `{kt} 2` is a root_POLY, `{kt} (x-2)` is a factor.
   
   ```{note}
   It's called "rational root theorem" because the coefficients have to be rational / real numbered coefficients? (e.g. coefficients can't be an imaginary or complex number).
   ```

You can use the methods described above to iteratively pull out roots_POLY using polynomial division until the entire polynomial is factored. For example, ...

 1. use rational root theorem to determine `(x-2)` is a factor of `{kt} x^3-3x^2-10x+24`.
 2. use polynomial division to factorize `{kt} x^3-3x^2-10x+24` to `{kt} (x-2)(x^2-x-12)`.
 3. use rational root theorem to determine `(x-4)` is a factor of `{kt} x^2-x-12`.
 4. use polynomial division to factorize `{kt} x^2-x-12` to `{kt} (x-2)(x-4)`.

`{kt} x^3-3x^2-10x+24 = (x-2)(x-2)(x-4)`.


# Terminology

* `{bm} quadratic` - An expression where the highest exponent on the top-level terms is 2. For example, `{kt} 2x^2+4x+4` is a quadratic.

* `{bm} root/(roots?)_POLY/i` - Given a polynomial `P(x)`, its roots_POLY are x values where `{kt} P(x)=0`. If you were to graph `P(x)`, the roots_POLY would be values of x that touch the x-axis.

  ```{note}
  Tough thinking about this? Think of it as finding the x-coordinate values on the graph `{kt} y=ax^2+bx+c` at `y=0`.
  ```

* `{bm} quadratic formula` - A formula determines a quadratic's roots_POLY: `{kt} x=\frac{-b\pm\sqrt{b^2-4ac}{2a}`.

* `{bm} discriminant` - The expression `{kt} b^2-4ac` within the quadratic formula. When the discriminant is ...

  * `{kt} b^2-4ac > 0`, there are two real root_POLYs.
  * `{kt} b^2-4ac = 0`, there's one real root_POLY.
  * `{kt} b^2-4ac < 0`, there's no real root_POLY.


* `{bm} difference of squares` - Quadratic expressions that follow the pattern `{kt} a^2-b^2`. Difference of squares factor as `{kt} a^2-b^2 = (a-b)(a+b)`.

* `{bm} difference of cubes` - Cubic expressions that follow the pattern `{kt} a^3-b^3`. Difference of cubes factor as `{kt} a^3-b^3 = (a-b)(a^2+ab+b^2)`.

* `{bm} sum of cubes` - Cubic expressions that follow the pattern `{kt} a^3+b^3`. Sum of cubes factor as `{kt} a^3+b^3 = (a+b)(a^2-ab+b^2)`.

* `{bm} polynomial division` - A process that breaks a polynomial into two factors, given that one of the factors is already known. For example, consider the polynomial `{kt} 2x^3+x^2-6x-8`. If you already know that `{kt} (x-2)` is a factor, you can divide the polynomial by that known factor to determine the other factor:

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

  As shown in the example above, the process works similarly to long division. The polynomial is being divided by the known factor to determine the other factor: `{kt} (x-2)(2x^2+5x+4)=2x^3+x^2-6x-8`.

* `{bm} Rational root theorem` - A theorem that states a root_POLY of the polynomial equation `{kt} P(x)=0` can be expressed in the form `{kt} \frac{p}{q}` (assuming `P(x)` is a polynomial with integer coefficients), where ...
 
  * p is a factor of the constant term.
  * q is a factor of the leading coefficient.
 
  In other words, you can find a factor by testing all possible `{kt} \frac{p}{q}` to see if it's a root_POLY / factor of the polynomial. For example, the polynomial `{kt} P(x)=2x^3+x^2-6x-8` has ...

  * constant term factors p={-8,-6,-4,-2,-1,1,2,4,6,8}.
  * leading coefficient factors q={1,2}.

  Testing possible `{kt} \frac{p}{q}` within `P(x)` shows that `{kt} \frac{4}{2}=2` is a root_POLY: `{kt} P(2) = 0`. Since `{kt} 2` is a root_POLY, `{kt} (x-2)` is a factor.

  `{bm-error} Remove _POLY from the word root/(rational root_POLY theorem)/i`

`{bm-ignore} !!([\w\-]+?)!!/i`

`{bm-error} Wrap in !! or apply suffix _POLY/(roots?)/i`

`{bm-error} Did you mean discriminant?/(discriminator)/i`

`{bm-error} Missing topic reference/(_TOPIC)/i`

`{bm-error} Use you instead of we/\b(we)\b/i`

# Questions

`{bm-disable-all}`

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


