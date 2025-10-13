#
# @lc app=leetcode id=102 lang=python3
#
# [102] Binary Tree Level Order Traversal
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        # Handle the edge case of an empty tree.
        if not root:
            return []

        result = []
        # A deque (double-ended queue) is an efficient queue implementation.
        queue = collections.deque([root])

        # Loop as long as there are levels (nodes in the queue) to process.
        while queue:
            # Get the number of nodes on the current level.
            level_size = len(queue)
            # Create a list to store the values of the nodes on this level.
            current_level = []

            # Process all nodes for the current level.
            for _ in range(level_size):
                # Dequeue the node from the front of the queue.
                node = queue.popleft()
                # Add its value to this level's list.
                current_level.append(node.val)

                # Enqueue its children (if they exist) for the next level.
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            # Add the completed level's list to the final result.
            result.append(current_level)

        return result


# @lc code=end
