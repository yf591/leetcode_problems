#
# @lc app=leetcode id=230 lang=python3
#
# [230] Kth Smallest Element in a BST
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        # The stack will store nodes we need to visit later.
        stack = []
        # Start the traversal at the root.
        current = root

        # The loop continues as long as there are nodes to process
        # or nodes stored in our stack.
        while current or stack:
            # 1. Go as far left as possible, pushing nodes onto the stack.
            while current:
                stack.append(current)
                current = current.left

            # 2. Pop the last node added—this is the next in-order element.
            current = stack.pop()

            # 3. "Visit" the node.
            k -= 1
            if k == 0:
                # If this is the k-th element we've visited, we're done.
                return current.val

            # 4. Move to the right subtree to continue the traversal.
            current = current.right


# @lc code=end
