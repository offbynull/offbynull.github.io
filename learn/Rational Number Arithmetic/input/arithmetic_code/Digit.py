from __future__ import annotations

class Digit:
    def __init__(self, value: int, allowOob: bool = False):
        if not allowOob and (value < 0 or value > 9):
            raise Exception('Bad value')
        self.value = value

    def __lt__(self: Digit, other: Digit):
        if isinstance(other, int):
            return self.value < other
        elif isinstance(other, Digit):
            return self.value < other.value
        return False

    def __le__(self: Digit, other: Digit) -> bool:
        return self < other or self == other

    def __gt__(self: Digit, other: Digit):
        if isinstance(other, int):
            return self.value > other
        elif isinstance(other, Digit):
            return self.value > other.value
        return False

    def __ge__(self: Digit, other: Digit) -> bool:
        return self > other or self == other

    def __eq__(self: Digit, other: Digit):
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, Digit):
            return self.value == other.value
        return False

    def __str__(self: Digit):
        return str(self.value)

    def __hash__(self: Digit):
        return hash(self.value)


if __name__ == '__main__':
    Digit(10)  # should fail
