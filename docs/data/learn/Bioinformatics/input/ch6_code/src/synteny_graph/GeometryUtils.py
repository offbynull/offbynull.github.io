from math import inf, atan2, degrees


def distance(x1, x2, y1, y2) -> float:
    return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5

def slope(x1, x2, y1, y2) -> float:
    if y2 - y1 == 0:
        return inf
    return (x2 - x1) / (y2 - y1)

def angle(x1, x2, y1, y2) -> float:
    x = x2 - x1
    y = y2 - y1
    ret = degrees(atan2(y, x))
    if ret < 0:
        ret = 360.0 - -ret
    return ret
