#
# @lc app=leetcode id=108 lang=python3
#
# [108] Convert Sorted Array to Binary Search Tree
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:

        def build_tree(left_index, right_index):
            # Base case: If the pointers cross, it means the subarray is empty,
            # so we return None to signify no node.
            if left_index > right_index:
                return None

            # Finde the middle index  of the current subarray.
            mid_index = (left_index + right_index) // 2

            # The middle element becomes the root of this subtree.
            root = TreeNode(nums[mid_index])

            # Recursively build the left subtree from the left half of the array.
            root.left = build_tree(left_index, mid_index - 1)

            # Recursively build the right subtree from the right half of the array.
            root.right = build_tree(mid_index + 1, right_index)

            return root

        # Start the recursive process with the entire array.
        return build_tree(0, len(nums) - 1)


# @lc code=end
