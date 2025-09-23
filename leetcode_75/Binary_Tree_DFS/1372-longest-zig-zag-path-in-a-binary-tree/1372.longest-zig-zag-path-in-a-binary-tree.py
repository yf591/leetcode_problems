#
# @lc app=leetcode id=1372 lang=python3
#
# [1372] Longest ZigZag Path in a Binary Tree
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        self.max_len = 0

        def dfs(node: Optional[TreeNode], go_left: bool, length: int):
            """
            A recursive function to explore zigzag paths.
            - go_left: True if the next move in the zigzag should be to the left.
            - length: The length of the current zigzag path.
            """
            if not node:
                return

            # Update the overall maximum length found so far.
            self.max_len = max(self.max_len, length)

            if go_left:
                # The zigzag continues by going left.
                dfs(node.left, False, length + 1)
                # We can also start a NEW path by going right.
                dfs(node.right, True, 1)
            else:  # go_right
                # The zigzag continues by going right.
                dfs(node.right, True, length + 1)
                # We can also start a NEW path by going left.
                dfs(node.left, False, 1)

        # Start the process. A path can start from the root by going
        # either left or right. The initial path has length 0.
        dfs(root, True, 0)

        return self.max_len


# @lc code=end
