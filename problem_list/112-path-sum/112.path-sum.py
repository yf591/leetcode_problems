#
# @lc app=leetcode id=112 lang=python3
#
# [112] Path Sum
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        # Base Case 1: If the tree is empty, there are no paths.
        if not root:
            return False

        # Subtract the current node's value from the sum we're looking for.
        remaining_sum = targetSum - root.val

        # Base Case 2: Check if the current node is a leaf.
        if not root.left and not root.right:
            # If it's a leaf, the path is valid only if the remaining sum is zero.
            return remaining_sum == 0

        # Recursive Step: If it's not a leaf, check the left and right subtrees.
        # Return True if a valid path is found in EITHER subtree.
        return self.hasPathSum(root.left, remaining_sum) or self.hasPathSum(
            root.right, remaining_sum
        )


# @lc code=end
