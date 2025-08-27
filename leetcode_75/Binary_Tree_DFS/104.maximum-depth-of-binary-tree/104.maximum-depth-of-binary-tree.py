#
# @lc app=leetcode id=104 lang=python3
#
# [104] Maximum Depth of Binary Tree
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # Base case: If the current node is None, we've reached the end
        # of a branch, and its depth is 0.
        if not root:
            return 0

        # Recursively calculate the depth of the left subtree.
        left_depth = self.maxDepth(root.left)

        # Recursively calculate the depth of the right subtree.
        right_depth = self.maxDepth(root.right)

        # The depth of the current tree is 1 (for the current node)
        # plus the depth of its deepest child subtree.
        return 1 + max(left_depth, right_depth)


# @lc code=end
