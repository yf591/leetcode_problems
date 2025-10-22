#
# @lc app=leetcode id=450 lang=python3
#
# [450] Delete Node in a BST
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:

        # Base case: If the tree/subtree is empty, return None.
        if not root:
            return None

        # --- Search Phase ---
        if key < root.val:
            # The key must be in the left subtree.
            # Recursively call deleteNode on the left child and update the left link.
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            # The key must be in the right subtree.
            # Recursively call deleteNode on the right child and update the right link.
            root.right = self.deleteNode(root.right, key)

        # --- Deletion Phase (key == root.val) ---
        else:
            # Case 1: Node is a leaf (no children) or has only one child.
            if not root.left:
                # If no left child, replace the node with its right child (or None if no right child).
                return root.right
            elif not root.right:
                # If no right child, replace the node with its left child.
                return root.left

            # Case 3: Node has two children.
            else:
                # Find the in-order successor (smallest node in the right subtree).
                min_node = self.findMin(root.right)
                # Replace the current node's value with the successor's value.
                root.val = min_node.val
                # Recursively delete the successor node from the right subtree.
                root.right = self.deleteNode(
                    root.right, root.val
                )  # root.val now holds successor's value

        # Return the potentially modified root of the current subtree.
        return root

    def findMin(self, node: TreeNode) -> TreeNode:
        """Helper function to find the node with the minimum value in a BST subtree."""
        current = node
        # The minimum value is always the leftmost node.
        while current and current.left:
            current = current.left
        return current


# @lc code=end
