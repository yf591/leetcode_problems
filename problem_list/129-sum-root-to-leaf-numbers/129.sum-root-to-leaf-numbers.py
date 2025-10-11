#
# @lc app=leetcode id=129 lang=python3
#
# [129] Sum Root to Leaf Numbers
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:

        def dfs(node: Optional[TreeNode], current_number: int) -> int:
            # Base Case 1: An empty branch contributes 0 to the sum.
            if not node:
                return 0

            # Update the number formed by the path down to the current node.
            current_number = current_number * 10 + node.val

            # Base Case 2: If the current node is a leaf, this path is complete.
            # We've found a full number, so we return it.
            if not node.left and not node.right:
                return current_number

            # Recursive Step: If it's not a leaf, the total sum from this point down
            # is the sum of the paths in the left subtree plus the sum of the paths
            # in the right subtree.
            return dfs(node.left, current_number) + dfs(node.right, current_number)

        # Start the entire recursive process from the root with an initial number of 0.
        return dfs(root, 0)


# @lc code=end
