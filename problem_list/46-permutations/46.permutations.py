#
# @lc app=leetcode id=46 lang=python3
#
# [46] Permutations
#

from typing import List


# @lc code=start
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:

        results = []
        n = len(nums)

        def backtrack(current_path: List[int], visited_set: set):

            # Base Case: If the current permutation is the same size as nums,
            # we have a complete permutation.
            if len(current_path) == n:
                # Add a *copy* of the path to our results.
                results.append(list(current_path))
                return

            # Recursive Step: Try adding each number from the original list.
            for num in nums:
                # Only use numbers that we haven't already used in this path.
                if num not in visited_set:

                    # 1. Choose
                    current_path.append(num)
                    visited_set.add(num)

                    # 2. Explore
                    backtrack(current_path, visited_set)

                    # 3. Unchoose (Backtrack)
                    # This happens after the recursive call returns.
                    visited_set.remove(num)
                    current_path.pop()

        # Start the backtracking process with an empty path and an empty visited set.
        backtrack([], set())

        return results


# @lc code=end
