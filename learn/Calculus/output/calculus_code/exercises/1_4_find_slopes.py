import math
from fractions import Fraction

from Evaluator import evaluate
from expression.parser.Parser import parse

def avg_slope(func: str, x1: float, x2: float):
    node = parse(func)
    y1 = evaluate(node, {'x': x1})
    y2 = evaluate(node, {'x': x2})
    return (y2-y1) / (x2-x1)


x_list = [0.999,1.001]
slopes = []
pi_frac = Fraction(math.pi)
for x in x_list:
    slope = avg_slope(f'sin(10*({pi_frac.numerator}/{pi_frac.denominator})/x)', 1, x)
    slopes.append(slope)
for s in slopes:
    print(f'{s:.4f}', end=', ')
