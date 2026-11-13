# Exercise Break: Compute the Pearson correlation coefficient for the following pairs of vectors:
#
#     (cos α, sin α) and (sin α,cos α) for an arbitrary value of α;
#     (\sqrt{0.75},0.5) and (-\sqrt{0.75},0.5)

# MY ANSWER
# ---------
from math import sqrt, cos, sin
from statistics import mean


def pearson_correlation_coefficient(m: int, x: tuple[float, ...], y: tuple[float, ...]):
    x_mean = mean(x)
    y_mean = mean(y)
    num = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(m))
    denom = sqrt(
        sum((x[i] - x_mean)**2 for i in range(m))
        * sum((y[i] - y_mean)**2 for i in range(m))
    )
    return num / denom


print(f'{pearson_correlation_coefficient(2, (cos(45), sin(45)), (sin(45), cos(45)))=}')
print(f'{pearson_correlation_coefficient(2, (cos(75), sin(75)), (sin(75), cos(75)))=}')
print(f'{pearson_correlation_coefficient(2, (cos(0), sin(0)), (sin(0), cos(0)))=}')

print(f'{pearson_correlation_coefficient(2, (sqrt(0.75), 0.5), (-sqrt(0.75), 0.5))=}')