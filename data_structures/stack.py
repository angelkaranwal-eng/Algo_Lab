"""
Node-based Stack implementation (LIFO: Last In, First Out).
Does not use Python built-in lists for storage.
"""

class StackNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class NodeBasedStack:
    def __init__(self, max_capacity: int = 8):
        self._top = None
        self._size = 0
        self.max_capacity = max_capacity
        self.push_count = 0
        self.pop_count = 0

    def is_empty(self) -> bool:
        return self._top is None

    def is_full(self) -> bool:
        return self._size >= self.max_capacity

    def push(self, value: int) -> bool:
        """Pushes an element onto the stack. Returns True on success, False if overflow."""
        if self.is_full():
            return False
        node = StackNode(value)
        node.next = self._top
        self._top = node
        self._size += 1
        self.push_count += 1
        return True

    def pop(self):
        """Pops the top element from the stack. Returns None on underflow."""
        if self.is_empty():
            return None
        removed = self._top.value
        self._top = self._top.next
        self._size -= 1
        self.pop_count += 1
        return removed

    def peek(self):
        """Returns the top element without removing it."""
        if self.is_empty():
            return None
        return self._top.value

    def size(self) -> int:
        return self._size

    def clear(self):
        self._top = None
        self._size = 0
        self.push_count = 0
        self.pop_count = 0

    def to_list(self):
        """Returns values from top to bottom."""
        values = []
        curr = self._top
        while curr:
            values.append(curr.value)
            curr = curr.next
        return values