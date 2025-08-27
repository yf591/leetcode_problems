#
# @lc app=leetcode id=637 lang=python3
#
# [637] Average of Levels in Binary Tree
#

from typing import Optional, List
import collections


# @lc code=start
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        # Handle the edge case of an empty tree
        if not root:
            return []

        averages = []
        # A deque (double-ended queue) is an efficient queue implementation.
        queue = collections.deque([root])

        # Loop as long as there are levels to process.
        while queue:
            level_sum = 0
            level_size = len(queue)

            # Process all nodes on the current level.
            for _ in range(level_size):
                node = queue.popleft()
                level_sum += node.val

                # Add its children to the back of the queue for the next level.
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            # Calculate the average for the level and add it to the results.
            averages.append(level_sum / level_size)

        return averages


# @lc code=end
