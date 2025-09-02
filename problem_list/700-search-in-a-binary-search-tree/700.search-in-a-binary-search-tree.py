#
# @lc app=leetcode id=700 lang=python3
#
# [700] Search in a Binary Search Tree
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:

        # Start our search pointer at the root of the tree.
        current_node = root

        # Loop as long as we haven't fallen off the tree (current_node is not None).
        while current_node:
            # If we found the value, return the current node (and its subtree).
            if val == current_node.val:
                return current_node

            # If the target value is smaller, we know we must go left.
            elif val < current_node.val:
                current_node = current_node.left

            # Otherwise, the target value must be larger, so we go right.
            else:  # val > current_node.val
                current_node = current_node.right

        # If the loop finishes, it means we reached a null pointer,
        # so the value does not exist in the tree.
        return None


# @lc code=end
