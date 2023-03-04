from __future__ import annotations

from abc import ABC


class Node(ABC):
    def __init__(self):
        ...

    @property
    def op_count(self):
        ...


class FunctionNode(Node):
    def __init__(
            self,
            op: str,
            args: list[Node]
    ):
        super().__init__()
        self._op = op
        self._args = tuple(args)
        self._hash = hash((self._op, tuple(self._args)))
        self._op_count = 1 + sum(a.op_count for a in args)

    @property
    def op_count(self):
        return self._op_count

    @property
    def op(self):
        return self._op

    @property
    def args(self):
        return self._args

    def __str__(self):
        return f'{self._op}({", ".join(str(x) for x in self._args)})'

    def __format__(self, format_spec):
        return str(self)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, FunctionNode) or self._hash != other._hash:
            return False
        return self._op == other._op and self._args == other._args

    def __hash__(self):
        return self._hash


class VariableNode(Node):
    def __init__(
            self,
            name: str
    ):
        super().__init__()
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def op_count(self):
        return 0

    def __str__(self):
        return f'{self.name}'

    def __format__(self, format_spec):
        return str(self)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return isinstance(other, VariableNode) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class ConstantNode(Node):
    def __init__(self, value: int | str):
        super().__init__()
        if isinstance(value, int):
            self._value = int(value)
        else:
            self._value = value

    @property
    def value(self):
        return self._value

    @property
    def op_count(self):
        return 0

    def __lt__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return self.value < other.value
        else:
            return self < ConstantNode(other)

    def __le__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return self.value <= other.value
        else:
            return self <= ConstantNode(other)

    def __gt__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return self.value > other.value
        else:
            return self > ConstantNode(other)

    def __ge__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return self.value >= other.value
        else:
            return self >= ConstantNode(other)

    def __eq__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return self.value == other.value
        else:
            return self == ConstantNode(other)

    def __ne__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return self.value != other.value
        else:
            return self != ConstantNode(other)

    def __add__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return ConstantNode(self.value + other.value)
        else:
            return self + ConstantNode(other)

    def __radd__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return ConstantNode(self.value + other.value)
        else:
            return self + ConstantNode(other)

    def __sub__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return ConstantNode(self.value - other.value)
        else:
            return self - ConstantNode(other)

    def __rsub__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return ConstantNode(self.value - other.value)
        else:
            return self - ConstantNode(other)

    def __mul__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return ConstantNode(self.value * other.value)
        else:
            return self * ConstantNode(other)

    def __rmul__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return ConstantNode(self.value * other.value)
        else:
            return self * ConstantNode(other)

    def __floordiv__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return ConstantNode(self.value // other.value)
        else:
            return self // ConstantNode(other)

    def __rfloordiv__(self, other: ConstantNode | int | str):
        if isinstance(other, ConstantNode):
            return ConstantNode(other.value // self.value)
        else:
            return ConstantNode(other) // self

    def __neg__(self):
        return ConstantNode(-self.value)

    def __str__(self):
        return f'{self.value}'

    def __format__(self, format_spec):
        return str(self)

    def __hash__(self):
        return hash(self.value)