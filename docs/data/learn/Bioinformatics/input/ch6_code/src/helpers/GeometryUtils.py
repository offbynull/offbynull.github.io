from math import inf, atan2, degrees, fmod


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


if __name__ == '__main__':
    for i in range(0, 361):
        i = normalize_degree(i)
        pre = normalize_degree(i-1)
        post = normalize_degree(i+1)
        if not test_angle_between(i, pre, post):
            raise ValueError(f'Failed when it should have passed on {i}')
        if test_angle_between(i, post, pre):
            raise ValueError(f'Passed when it should have failed on {i}')
        if not test_angle_between(i, i, i):
            raise ValueError(f'Failed when it should have passed on {i}')