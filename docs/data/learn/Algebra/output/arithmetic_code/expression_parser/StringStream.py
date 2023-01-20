class StringStream:
    def __init__(self, value: str):
        self.value = value
        self.pointer = 0
        self.queue = []

    def mark(self):
        self.queue.append(self.pointer)

    def revert(self):
        self.pointer = self.queue.pop()

    def read_char(self):
        if self.pointer == len(self.value):
            raise ValueError('Too few characters')
        x = self.value[self.pointer]
        self.pointer += 1
        return x

    def read_chars(self, k: int):
        x = self.value[self.pointer:self.pointer+k]
        if len(x) != k:
            raise ValueError('Too few characters')
        self.pointer += k
        return x

    def peek_char(self):
        if self.pointer == len(self.value):
            raise ValueError('Too few characters')
        return self.value[self.pointer]

    def peek_chars(self, k: int):
        x = self.value[self.pointer:self.pointer+k]
        if len(x) != k:
            raise ValueError('Too few characters')
        return x

    def has_const(self, const: str):
        x = self.value[self.pointer:self.pointer+len(const)]
        return x == const

    def skip_const(self, const: str):
        x = self.value[self.pointer:self.pointer+len(const)]
        if x != const:
            raise ValueError('Const missing')
        self.pointer += len(const)
        return x

    def skip_whitespace(self):
        while self.pointer < len(self.value) and self.value[self.pointer].isspace():
            self.pointer += 1

    def is_finished(self):
        return self.pointer == len(self.value)

    def __next__(self):
        return self.read_char()
