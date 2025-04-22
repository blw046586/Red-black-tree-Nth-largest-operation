import logging
from ExtendedRBTNode import ExtendedRBTNode

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

class ExtendedRedBlackTree:
    def __init__(self):
        self.root = None

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

        # Update subtree key counts after rotation
        x.update_subtree_key_count()
        y.update_subtree_key_count()

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right:
            x.right.parent = y
        x.parent = y.parent
        if not y.parent:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

        # Update subtree key counts after rotation
        y.update_subtree_key_count()
        x.update_subtree_key_count()

    def insert(self, key):
        logging.debug(f"Inserting key: {key}")
        node = ExtendedRBTNode(key)
        y = None
        x = self.root

        while x:
            y = x
            if key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if not y:
            self.root = node
        elif key < y.key:
            y.left = node
        else:
            y.right = node

        self.fix_insert(node)

    def fix_insert(self, z):
        while z.parent and z.parent.color == 'red':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y and y.color == 'red':
                    z.parent.color = y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y and y.color == 'red':
                    z.parent.color = y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.left_rotate(z.parent.parent)
        self.root.color = 'black'
        self._update_counts_upward(z)

    def _update_counts_upward(self, node):
        while node:
            logging.debug(f"Updating subtree key count for node with key: {node.key}")
            node.update_subtree_key_count()
            node = node.parent

    def get_nth_key(self, n):
        if n < 0 or not self.root or n >= self.root.subtree_key_count:
            logging.error("Invalid value for n: Out of range")
            return None

        def helper(node, n):
            if not node:
                return None
            left_count = node.left.subtree_key_count if node.left else 0
            if n < left_count:
                return helper(node.left, n)
            elif n == left_count:
                return node.key
            else:
                return helper(node.right, n - left_count - 1)

        return helper(self.root, n)

    def in_order_traversal(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node.left:
            self.in_order_traversal(node.left, result)
        result.append(node.key)
        if node.right:
            self.in_order_traversal(node.right, result)
        return result
