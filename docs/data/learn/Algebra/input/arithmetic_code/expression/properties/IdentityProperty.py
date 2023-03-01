from expression.parser.Parser import FunctionNode, parse, Node
from expression.parser.Printer import to_string


def identity(fn: Node):
    if not isinstance(fn, FunctionNode):
        return set()
    if fn.op == '+' and fn.args[1] == 0:
        return {fn.args[0]}
    elif fn.op == '-' and fn.args[1] == 0:
        return {fn.args[0]}
    elif fn.op == '*' and fn.args[1] == 1:
        return {fn.args[0]}
    elif fn.op == '/' and  fn.args[1] == 1:
        return {fn.args[0]}
    return set()


if __name__ == '__main__':
    for r in identity(parse('x*1')):
        print(f'{to_string(r)}')
    for r in identity(parse('x/1')):
        print(f'{to_string(r)}')
    for r in identity(parse('x-0')):
        print(f'{to_string(r)}')
    for r in identity(parse('x+0')):
        print(f'{to_string(r)}')
