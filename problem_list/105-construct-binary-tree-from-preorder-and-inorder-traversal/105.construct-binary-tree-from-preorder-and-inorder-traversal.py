#
# @lc app=leetcode id=105 lang=python3
#
# [105] Construct Binary Tree from Preorder and Inorder Traversal
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:

        # Create a hash map for fast lookups of a value's index in the inorder list.
        inorder_map = {val: i for i, val in enumerate(inorder)}

        # A pointer to the current root in the preorder traversal.
        self.preorder_index = 0

        def build_helper(in_left_idx, in_right_idx):
            """
            Recursive helper to build a tree from the inorder slice
            defined by in_left_idx and in_right_idx.
            """
            # Base case: If there are no elements to construct the tree.
            if in_left_idx > in_right_idx:
                return None

            # The first element in the current preorder segment is the root.
            root_val = preorder[self.preorder_index]
            self.preorder_index += 1  # Move to the next root for subsequent calls.

            # Create the root node for this subtree.
            root = TreeNode(root_val)

            # Find the root's index in the inorder list to partition it.
            inorder_root_idx = inorder_map[root_val]

            # Recursively build the left subtree.
            # The left subtree's inorder elements are from in_left_idx to inorder_root_idx - 1.
            root.left = build_helper(in_left_idx, inorder_root_idx - 1)

            # Recursively build the right subtree.
            # The right subtree's inorder elements are from inorder_root_idx + 1 to in_right_idx.
            root.right = build_helper(inorder_root_idx + 1, in_right_idx)

            return root

        # Start the recursive construction with the entire range of the inorder list.
        return build_helper(0, len(inorder) - 1)


# @lc code=end
