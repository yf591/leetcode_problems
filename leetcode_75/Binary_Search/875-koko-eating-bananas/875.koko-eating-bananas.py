#
# @lc app=leetcode id=875 lang=python3
#
# [875] Koko Eating Bananas
#


# @lc code=start
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:

        left = 1
        right = max(piles)
        min_speed = right

        while left <= right:
            speed = (left + right) // 2

            total_hours = 0
            for pile in piles:
                total_hours += (pile + speed - 1) // speed

            if total_hours <= h:
                min_speed = speed
                right = speed - 1

            else:
                left = speed + 1

        return min_speed


# @lc code=end
