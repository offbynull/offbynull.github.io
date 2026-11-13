from __future__ import annotations


class TerminalNode:
    INST: TerminalNode = None

    def __init__(self):
        raise RuntimeError('Call instance() or use INST instead')

    def __eq__(self, other):
        if not isinstance(other, TerminalNode):
            return False
        return True

    def __hash__(self):
        return hash(())

    def __str__(self):
        return str('<TERM>')

    def __repr__(self):
        return str(self)

    @classmethod
    def instance(cls):
        if cls.INST is None:
            cls.INST = cls.__new__(cls)
        return cls.INST


TerminalNode.instance()  # prime instance

if __name__ == '__main__':
    t = TerminalNode.INST
    print(f'{t}')
