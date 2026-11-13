from expression.parser.StringStream import StringStream


class StringLiteral:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f'StringLiteral({self.value})'

    def __repr__(self):
        return str(self)

    def __format__(self, format_spec):
        return str(self)
    
    def __eq__(self, other):
        return self.value == other.value


class Identifier:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f'StringLiteral({self.value})'

    def __repr__(self):
        return str(self)

    def __format__(self, format_spec):
        return str(self)

    def __eq__(self, other):
        return self.value == other.value



def decimal(ss: StringStream):
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
        ret = int(v_str)
        ss.release()
        return ret
    except Exception as e:
        ss.revert()
        raise e

def string(ss: StringStream):
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
        return StringLiteral(value)
    except Exception as e:
        ss.revert()
        raise e

def identifier(ss: StringStream):
    ss.mark()
    try:
        name = ''
        ss.skip_whitespace()
        while ss.is_more() and ss.peek_char().isalpha():
            name += ss.read_char()
        if name == '':
            raise ValueError('Bad function name')
        ss.release()
        return Identifier(name)
    except Exception as e:
        ss.revert()
        raise e

def tokenize_stream(ss: StringStream):
    ss.mark()
    try:
        ret = []
        while True:
            ss.skip_whitespace()
            try:
                ret.append(identifier(ss))
                continue
            except Exception as e:
                ...
            try:
                ret.append(decimal(ss))
                continue
            except Exception as e:
                ...
            try:
                ret.append(string(ss))
                continue
            except Exception as e:
                ...
            try:
                if ss.peek_char() in '(,)+-/*^':
                    ret.append(ss.read_char())
                    continue
                if ss.remaining() >= 2 and ss.peek_chars(2) in {'>=', '<=', '!='}:
                    ret.append(ss.read_chars(2))
                    continue
                if ss.peek_char() in '=<>':
                    ret.append(ss.read_char())
                    continue
            except Exception as e:
                ...
            ss.skip_whitespace()
            if not ss.is_more():
                return ret
            raise ValueError(f'Unidentified token {ss.pointer=}')
    except Exception as e:
        ss.revert()
        raise e

def tokenize(s: str):
    return tokenize_stream(StringStream(s))


if __name__ == '__main__':
    tokens = tokenize('5/2 + 45/100 ^ -x <= 3 * 8 / log(2, 32, \'hello\')')
    print(f'{tokens}')
