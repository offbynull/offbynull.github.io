from __future__ import annotations
from typing import Iterable


class Address:
    @staticmethod
    def from_string(elements_str: str) -> Address:
        return Address._unescape_address(elements_str)

    def __init__(self, address_elements: Iterable[str]):
        self._address_elements = tuple(address_elements)

    def __len__(self):
        return len(self._address_elements)

    def is_empty(self) -> bool:
        return len(self._address_elements) == 0

    def get_elements(self) -> list[str]:
        return list(self._address_elements)

    def append_suffix(self, suffix: str | Iterable[str]) -> Address:
        if isinstance(suffix, str):
            return Address(self._address_elements + (suffix, ))
        else:
            return Address(self._address_elements + tuple(suffix))

    def is_prefix_of(self, potential_prefix: Address) -> bool:
        if len(potential_prefix._address_elements) < len(self._address_elements):
            return False
        return potential_prefix._address_elements[0:len(self._address_elements)] == self._address_elements

    def remove_prefix(self, prefix: Address) -> Address:
        if not self.is_prefix_of(prefix):
            raise ValueError()
        return Address(self._address_elements[len(prefix._address_elements):])

    def remove_suffix(self, count: int) -> Address:
        if count < 0:
            raise ValueError()
        return Address(self._address_elements[:-count])

    def __hash__(self) -> int:
        return hash(self._address_elements)

    def __eq__(self, other: Address) -> bool:
        return self._address_elements == other._address_elements

    def __lt__(self, other: Address) -> bool:
        return self._address_elements < other._address_elements

    def __str__(self) -> str:
        return Address._escape_address(self)

    def __repr__(self):
        return str(self)

    def __format__(self, format_spec):
        return str(self)


    @staticmethod
    def _escape_address(address: Address) -> str:
        ret = []
        for element in address._address_elements:
            escaped = ''
            for ch in element:
                # if not (ch.isascii() and ch.isprintable()):
                #     raise ValueError()
                if ch == ':':
                    escaped += '\\:'
                elif ch == '\\':
                    escaped += '\\\\'
                else:
                    escaped += ch
            ret.append(escaped)
        return ':'.join(ret)

    @staticmethod
    def _unescape_address(elements_str: str) -> Address:
        ret = []
        current = ''
        read_count = 0
        escape_mode = False
        for ch in elements_str:
            read_count += 1
            if escape_mode:
                if ch == ':':
                    current += ':'
                elif ch == '\\':
                    current += '\\'
                else:
                    raise ValueError(f'Unrecognized escape sequence {ch}')
                escape_mode = False
            else:
                if ch == '\\':
                    # This is the start of an escape sequence. Character after this one will determine what will be dumped.
                    escape_mode = True
                    continue
                elif ch == ':':
                    # We're unescaping an address element. Encounter a non-escaped separator (colon) is the end of the address element.
                    ret.append(current)
                    current = ''
                    continue
                else:
                    current += ch
        if read_count > 0:
            ret.append(current)
        return Address(ret)
