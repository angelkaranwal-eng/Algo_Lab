"""
Binary Search Tree (BST) implementation.
Includes node insertion, search path generator, deletion (handling 0, 1, and 2 children),
and Preorder, Inorder, and Postorder traversals.
"""

class BSTNode:
    def __init__(self, key: int):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self._size = 0

    def is_empty(self) -> bool:
        return self.root is None

    def size(self) -> int:
        return self._size

    def height(self, node=None) -> int:
        if self.is_empty():
            return 0
        if node is None and self.root is not None:
            return self._height_recursive(self.root)
        return self._height_recursive(node)

    def _height_recursive(self, node) -> int:
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), self._height_recursive(node.right))

    def insert(self, key: int):
        """
        Inserts key and yields comparison steps for visual tracking:
        Yields: ('compare', current_key, target_key, 'left'|'right')
        """
        if self.root is None:
            self.root = BSTNode(key)
            self._size += 1
            yield ('placed', key, None, 'root')
            return

        curr = self.root
        while True:
            if key == curr.key:
                yield ('duplicate', curr.key, key, 'none')
                return
            elif key < curr.key:
                yield ('compare', curr.key, key, 'left')
                if curr.left is None:
                    curr.left = BSTNode(key)
                    self._size += 1
                    yield ('placed', curr.left.key, curr.key, 'left')
                    return
                curr = curr.left
            else:
                yield ('compare', curr.key, key, 'right')
                if curr.right is None:
                    curr.right = BSTNode(key)
                    self._size += 1
                    yield ('placed', curr.right.key, curr.key, 'right')
                    return
                curr = curr.right

    def search(self, key: int):
        """Yields ('visit', node_key, found_boolean)"""
        curr = self.root
        while curr:
            if curr.key == key:
                yield ('visit', curr.key, True)
                return
            yield ('visit', curr.key, False)
            if key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        yield ('not_found', key, False)

    def delete(self, key: int):
        """Deletes a key, handling leaf, 1-child, and 2-child cases."""
        self.root, deleted = self._delete_node(self.root, key)
        if deleted:
            self._size -= 1
        return deleted

    def _delete_node(self, root: BSTNode, key: int):
        if root is None:
            return root, False

        deleted = False
        if key < root.key:
            root.left, deleted = self._delete_node(root.left, key)
        elif key > root.key:
            root.right, deleted = self._delete_node(root.right, key)
        else:
            deleted = True
            # Case 1 & 2: Leaf or one child
            if root.left is None:
                return root.right, True
            elif root.right is None:
                return root.left, True

            # Case 3: Two children -> find in-order successor (min in right subtree)
            successor = self._find_min_node(root.right)
            root.key = successor.key
            root.right, _ = self._delete_node(root.right, successor.key)

        return root, deleted

    def _find_min_node(self, node: BSTNode):
        curr = node
        while curr.left is not None:
            curr = curr.left
        return curr

    def find_min(self):
        if self.is_empty():
            return None
        return self._find_min_node(self.root).key

    def find_max(self):
        if self.is_empty():
            return None
        curr = self.root
        while curr.right:
            curr = curr.right
        return curr.key

    def inorder(self):
        """Inorder produces sorted keys."""
        res = []
        def _walk(node):
            if node:
                _walk(node.left)
                res.append(node.key)
                _walk(node.right)
        _walk(self.root)
        return res

    def preorder(self):
        res = []
        def _walk(node):
            if node:
                res.append(node.key)
                _walk(node.left)
                _walk(node.right)
        _walk(self.root)
        return res

    def postorder(self):
        res = []
        def _walk(node):
            if node:
                _walk(node.left)
                _walk(node.right)
                res.append(node.key)
        _walk(self.root)
        return res

    def clear(self):
        self.root = None
        self._size = 0