"""
Singly Linked List implementation.
Provides manual pointer-swapping implementations for insertion, deletion, and reversal.
"""

class ListNode:
    def __init__(self, data: int):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self._count = 0

    def is_empty(self) -> bool:
        return self.head is None

    def size(self) -> int:
        return self._count

    def insert_at_beginning(self, value: int):
        node = ListNode(value)
        node.next = self.head
        self.head = node
        self._count += 1

    def insert_at_end(self, value: int):
        node = ListNode(value)
        if self.head is None:
            self.head = node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = node
        self._count += 1

    def insert_at_position(self, value: int, pos: int) -> bool:
        if pos < 0 or pos > self._count:
            return False
        if pos == 0:
            self.insert_at_beginning(value)
            return True
        node = ListNode(value)
        curr = self.head
        for _ in range(pos - 1):
            curr = curr.next
        node.next = curr.next
        curr.next = node
        self._count += 1
        return True

    def delete_from_beginning(self):
        if self.is_empty():
            return None
        val = self.head.data
        self.head = self.head.next
        self._count -= 1
        return val

    def delete_from_end(self):
        if self.is_empty():
            return None
        if self.head.next is None:
            val = self.head.data
            self.head = None
            self._count -= 1
            return val
        curr = self.head
        while curr.next.next:
            curr = curr.next
        val = curr.next.data
        curr.next = None
        self._count -= 1
        return val

    def delete_from_position(self, pos: int):
        if self.is_empty() or pos < 0 or pos >= self._count:
            return None
        if pos == 0:
            return self.delete_from_beginning()
        curr = self.head
        for _ in range(pos - 1):
            curr = curr.next
        val = curr.next.data
        curr.next = curr.next.next
        self._count -= 1
        return val

    def search_steps(self, target: int):
        """Yields (current_index, current_value, is_found) step-by-step."""
        curr = self.head
        idx = 0
        while curr:
            if curr.data == target:
                yield idx, curr.data, True
                return
            yield idx, curr.data, False
            curr = curr.next
            idx += 1
        yield -1, None, False

    def reverse(self):
        """In-place pointer reversal: prev, curr, next."""
        prev = None
        curr = self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    def to_list(self):
        res = []
        curr = self.head
        while curr:
            res.append(curr.data)
            curr = curr.next
        return res

    def clear(self):
        self.head = None
        self._count = 0