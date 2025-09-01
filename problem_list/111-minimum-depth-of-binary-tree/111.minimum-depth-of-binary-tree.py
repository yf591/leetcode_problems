#
# @lc app=leetcode id=111 lang=python3
#
# [111] Minimum Depth of Binary Tree
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        # Base case: If the tree is empty, the depth is 0.
        if not root:
            return 0

        # Initialize a queue for BFS. Store tuples of (node, depth).
        # The root is at depth 1.
        queue = collections.deque([(root, 1)])

        while queue:
            # Get the next node and its depth from the front of the queue.
            node, depth = queue.popleft()

            # Check if this node is a leaf (no children).
            if not node.left and not node.right:
                # Since BFS finds the shallowest leaf first, we can return its depth.
                return depth

            # If it's not a leaf, add its children to the queue for the next level.
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))


# @lc code=end
