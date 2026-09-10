"""Custom educational data structures built from scratch."""
from .stack import NodeBasedStack
from .queue import NodeBasedQueue
from .circular_queue import CircularQueue
from .linked_list import SinglyLinkedList, ListNode
from .binary_search_tree import BinarySearchTree, BSTNode
from .graph import Graph

__all__ = [
    "NodeBasedStack",
    "NodeBasedQueue",
    "CircularQueue",
    "SinglyLinkedList",
    "ListNode",
    "BinarySearchTree",
    "BSTNode",
    "Graph",
]