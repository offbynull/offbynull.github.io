from expression_parser.StringStream import StringStream


def parse_number(ss: StringStream):
    ss.mark()
    try:
        ss.skip_whitespace()
        v_str = ''
        if ss.peek_char() not in '0123456789':
            raise ValueError('Bad float')
        while ss.peek_char() in '0123456789':
            v_str += ss.read_char()
        if ss.peek_char() == '.':
            v_str += '.'
            if ss.peek_char() not in '0123456789':
                raise ValueError('Bad float')
            while ss.peek_char() in '0123456789':
                v_str += ss.read_char()
            ss.skip_whitespace()
        return float(v_str)
    except Exception as e:
        ss.revert()
        raise e

class FunctionNode:
    def __init__(self):
        self.op = None
        self.args = None

    def __str__(self):
        return f'{self.op}({", ".join(str(x) for x in self.args)})'

    def __format__(self, format_spec):
        return str(self)

def parse_function(ss: StringStream):
    ss.mark()
    try:
        n = FunctionNode()
        n.op = ''
        ss.skip_whitespace()
        while ss.peek_char().isalpha():
            n.op += ss.read_char()
        if n.op == '':
            raise ValueError('Bad function name')
        ss.skip_whitespace()
        ss.skip_const('(')
        ss.skip_whitespace()
        n.args = []
        while True:
            arg = parse_expression(ss)
            n.args.append(arg)
            if ss.peek_char() == ')':
                break
            elif ss.peek_char() == ',':
                ss.read_char()
            else:
                raise ValueError('Unexpected delim')
            ss.skip_whitespace()
        ss.skip_const(')')
        ss.skip_whitespace()
        return n
    except Exception as e:
        ss.revert()
        raise e

class VariableNode:
    def __init__(self):
        self.name = None

    def __str__(self):
        return f'{self.name}'

    def __format__(self, format_spec):
        return str(self)

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
        return n
    except Exception as e:
        ss.revert()
        raise e

def parse_variable_or_function(ss: StringStream):
    ss.mark()
    try:
        try:
            return parse_function(ss)
        except ValueError:
            ...
        return parse_variable(ss)
    except Exception as e:
        ss.revert()
        raise e

class BinaryNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.op = None

    def __str__(self):
        return f'{self.op}({self.left}, {self.right})'

    def __format__(self, format_spec):
        return str(self)

def parse_brackets(ss: StringStream):
    ss.mark()
    try:
        ss.skip_whitespace()
        ss.skip_const('(')
        ret = parse_expression(ss)
        ss.skip_whitespace()
        ss.skip_const(')')
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
            if ss.peek_char() in '0123456789.':
                num = parse_number(ss)
                chain.append(num)
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
                    n = BinaryNode()
                    n.left = chain[i - 1]
                    n.op = chain[i]
                    n.right = chain[i + 1]
                    chain[i - 1:i + 2] = [n]
                else:
                    i += 2

        replace('^')
        replace('*/')
        replace('+-')
        assert len(chain) == 1
        return chain[0]
    except Exception as e:
        ss.revert()
        raise e


tree = parse_expression(StringStream('5 + 4 ^ x + 3 * 8 / log(2, 32)'))
print(f'{tree}')