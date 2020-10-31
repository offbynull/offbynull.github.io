from __future__ import annotations

import sys
from enum import Enum
import inspect
from typing import List, Tuple, Optional

save_states: List[int] = []
indent_offset: int = -2
whitelist: List[Tuple[str, str]] = []


def log_indent():
    global indent_offset
    indent_offset += 2


def log_unindent():
    global indent_offset
    indent_offset -= 2


def log_push_indent_state():
    global indent_offset
    save_states.append(indent_offset)


def log_pop_indent_state():
    global indent_offset, save_states
    indent_offset = save_states.pop()


def log_whitelist(allowed: List[Tuple[str, str]]):
    global whitelist
    whitelist = allowed


def log(data: str):
    global indent_offset, whitelist

    # This was what was previously used, but it was becoming cripplingly slow. The alternative is a little better. More
    # info available at https://stackoverflow.com/a/24940992
    #     s = inspect.stack(0)[1]
    #     if not (s.filename, s.function) in whitelist:
    previous_frame = sys._getframe().f_back
    function_name = previous_frame.f_code.co_name
    if not [True for x in whitelist if x[1] == function_name]:  # do this to avoid touching co_filename if unneeded -- I'm thinking accesssing it does disk IO?
        return
    filename = previous_frame.f_code.co_filename
    if not (filename, function_name) in whitelist:
        return

    data = (' ' * indent_offset) + ' * ' + data
    print(data)


def log_decorator(func):
    def inner(*args, **kwargs):
        log_push_indent_state()
        try:
            log_indent()
            ret = func(*args, **kwargs)
            log_unindent()
            return ret
        finally:
            log_pop_indent_state()
    return inner


if __name__ == '__main__':
    output = inspect.stack()
    print(str(output[0].function))
