from typing import Any

from actor_framework.Address import Address


class Context:
    def __init__(self, self_addr: Address):
        self._self_addr = self_addr
        self._in_msg = None
        self._out_msgs = None
        self._timestamp = None

    def _update(self, timestamp: int, in_from_addr: Address, in_to_addr: Address, in_msg: Any):
        if not self._self_addr.is_prefix_of(in_from_addr):
            raise ValueError()
        self._in_msg = in_from_addr, in_to_addr, in_msg
        self._out_msgs = []
        self._timestamp = timestamp

    def add_outgoing_message(self, to_addr: Address, msg: Any, from_addr: Address | None = None, wait_duration_override: int | None = None):
        if msg is None:
            raise ValueError()
        if from_addr is None:
            from_addr = self._self_addr
        self._out_msgs.append((from_addr, to_addr, msg, wait_duration_override))

    def get_self_address(self) -> Address:
        return self._self_addr

    def get_incoming_message(self) -> tuple[Address, Address, Any]:
        return self._in_msg

    def get_timestamp(self):
        return self._timestamp
