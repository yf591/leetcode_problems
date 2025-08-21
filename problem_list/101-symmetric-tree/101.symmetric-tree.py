#
# @lc app=leetcode id=101 lang=python3
#
# [101] Symmetric Tree
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        # A tree with no root is considered symmetric.
        if not root:
            return True

        # Start the recursive check on the left and right children of the root.
        return self.isMirror(root.left, root.right)

    def isMirror(self, node1: Optional[TreeNode], node2: Optional[TreeNode]) -> bool:
        # --- Base Cases (Stopping Conditions) ---

        # If both nodes are None, they are symmetric.
        if not node1 and not node2:
            return True

        # If only one of the nodes is None, they are not symmetric.
        if not node1 or not node2:
            return False

        # --- Recursive Step ---

        # The two nodes are mirrors if:
        # 1. Their values are equal.
        # 2. The left child of node1 is a mirror of the right child of node2.
        # 3. The right child of node1 is a mirror of the left child of node2.
        return (
            node1.val == node2.val
            and self.isMirror(node1.left, node2.right)
            and self.isMirror(node1.right, node2.left)
        )


# @lc code=end
