#
# @lc app=leetcode id=437 lang=python3
#
# [437] Path Sum III
#


# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        # A map to store prefix sums and their frequencies: {prefix_sum: count}
        self.prefix_sum_counts = collections.defaultdict(int)
        # Initialize with {0: 1} to handle paths that start from the root itself.
        self.prefix_sum_counts[0] = 1

        self.count = 0
        self.dfs(root, 0, targetSum)
        return self.count

    def dfs(self, node: Optional[TreeNode], current_path_sum: int, targetSum: int):
        # Base case: if node is null, end this path.
        if not node:
            return

        # 1. Update the current path sum.
        current_path_sum += node.val

        # 2. Check if a path ending at this node sums to targetSum.
        # This happens if (current_path_sum - targetSum) is a known prefix sum.
        self.count += self.prefix_sum_counts[current_path_sum - targetSum]

        # 3. Add the current path sum to the map for its descendants to use.
        self.prefix_sum_counts[current_path_sum] += 1

        # 4. Recurse on children.
        self.dfs(node.left, current_path_sum, targetSum)
        self.dfs(node.right, current_path_sum, targetSum)

        # 5. Backtrack: When leaving this node's path, remove its prefix sum
        # from the map so it doesn't affect sibling paths. This is crucial.
        self.prefix_sum_counts[current_path_sum] -= 1


# @lc code=end
