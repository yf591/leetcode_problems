#
# @lc app=leetcode id=222 lang=python3
#
# [222] Count Complete Tree Nodes
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        # Helper to find height by just going left. This is fast (O(log n)).
        def get_height(node):
            h = 0
            while node:
                h += 1
                node = node.left
            return h

        left_height = get_height(root.left)
        right_height = get_height(root.right)

        if left_height == right_height:
            # If heights are equal, the left subtree is a perfect binary tree.
            # Its size is 2^h. We add 1 for the root, and then recursively
            # count the nodes in the right subtree.
            # (1 << left_height) is a fast way to calculate 2^left_height.
            return (1 << left_height) + self.countNodes(root.right)
        else:
            # If heights are not equal, the right subtree is a perfect binary tree.
            # Its size is 2^h. We add 1 for the root, and then recursively
            # count the nodes in the left subtree.
            return (1 << right_height) + self.countNodes(root.left)


# @lc code=end
