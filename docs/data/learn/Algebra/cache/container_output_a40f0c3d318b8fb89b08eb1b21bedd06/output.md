<div style="margin:2em; background-color: #e0e0e0;">

<strong>⚠️NOTE️️️⚠️</strong>

The expression parsing code is too large to post here, but the execution of that code is shown below. There are key differences with how the code treats expressions vs how you were probably taught expressions in high school / college ...

 1. **All constants are integers**
 
    Only integer numbers are allowed as constants in the expressions. For rational numbers that aren't integers, those numbers can be expressed as ratios / fractions (e.g. 4.5 is `{kt} \frac{45}{10}`).

 1. **Fractions and division are the same thing**
 
    There is no distinction between fractions and divisions (e.g. `{kt} \frac{5+x}{10}` is the same as `{kt}(5+x) \div 10`). The code uses the `/` for both.

 1. **Variables can't be negative**
 
    A variable can't be positive or negative in the same way that an integer can be. Instead, a negated variable is represented by multiplying that variable by -1 (e.g. -x becomes -1*x).
</div>

