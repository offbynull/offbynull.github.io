def str_to_list(x: str, x_ptr: int):
    ret = []
    val = None
    assert x[x_ptr] == '['
    x_ptr += 1
    while x_ptr < len(x):
        ch = x[x_ptr]
        if ch == ',':
            if val is None:
                ret.append('')
            elif type(val) == str:
                ret.append(val.strip())
            else:
                ret.append(val)
            val = None
        elif ch == ']':
            if val is None:
                ...
            elif type(val) == str:
                ret.append(val.strip())
            else:
                ret.append(val)
            return ret, x_ptr
        elif ch == '[':
            if val is None:
                ...
            elif type(val) == str and len(val.strip()) == 0:
                ...
            else:
                assert False
            val, x_ptr = str_to_list(x, x_ptr)
        else:
            if val is None:
                val = ''
            assert type(val) == str
            val += ch
        x_ptr += 1
    raise ValueError(f'Unable to parse {x=} at {x_ptr=}')
