#
# @lc app=leetcode id=1161 lang=python3
#
# [1161] Maximum Level Sum of a Binary Tree
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        if not root:  # Although constraints say >= 1 node, good practice
            return 0

        max_sum = float("-inf")
        result_level = 0
        current_level_number = 1

        queue = collections.deque([root])

        while queue:
            level_size = len(queue)
            current_level_sum = 0

            # Process all nodes on the current level
            for _ in range(level_size):
                node = queue.popleft()
                current_level_sum += node.val

                # Add children for the next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            # Check if this level's sum is the new maximum
            if current_level_sum > max_sum:
                max_sum = current_level_sum
                result_level = current_level_number

            # Move to the next level number
            current_level_number += 1

        return result_level


# @lc code=end
