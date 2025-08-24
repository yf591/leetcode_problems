#
# @lc app=leetcode id=55 lang=python3
#
# [55] Jump Game
#


# @lc code=start
class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_reach = 0
        n = len(nums)

        for i, max_jump in enumerate(nums):
            if i > max_reach:
                return False

            max_reach = max(max_reach, i + max_jump)

            if max_jump >= n - 1:
                return True

        return True


# @lc code=end
