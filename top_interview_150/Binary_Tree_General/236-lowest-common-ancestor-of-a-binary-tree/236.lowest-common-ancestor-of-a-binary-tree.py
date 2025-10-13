#
# @lc app=leetcode id=236 lang=python3
#
# [236] Lowest Common Ancestor of a Binary Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


class Solution:
    def lowestCommonAncestor(
        self, root: "TreeNode", p: "TreeNode", q: "TreeNode"
    ) -> "TreeNode":

        # Base Case: If the current node is null, or it's one of the nodes
        # we are looking for (p or q), return the current node.
        if not root or root == p or root == q:
            return root

        # Recursively search in the left and right subtrees.
        left_lca = self.lowestCommonAncestor(root.left, p, q)
        right_lca = self.lowestCommonAncestor(root.right, p, q)

        # --- Process the results from the children ---

        # If both children returned a non-null node, it means p and q
        # were found in different subtrees. Therefore, the current 'root'
        # is their lowest common ancestor.
        if left_lca and right_lca:
            return root

        # Otherwise, if only one of them returned a node, it means both p and q
        # are in that subtree. That returned node is the LCA.
        # This concisely returns the non-null child result, or None if both were null.
        return left_lca or right_lca


# @lc code=end
