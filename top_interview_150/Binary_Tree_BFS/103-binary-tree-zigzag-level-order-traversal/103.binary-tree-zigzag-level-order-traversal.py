#
# @lc app=leetcode id=103 lang=python3
#
# [103] Binary Tree Zigzag Level Order Traversal
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        # Handle the edge case of an empty tree.
        if not root:
            return []

        result = []
        queue = collections.deque([root])
        # A flag to track the traversal direction for the current level.
        left_to_right = True

        # Continue as long as there are levels to process.
        while queue:
            level_size = len(queue)
            current_level = []

            # Process all nodes for the current level.
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)

                # Enqueue children for the next level.
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            # If the direction for this level was right-to-left, reverse the list.
            if not left_to_right:
                current_level.reverse()

            result.append(current_level)

            # Flip the direction for the next level.
            left_to_right = not left_to_right

        return result


# @lc code=end
