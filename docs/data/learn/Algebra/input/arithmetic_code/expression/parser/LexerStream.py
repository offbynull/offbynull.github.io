from typing import Any


class LexerStream:
    def __init__(self, value: list[Any]):
        self.value = value
        self.pointer = 0
        self.queue = []

    def mark(self):
        self.queue.append(self.pointer)

    def revert(self):
        self.pointer = self.queue.pop()

    def release(self):
        self.queue.pop()

    def read(self):
        if self.pointer == len(self.value):
            raise ValueError('Too few characters')
        x = self.value[self.pointer]
        self.pointer += 1
        return x

    def read_n(self, k: int):
        x = self.value[self.pointer:self.pointer+k]
        if len(x) != k:
            raise ValueError('Too few characters')
        self.pointer += k
        return x

    def peek(self):
        if self.pointer == len(self.value):
            raise ValueError('Too few characters')
        return self.value[self.pointer]

    def peek_n(self, k: int):
        x = self.value[self.pointer:self.pointer+k]
        if len(x) != k:
            raise ValueError('Too few characters')
        return x

    def has_const(self, const: list[Any]):
        x = self.value[self.pointer:self.pointer+len(const)]
        return x == const

    def skip_const(self, const: list[Any]):
        x = self.value[self.pointer:self.pointer+len(const)]
        if x != const:
            raise ValueError('Const missing')
        self.pointer += len(const)
        return x

    def remaining(self):
        return len(self.value) - self.pointer

    def is_finished(self):
        return self.pointer == len(self.value)

    def is_more(self):
        return not self.is_finished()
