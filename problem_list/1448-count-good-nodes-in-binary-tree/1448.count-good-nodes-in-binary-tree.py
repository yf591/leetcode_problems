#
# @lc app=leetcode id=1448 lang=python3
#
# [1448] Count Good Nodes in Binary Tree
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:

        def dfs(node: Optional[TreeNode], max_so_far: int) -> int:
            # Base Case: If we are at a null node, there are no good nodes here.
            if not node:
                return 0

            # Check if the current node is a "good node".
            # It's good if its value is >= the max value seen on the path to it.
            # Initialize our count for this subtree based on this check.
            count = 1 if node.val >= max_so_far else 0

            # Update the max value for the path going down to the children.
            # The new max is the greater of the old max and the current node's value.
            new_max = max(max_so_far, node.val)

            # Recursively call on the left and right children and add their results.
            count += dfs(node.left, new_max)
            count += dfs(node.right, new_max)

            # Return the total count of good nodes for the subtree at 'node'.
            return count

        # Start the recursion from the root.
        # We pass a very small number as the initial max_so_far to ensure
        # that the root node itself is always considered a good node.
        return dfs(root, float("-inf"))


# @lc code=end
