class ExtendedRBTNode:
    def __init__(self, key, color='red', left=None, right=None, parent=None):
        self.key = key
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent
        self.subtree_key_count = 1  # counts self

    def update_subtree_key_count(self):
        left_count = self.left.subtree_key_count if self.left else 0
        right_count = self.right.subtree_key_count if self.right else 0
        self.subtree_key_count = 1 + left_count + right_count

    def get_subtree_key_count(self):
        return self.subtree_key_count
