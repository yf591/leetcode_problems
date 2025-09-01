#
# @lc app=leetcode id=110 lang=python3
#
# [110] Balanced Binary Tree
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:

        def check_height(node: Optional[TreeNode]) -> int:
            """
            This helper function returns the height of a node if it's balanced,
            or -1 if it's unbalanced.
            """
            # Base Case: An empty tree is balanced and has a height of 0.
            if not node:
                return 0

            # Recursively check the left subtree.
            left_height = check_height(node.left)
            # If the left subtree is unbalanced, propagate the failure signal up.
            if left_height == -1:
                return -1

            # Recursively check the right subtree.
            right_height = check_height(node.right)
            # If the right subtree is unbalanced, propagate the failure signal up.
            if right_height == -1:
                return -1

            # Check if the current node is balanced.
            if abs(left_height - right_height) > 1:
                return -1  # Signal that this node is the point of imbalance.

            # If it is balanced, return its height for the parent node to use.
            return 1 + max(left_height, right_height)

        # The entire tree is balanced if the check doesn't return the failure signal (-1).
        return check_height(root) != -1


# @lc code=end
