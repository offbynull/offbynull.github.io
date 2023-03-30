from __future__ import annotations

import inspect
import sys
from pathlib import Path
from sys import stdin

import yaml

from expression.Node import FunctionNode, VariableNode, ConstantNode
from relation.Relation import Relation
from relation.parser.Lexer import Identifier, tokenize
from relation.parser.LexerStream import LexerStream


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


def relation(s: LexerStream):
    s.mark()
    try:
        lhs = expression(s)
        op = s.read()  # discard
        if op not in {'<', '<=', '>', '>=', '!=', '='}:
            raise ValueError('Unknown relation operator')
        rhs = expression(s)
        return Relation(op, lhs, rhs)
    except Exception as e:
        s.revert()
        raise e


def parse_stream(s: LexerStream):
    s.mark()
    try:
        ret = relation(s)
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
    ret = parse('5/2 + -45/50 ^ -x <= -(3 * 8) / -log(2, 32)')
    print(f'{ret}')
