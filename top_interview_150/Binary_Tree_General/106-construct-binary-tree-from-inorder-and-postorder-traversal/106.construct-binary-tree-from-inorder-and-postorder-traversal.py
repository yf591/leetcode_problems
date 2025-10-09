#
# @lc app=leetcode id=106 lang=python3
#
# [106] Construct Binary Tree from Inorder and Postorder Traversal
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:

        # Create a hash map for O(1) lookups of a value's index in the inorder list.
        inorder_map = {val: i for i, val in enumerate(inorder)}

        # A pointer to the current root in the postorder traversal, starting from the end.
        self.postorder_index = len(postorder) - 1

        def build_helper(in_left_idx, in_right_idx):
            """
            Recursive helper to build a tree from the inorder slice
            defined by in_left_idx and in_right_idx.
            """
            # Base case: If there are no elements to construct the tree.
            if in_left_idx > in_right_idx:
                return None

            # The current root is the last element in the current postorder segment.
            root_val = postorder[self.postorder_index]
            self.postorder_index -= 1  # Move to the root of the next subtree.

            root = TreeNode(root_val)

            # Find the root's index in the inorder list to find the partition point.
            inorder_root_idx = inorder_map[root_val]

            # --- CRITICAL STEP ---
            # Recursively build the RIGHT subtree first. This is because we are
            # consuming the postorder list from the end, and the right subtree's
            # elements appear just before the root in a postorder traversal.
            root.right = build_helper(inorder_root_idx + 1, in_right_idx)

            # Then, recursively build the left subtree.
            root.left = build_helper(in_left_idx, inorder_root_idx - 1)

            return root

        # Start the recursive construction with the entire range of the inorder list.
        return build_helper(0, len(inorder) - 1)


# @lc code=end
