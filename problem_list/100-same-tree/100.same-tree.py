#
# @lc app=leetcode id=100 lang=python3
#
# [100] Same Tree
#


# @lc code=start
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        # Base case 1: If both nodes are None, They are identical.
        if not p and not q:
            return True

        # Base case 2: If one node is None, or if their values don't match,
        # they are not identical.
        if not p or not q or p.val != q.val:
            return False

        # Recursive Step: The trees are the same only if both their left
        # and right subtrees are also identical.
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)


# @lc code=end
