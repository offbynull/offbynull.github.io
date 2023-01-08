from math import inf, atan2, degrees, fmod
from typing import Tuple


def distance(x1, x2, y1, y2) -> float:
    return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5


def slope(x1, x2, y1, y2) -> float:
    if y2 - y1 == 0:
        return inf
    return (x2 - x1) / (y2 - y1)


# As you move counter clockwise from (1, 0), degrees goes from >= 0 to < 360
def angle(x1, x2, y1, y2) -> float:
    x = x2 - x1
    y = y2 - y1
    assert not(x == 0 and y == 0), 'Getting angle of nothing?'
    ret = degrees(atan2(y, x))
    if ret < 0:
        ret = 360 + ret
    return ret


# angle1 must be before angle2, where "before" is in the context of the counter-clockwise direction
#
#            angle2 -->
#               \
#                \
#                 \
#                  \   passes            ^
#                   \                    |
#                    +------------- angle1
#             fails
#
#
def test_angle_between(test_angle, angle1, angle2) -> bool:
    assert 0 <= test_angle < 360
    assert 0 <= angle1 < 360
    assert 0 <= angle2 < 360

    if angle1 <= angle2:
        return angle1 <= test_angle <= angle2
    elif angle1 >= angle2:
        return test_angle <= angle2 or test_angle >= angle1
    else:
        raise ValueError('???')


# Ensures degree is >= 0 and < 360
def normalize_degree(degree) -> float:
    ret = fmod(degree, 360.0)
    if ret < 0.0:
        ret = 360.0 + ret
    return ret


# returns (slope, y-intercept) of a line
def y_intercept(x1, y1, x2, y2) -> float:
    m = slope(x1, x2, y1, y2)
    # y=m*x+b
    # y-m*x=b
    b = y1 - m * x1
    return b


# returns (slope, y-intercept) of the PERPENDICULAR line (90 degree rotation)
def perpendicular_line(slope: float, point: Tuple[float, float]) -> Tuple[float, float]:
    x, y = point
    m = slope
    # invert a line by changing slope to -1/m
    m_inv = -1 / m
    # y=m*x+b
    # y-m*x=b
    b_inv = y - m_inv * x
    return m_inv, b_inv


# returns intercept point (x, y) between the 2 lines
def line_intercept(slope1: float, y_intercept1: float, slope2: float, y_intercept2: float) -> Tuple[float, float]:
    # y=m1*x+b1
    # m2*x+b2=m1*x+b1
    # m2*x=m1*x+b1-b2
    # m2*x-m1*x=b1-b2
    # x*(m2-m1)=b1-b2
    # x=(b1-b2)/(m2-m1)
    x = (y_intercept1 - y_intercept2) / (slope2 - slope1)
    y = slope2 * x + y_intercept2
    return x, y


if __name__ == '__main__':
    m = slope(0, 1, 1, 3)
    b = y_intercept(0, 1, 1, 3)
    print(f'{m=} {b=}')

    m_inv, b_inv = perpendicular_line(m, (1, 3))
    print(f'{m_inv=} {b_inv=}')

    int_x, int_y = line_intercept(1/3, 5, -1/2, -2)
    print(f'{int_x=} {int_y=}')
    # for i in range(0, 361):
    #     i = normalize_degree(i)
    #     pre = normalize_degree(i-1)
    #     post = normalize_degree(i+1)
    #     if not test_angle_between(i, pre, post):
    #         raise ValueError(f'Failed when it should have passed on {i}')
    #     if test_angle_between(i, post, pre):
    #         raise ValueError(f'Passed when it should have failed on {i}')
    #     if not test_angle_between(i, i, i):
    #         raise ValueError(f'Failed when it should have passed on {i}')