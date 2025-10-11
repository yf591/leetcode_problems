#
# @lc app=leetcode id=114 lang=python3
#
# [114] Flatten Binary Tree to Linked List
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        # 'self.prev' will keep track of the previously visited node,
        # which will be the head of the already-flattened part of the list.
        self.prev = None

        def dfs(node: Optional[TreeNode]):
            if not node:
                return

            # Traverse in reverse pre-order: Right, then Left, then Root.
            dfs(node.right)
            dfs(node.left)

            # --- Re-wire the pointers ---
            # Set the current node's right pointer to the head of the
            # list we've built so far (stored in self.prev).
            node.right = self.prev
            # Set the left pointer to None as required.
            node.left = None
            # The current node is now the new head of our flattened list.
            self.prev = node

        dfs(root)


# @lc code=end
