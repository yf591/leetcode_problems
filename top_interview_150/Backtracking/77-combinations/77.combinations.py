#
# @lc app=leetcode id=77 lang=python3
#
# [77] Combinations
#

from typing import List


# @lc code=start
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:

        result = []

        def backtrack(start_num: int, current_path: List[int]):

            if len(current_path) == k:
                result.append(list(current_path))
                return

            for num in range(start_num, n + 1):
                current_path.append(num)

                backtrack(num + 1, current_path)

                current_path.pop()

        backtrack(1, [])

        return result


# @lc code=end
