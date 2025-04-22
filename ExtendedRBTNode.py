from RBTNode import RBTNode

class ExtendedRBTNode(RBTNode):
    def __init__(self, node_key):
        super().__init__(node_key)
        self.subtree_key_count = 1

    def get_subtree_key_count(self):
        return self.subtree_key_count

    def _update_subtree_key_count(self):
        left_count = self.left.subtree_key_count if self.left else 0
        right_count = self.right.subtree_key_count if self.right else 0
        self.subtree_key_count = 1 + left_count + right_count

    def set_left(self, new_left):
        super().set_left(new_left)
        self._update_subtree_key_count()
        if self.parent:
            self.parent._update_subtree_key_count()

    def set_right(self, new_right):
        super().set_right(new_right)
        self._update_subtree_key_count()
        if self.parent:
            self.parent._update_subtree_key_count()

    def set_key(self, new_key):
        super().set_key(new_key)
        self._update_subtree_key_count()
