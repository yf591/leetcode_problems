#
# @lc app=leetcode id=39 lang=python3
#
# [39] Combination Sum
#

from typing import List


# @lc code=start
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        results = []

        # Sorting is not strictly necessary but can speed up the process
        # because we can break the loop early if the sum exceeds the target.
        candidates.sort()

        def backtrack(start_index: int, current_sum: int, current_path: List[int]):

            # --- Base Case 1: Success ---
            if current_sum == target:
                results.append(list(current_path))
                return

            # --- Base Case 2: Failure (Pruning) ---
            if current_sum > target:
                return

            # --- Recursive Step ---
            for i in range(start_index, len(candidates)):
                num = candidates[i]

                # Optimization: If adding the current number exceeds the target,
                # then adding any subsequent (larger) number will also fail.
                # We can break the loop early.
                if current_sum + num > target:
                    break

                # 1. Choose
                current_path.append(num)

                # 2. Explore
                # KEY DIFFERENCE: We pass 'i' as the start_index, NOT 'i + 1'.
                # This allows us to reuse the same number (candidates[i]) again.
                backtrack(i, current_sum + num, current_path)

                # 3. Unchoose (Backtrack)
                current_path.pop()

        # Start the process from the first candidate (index 0).
        backtrack(0, 0, [])

        return results


# @lc code=end
