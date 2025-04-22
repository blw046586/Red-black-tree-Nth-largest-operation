from RedBlackTree import RedBlackTree
from ExtendedRBTNode import ExtendedRBTNode
from RBTNode import RBTNode

class ExtendedRedBlackTree(RedBlackTree):
    def __init__(self):
        super().__init__()
        self.visited_nodes = []

    def make_new_node(self, key):
        return ExtendedRBTNode(key)

    def insert_key(self, key):
        new_node = self.make_new_node(key)
        self.insert_node(new_node)
        return new_node

    def insert_node(self, node):
        super().insert_node(node)
        self._update_subtree_counts_upward(node)

    def remove_node(self, node):
        if not node:
            return False

        # Case 1: Node has two children
        if node.get_left() and node.get_right():
            # Step 1: Find predecessor
            predecessor = node.get_left()
            while predecessor.get_right():
                predecessor = predecessor.get_right()

            # Step 2: Store key and parent
            pred_key = predecessor.get_key()
            parent_of_predecessor = predecessor.parent

            # Step 3: Prepare predecessor if black
            if predecessor.is_black():
                self.prepare_for_removal(predecessor)

            # Step 4: Remove predecessor using base method
            super().remove_node(predecessor)

            # Step 5: Replace node's key AFTER removal
            node.set_key(pred_key)

            # Step 6: Update counts from both node and predecessor's parent
            self._update_subtree_counts_upward(node)
            self._update_subtree_counts_upward(parent_of_predecessor)
            return True

        # Case 2: Node has 0 or 1 child
        if node.is_black():
            self.prepare_for_removal(node)

        result = super().remove_node(node)

        if self.root and self.root.is_red():
            self.root.color = RBTNode.black

        self._update_subtree_counts_upward(node.parent if node else None)
        return result

    def _left_rotate(self, node):
        rotated = super()._left_rotate(node)
        node._update_subtree_key_count()
        rotated._update_subtree_key_count()
        if rotated.parent:
            rotated.parent._update_subtree_key_count()
        return rotated

    def _right_rotate(self, node):
        rotated = super()._right_rotate(node)
        node._update_subtree_key_count()
        rotated._update_subtree_key_count()
        if rotated.parent:
            rotated.parent._update_subtree_key_count()
        return rotated

    def _update_subtree_counts_upward(self, node):
        while node:
            node._update_subtree_key_count()
            node = node.parent

    def get_nth_key(self, n):
        self.visited_nodes = []
        if not self.root:
            return None
        return self._get_nth_key_recursive(self.root, n)

    def _get_nth_key_recursive(self, node, n):
        self.visited_nodes.append(node)

        left = node.get_left()
        left_count = left.get_subtree_key_count() if left else 0

        if n == left_count:
            return node.get_key()
        elif n < left_count:
            return self._get_nth_key_recursive(left, n)
        else:
            return self._get_nth_key_recursive(node.get_right(), n - left_count - 1)
