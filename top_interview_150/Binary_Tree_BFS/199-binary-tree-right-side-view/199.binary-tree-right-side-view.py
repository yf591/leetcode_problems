#
# @lc app=leetcode id=199 lang=python3
#
# [199] Binary Tree Right Side View
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        # Handle the edge case of an empty tree.
        if not root:
            return []

        result = []
        # A deque (double-ended queue) is an efficient queue implementation.
        queue = collections.deque([root])

        # Loop as long as there are levels to process.
        while queue:
            # The rightmost node of the current level is the last element
            # currently in the queue. We add its value to our result.
            rightmost_node = queue[-1]
            result.append(rightmost_node.val)

            # Now, process all nodes on the current level to add their
            # children to the queue for the next level.
            level_size = len(queue)
            for _ in range(level_size):
                # Remove a node from the front of the queue.
                node = queue.popleft()

                # Add its children (if they exist) to the back of the queue.
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result


# @lc code=end
