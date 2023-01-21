from fractions import Fraction
from typing import Any

from expression_parser.StringStream import StringStream


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


def parse_decimal(ss: StringStream):
    ss.mark()
    try:
        ss.skip_whitespace()
        v_str = ''
        if ss.peek_char() not in '0123456789':
            raise ValueError('Bad decimal')
        while ss.is_more() and ss.peek_char() in '0123456789':
            v_str += ss.read_char()
        if ss.is_more() and ss.peek_char() == '.':
            v_str += ss.read_char()  # '.'
            if ss.is_finished() or ss.peek_char() not in '0123456789':
                raise ValueError('Bad decimal')
            while ss.is_more() and ss.peek_char() in '0123456789':
                v_str += ss.read_char()
            ss.skip_whitespace()
        ret = Fraction(v_str)
        ss.release()
        return ret
    except Exception as e:
        ss.revert()
        raise e

def parse_fraction(ss: StringStream):
    ss.mark()
    try:
        ss.skip_whitespace()
        num_str = ''
        if ss.peek_char() not in '0123456789':
            raise ValueError('Bad fraction')
        while ss.is_more() and ss.peek_char() in '0123456789':
            num_str += ss.read_char()
        if ss.read_char() != ':':
            raise ValueError('Bad fraction')
        denom_str = ''
        if ss.peek_char() not in '0123456789':
            raise ValueError('Bad fraction')
        while ss.is_more() and ss.peek_char() in '0123456789':
            denom_str += ss.read_char()
        ret = Fraction(int(num_str), int(denom_str))
        ss.release()
        return ret
    except Exception as e:
        ss.revert()
        raise e

def parse_fraction_or_decimal(ss: StringStream):
    ss.mark()
    try:
        try:
            ret = parse_fraction(ss)
            ss.release()
            return ret
        except ValueError:
            ...
        ret = parse_decimal(ss)
        ss.release()
        return ret
    except Exception as e:
        ss.revert()
        raise e

def parse_string(ss: StringStream):
    ss.mark()
    try:
        ss.skip_whitespace()
        ss.skip_const('\'')
        value = ''
        in_escape_seq = False
        while True:
            ch = ss.read_char()
            if in_escape_seq:
                if ch == '\\':
                    value += '\\'
                elif ch == '\'':
                    value += '\''
                else:
                    raise ValueError('Unrecognized escape')
                in_escape_seq = False
            elif ch == '\\':
                in_escape_seq = True
            elif ch == '\'':
                break
            else:
                value += ch
        ss.skip_whitespace()
        ss.release()
        return value
    except Exception as e:
        ss.revert()
        raise e

def parse_function(ss: StringStream):
    ss.mark()
    try:
        op = ''
        ss.skip_whitespace()
        while ss.peek_char().isalpha():
            op += ss.read_char()
        if op == '':
            raise ValueError('Bad function name')
        ss.skip_whitespace()
        ss.skip_const('(')
        ss.skip_whitespace()
        args = []
        while True:
            arg = parse_expression(ss)
            args.append(arg)
            if ss.peek_char() == ')':
                break
            elif ss.peek_char() == ',':
                ss.read_char()
            else:
                raise ValueError('Unexpected delim')
            ss.skip_whitespace()
        ss.skip_const(')')
        ss.skip_whitespace()
        ss.release()
        return FunctionNode(op, args)
    except Exception as e:
        ss.revert()
        raise e

def parse_variable(ss: StringStream):
    ss.mark()
    try:
        n = VariableNode()
        n.name = ''
        ss.skip_whitespace()
        while ss.peek_char().isalpha():
            n.name += ss.read_char()
        if n.name == '':
            raise ValueError('Bad function name')
        ss.release()
        return n
    except Exception as e:
        ss.revert()
        raise e

def parse_variable_or_function(ss: StringStream):
    ss.mark()
    try:
        try:
            ret = parse_function(ss)
            ss.release()
            return ret
        except ValueError:
            ...
        ret = parse_variable(ss)
        ss.release()
        return ret
    except Exception as e:
        ss.revert()
        raise e

def parse_brackets(ss: StringStream):
    ss.mark()
    try:
        ss.skip_whitespace()
        ss.skip_const('(')
        ret = parse_expression(ss)
        ss.skip_whitespace()
        ss.skip_const(')')
        ss.release()
        return ret
    except Exception as e:
        ss.revert()
        raise e

def parse_expression(ss: StringStream):
    ss.mark()
    try:
        chain = []
        ss.skip_whitespace()
        while not ss.is_finished():
            ss.skip_whitespace()
            if ss.peek_char() in '0123456789':
                num = parse_fraction_or_decimal(ss)
                chain.append(num)
            elif ss.peek_char() == '\'':
                s = parse_string(ss)
                chain.append(s)
            elif ss.peek_char().isalpha():
                tree = parse_variable_or_function(ss)
                chain.append(tree)
            elif ss.peek_char() == '(':
                tree = parse_brackets(ss)
                chain.append(tree)
            elif ss.peek_char() in '+-*/^':
                op = ss.read_char()
                chain.append(op)
            else:
                break
        ss.skip_whitespace()

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
        ss.release()
        return chain[0]
    except Exception as e:
        ss.revert()
        raise e


def parse_main(ss: StringStream):
    ss.mark()
    try:
        ss.skip_whitespace()
        ret = parse_expression(ss)
        ss.skip_whitespace()
        if not ss.is_finished():
            raise ValueError('Unexpected char')
        return ret
    except Exception as e:
        ss.revert()
        raise e


if __name__ == '__main__':
    tree = parse_main(StringStream('5:2 + 4.5 ^ x + 3 * 8 / log(2, 32, \'hello \\\\ world \')'))
    print(f'{tree}')
