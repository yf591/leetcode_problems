#
# @lc app=leetcode id=872 lang=python3
#
# [872] Leaf-Similar Trees
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:

        def get_leaves(root: Optional[TreeNode]) -> List[int]:
            """
            A helper function to perform a DFS and return a list of leaf values.
            """
            leaf_sequence = []

            # Base case: If the tree is empty, there are no leaves.
            if not root:
                return []

            # A stack for an iterative DFS. We start with the root.
            stack = [root]

            while stack:
                node = stack.pop()

                # Check if the current node is a leaf.
                if not node.left and not node.right:
                    leaf_sequence.append(node.val)

                # Add children to the stack. We add the right child first
                # so that the left child is processed first (LIFO).
                if node.right:
                    stack.append(node.right)
                if node.left:
                    stack.append(node.left)

            return leaf_sequence

        # Get the leaf sequence for both trees.
        leaves1 = get_leaves(root1)
        leaves2 = get_leaves(root2)

        # Compare the two sequences for equality.
        return leaves1 == leaves2


# @lc code=end
