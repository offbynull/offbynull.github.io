# def func19(x):
#     return (x**2-3*x)/(x**2-9)
#
# for x in [3.1, 3.05, 3.01, 3.001, 3.0001, 2.9, 2.95, 2.99, 2.999, 2.9999]:
#     y = func19(x)
#     print(f'{x}, {y:.4f}')
import math
from math import sin, tan


# def func20(x):
#     return (x**2-3*x)/(x**2-9)
#
# for x in [-2.5, -2.9, -2.95, -2.99, -2.999, -2.9999, -3.5, -3.1, -3.05, -3.01, -3.001, -3.0001]:
#     y = func20(x)
#     print(f'{x}, {y:.4f}')


# def func21(x):
#     return sin(x)/(x+tan(x))
#
# for x in sorted([-1, -0.5, -0.2, -0.1, -0.05, -0.01, 1, 0.5, 0.2, 0.1, 0.05, 0.01]):
#     y = func21(x)
#     print(f'{x}, {y:.4f}')


# def func22(x):
#     return ((2+x)**5 - 32)/x
#
# for x in sorted([-0.5, -0.1, -0.01, -0.001, -0.0001, 0.5, 0.1, 0.01, 0.001, 0.0001]):
#     y = func22(x)
#     print(f'{x}, {y:.4f}')


# def func41a(x):
#     return 1/(x**3-1)
#
# for x in sorted([1.1, 1.01, 1.001, 1.0001, 0.9999, 0.999, 0.99, 0.9]):
#     y = func41a(x)
#     print(f'{x}, {y:.4f}')


# def func42b(x):
#     return tan(4*x)/x
#
# for x in sorted([-0.1, -0.01, -0.001, -0.0001, 0.0001, 0.001, 0.01, 0.1]):
#     y = func42b(x)
#     print(f'{x}, {y:.4f}')


# def func43(x):
#     return x**2 - 2**x/1000
#
# for x in sorted([0.04, 0.02, 0.01, 0.005, 0.003, 0.001]):
#     y = func43(x)
#     print(f'{x}, {y:.9f}')


def func49(x):
    return (x**3 - 1) / (math.sqrt(x) - 1)

for x in sorted([1-0.0001, 1-0.001, 1-0.01, 1-0.1, 1+0.1, 1+0.01, 1+0.001, 1+0.0001]):
    y = func49(x)
    print(f'{x}, {y:.9f}')
