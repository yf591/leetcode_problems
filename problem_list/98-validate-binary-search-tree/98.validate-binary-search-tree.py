#
# @lc app=leetcode id=98 lang=python3
#
# [98] Validate Binary Search Tree
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:

        def validate(node, lower_bound, upper_bound):
            # Base Case: An empty tree or leaf's child is a valid BST.
            if not node:
                return True

            # Check if the current node's value is within its valid range.
            if not (lower_bound < node.val < upper_bound):
                return False

            # Recursively check the left and right subtrees with updated bounds.
            # The left child's new upper bound is the parent's value.
            is_left_valid = validate(node.left, lower_bound, node.val)
            # The right child's new lower bound is the parent's value.
            is_right_valid = validate(node.right, node.val, upper_bound)

            # The tree is valid only if both subtrees are also valid.
            return is_left_valid and is_right_valid

        # Start the initial validation with the widest possible range.
        return validate(root, float("-inf"), float("inf"))
        return validate(root, float("-inf"), float("inf"))


# @lc code=end
