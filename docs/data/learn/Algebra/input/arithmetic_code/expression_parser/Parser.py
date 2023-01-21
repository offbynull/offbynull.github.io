from fractions import Fraction
from typing import Any

from expression_parser import LexerStream
from expression_parser.Lexer import Identifier, tokenize
from expression_parser.LexerStream import LexerStream


class FunctionNode:
    def __init__(self, op: str, args: list[Any]):
        self.op = op
        self.args = args

    def __str__(self):
        return f'{self.op}({", ".join(str(x) for x in self.args)})'

    def __format__(self, format_spec):
        return str(self)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.op == other.op and self.args == other.args

    def __hash__(self):
        return hash((self.op, tuple(self.args)))


class VariableNode:
    def __init__(self):
        self.name = None

    def __str__(self):
        return f'{self.name}'

    def __format__(self, format_spec):
        return str(self)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

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
        n = VariableNode()
        n.name = name.value
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
            if isinstance(item, Fraction):
                s.read()  # discard
                if negate:
                    item = -item
                    negate = False
                chain.append(item)
            elif isinstance(item, Identifier):
                tree = variable_or_function(s)
                if negate:
                    tree = FunctionNode('*', [Fraction(-1), tree])
                    negate = False
                chain.append(tree)
            elif item == '(':
                tree = brackets(s)
                if negate:
                    if isinstance(tree, Fraction):
                        tree = -tree
                    elif isinstance(tree, FunctionNode) or isinstance(tree, VariableNode):
                        tree = FunctionNode('*', [Fraction(-1), tree])
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


if __name__ == '__main__':
    tree = parse('5:2 + -4.5 ^ -x + -(3 * 8) / -log(2, 32)')
    print(f'{tree}')
