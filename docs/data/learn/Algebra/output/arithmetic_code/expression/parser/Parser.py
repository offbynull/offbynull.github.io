from __future__ import annotations

import inspect
import sys
from abc import ABC
from pathlib import Path
from sys import stdin

import yaml

from expression.parser import LexerStream
from expression.parser.Lexer import Identifier, tokenize
from expression.parser.LexerStream import LexerStream


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


def function(s: LexerStream):
    s.mark()
    try:
        name = s.read()
        if not isinstance(name, Identifier):
            raise ValueError('Not identifier')
        s.skip_const(['('])
        args = []
        while True:
            arg = expression(s)
            args.append(arg)
            if s.peek() == ')':
                break
            elif s.peek() == ',':
                s.read()
            else:
                raise ValueError('Unexpected delim')
        s.skip_const([')'])
        s.release()
        return FunctionNode(name.value, args)
    except Exception as e:
        s.revert()
        raise e

def variable(s: LexerStream):
    s.mark()
    try:
        name = s.read()
        if not isinstance(name, Identifier):
            raise ValueError('Not identifier')
        n = VariableNode(name.value)
        s.release()
        return n
    except Exception as e:
        s.revert()
        raise e

def variable_or_function(s: LexerStream):
    s.mark()
    try:
        try:
            ret = function(s)
            s.release()
            return ret
        except ValueError:
            ...
        ret = variable(s)
        s.release()
        return ret
    except Exception as e:
        s.revert()
        raise e

def brackets(s: LexerStream):
    s.mark()
    try:
        s.skip_const(['('])
        ret = expression(s)
        s.skip_const([')'])
        s.release()
        return ret
    except Exception as e:
        s.revert()
        raise e

def expression(s: LexerStream):
    s.mark()
    try:
        chain = []
        negate = False
        while not s.is_finished():
            item = s.peek()
            if isinstance(item, int):
                s.read()  # discard
                if negate:
                    item = -item
                    negate = False
                tree = ConstantNode(item)
                chain.append(tree)
            elif isinstance(item, Identifier):
                tree = variable_or_function(s)
                if negate:
                    tree = FunctionNode('*', [ConstantNode(-1), tree])
                    negate = False
                chain.append(tree)
            elif item == '(':
                tree = brackets(s)
                if negate:
                    if isinstance(tree, ConstantNode):
                        tree = -tree
                    elif isinstance(tree, FunctionNode) or isinstance(tree, VariableNode):
                        tree = FunctionNode('*', [ConstantNode(-1), tree])
                    else:
                        raise ValueError('Unknown type')
                    negate = False
                chain.append(tree)
            elif item in {'-', '+'} and len(chain) == 0 or (isinstance(chain[-1], str) and chain[-1] in '+-*/^'):
                s.read()  # discard
                negate = item == '-'
            elif item in {'+', '-', '*', '/', '^'}:
                s.read()  # discard
                op = item
                chain.append(op)
            else:
                break

        def replace(ops: str):
            i = 1
            while i < len(chain):
                if chain[i] in ops:
                    op = chain[i]
                    args = [chain[i - 1], chain[i + 1]]
                    fn = FunctionNode(op, args)
                    chain[i - 1:i + 2] = [fn]
                else:
                    i += 2

        replace('^')
        replace('*/')
        replace('+-')
        assert len(chain) == 1
        s.release()
        return chain[0]
    except Exception as e:
        s.revert()
        raise e

def parse_stream(s: LexerStream):
    s.mark()
    try:
        ret = expression(s)
        if not s.is_finished():
            raise ValueError('Unexpected tokens')
        return ret
    except Exception as e:
        s.revert()
        raise e

def parse(s: str):
    tokens = tokenize(s)
    return parse_stream(LexerStream(tokens))


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    funcs = {n: o for n, o in inspect.getmembers(sys.modules[__name__]) if (inspect.isfunction(o) and n != 'main')}
    try:
        data_raw = ''.join(stdin.readlines())
        data: list = yaml.safe_load(data_raw)
        print(f'{Path(__file__).name} produced the following ...')
        print()
        # print('```')
        # print(data_raw)
        # print('```')
        # print()
        # print(f'The following alternative forms were produced ...')
        # print()
        print('```')
        for exp in data:
            exp = str(exp)
            print(f'Parse {exp} ...')
            print(f'    {parse(exp)}')
        print('```')
        print()
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()
    # tree = parse('5/2 + -45/50 ^ -x + -(3 * 8) / -log(2, 32)')
    # print(f'{tree}')
