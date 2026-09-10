"""
Array-based Circular Queue demonstration.
Demonstrates pointer wrap-around: (rear + 1) % capacity.
"""

class CircularQueue:
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.front_idx = -1
        self.rear_idx = -1
        self._size = 0
        self.enqueue_count = 0
        self.dequeue_count = 0

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self.capacity

    def enqueue(self, value: int) -> bool:
        if self.is_full():
            return False
        if self.is_empty():
            self.front_idx = self.rear_idx = 0
        else:
            self.rear_idx = (self.rear_idx + 1) % self.capacity
        self.buffer[self.rear_idx] = value
        self._size += 1
        self.enqueue_count += 1
        return True

    def dequeue(self):
        if self.is_empty():
            return None
        val = self.buffer[self.front_idx]
        self.buffer[self.front_idx] = None
        if self.front_idx == self.rear_idx:
            self.front_idx = self.rear_idx = -1
        else:
            self.front_idx = (self.front_idx + 1) % self.capacity
        self._size -= 1
        self.dequeue_count += 1
        return val

    def get_front(self):
        return self.buffer[self.front_idx] if not self.is_empty() else None

    def get_rear(self):
        return self.buffer[self.rear_idx] if not self.is_empty() else None

    def size(self) -> int:
        return self._size

    def clear(self):
        self.buffer = [None] * self.capacity
        self.front_idx = -1
        self.rear_idx = -1
        self._size = 0