#
# @lc app=leetcode id=94 lang=python3
#
# [94] Binary Tree Inorder Traversal
#


# @lc code=start
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # This list will store the values of the nodes in order.
        result = []

        # We use a helper function to perform the recursion.
        def dfs(node):
            # Base case: If the current node is null, we return.
            if not node:
                return

            # Traverse the left subtree.
            dfs(node.left)

            # Visit the current node (add its value to the result).
            result.append(node.val)

            # Traverse the right subtree.
            dfs(node.right)

        # Start the recursive traversal from the root of the tree.
        dfs(root)

        return result


# @lc code=end
