#
# @lc app=leetcode id=226 lang=python3
#
# [226] Invert Binary Tree
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # Base case: If the current node is None, we've reached the end
        # of a branch, so we just return.
        if not root:
            return None

        # --- The Swap ---
        # Swap the left and right children of the current node.
        # This is a Pythonic way to swap two variables in one line.
        root.left, root.right = root.right, root.left

        # --- The Recursive Calls ---
        # Recursively call the function on the children to invert their subtrees.
        self.invertTree(root.left)
        self.invertTree(root.right)

        # Return the root of the now-inverted tree.
        return root


# @lc code=end
