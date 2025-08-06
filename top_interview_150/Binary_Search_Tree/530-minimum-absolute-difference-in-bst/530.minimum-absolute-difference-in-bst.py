#
# @lc app=leetcode id=530 lang=python3
#
# [530] Minimum Absolute Difference in BST
#

from typing import Optional, List


# @lc code=start
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        # We need to track minimum difference and the value of the previous node.
        self.min_difference = float("inf")
        self.prev_node_val = None

        def inorder_traversal(node):
            # Base case for recursion
            if not node:
                return

            # Traverse the left subtree.
            inorder_traversal(node.left)

            # Visit the current node.
            # If this is not the first node we've visited...
            if self.prev_node_val is not None:
                # ...calculate the difference and update the minimum.
                self.min_difference = min(
                    self.min_difference, node.val - self.prev_node_val
                )

            # Update the previous node's value fof the next comparision.
            self.prev_node_val = node.val

            # Traverse the right subtree.
            inorder_traversal(node.right)

        # Start the traversal from the root.
        inorder_traversal(root)

        return self.min_difference


# @lc code=end
