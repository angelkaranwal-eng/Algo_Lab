"""
Node-based Queue implementation (FIFO: First In, First Out).
Demonstrates dynamic linked node allocation without fixed array buffers.
"""

class QueueNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class NodeBasedQueue:
    def __init__(self, max_capacity: int = 8):
        self._front = None
        self._rear = None
        self._size = 0
        self.max_capacity = max_capacity
        self.enqueue_count = 0
        self.dequeue_count = 0

    def is_empty(self) -> bool:
        return self._front is None

    def is_full(self) -> bool:
        return self._size >= self.max_capacity

    def enqueue(self, value: int) -> bool:
        if self.is_full():
            return False
        node = QueueNode(value)
        if self.is_empty():
            self._front = self._rear = node
        else:
            self._rear.next = node
            self._rear = node
        self._size += 1
        self.enqueue_count += 1
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        removed = self._front.value
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        self.dequeue_count += 1
        return removed

    def front(self):
        return self._front.value if self._front else None

    def rear(self):
        return self._rear.value if self._rear else None

    def size(self) -> int:
        return self._size

    def clear(self):
        self._front = self._rear = None
        self._size = 0
        self.enqueue_count = 0
        self.dequeue_count = 0

    def to_list(self):
        """Returns list from front to rear."""
        values = []
        curr = self._front
        while curr:
            values.append(curr.value)
            curr = curr.next
        return values