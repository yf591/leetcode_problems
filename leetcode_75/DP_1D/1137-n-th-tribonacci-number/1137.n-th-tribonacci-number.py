#
# @lc app=leetcode id=1137 lang=python3
#
# [1137] N-th Tribonacci Number
#


# @lc code=start
class Solution:
    def tribonacci(self, n: int) -> int:

        if n == 0:
            return 0

        if n == 1 or n == 2:
            return 1

        t0 = 0
        t1 = 1
        t2 = 1

        for _ in range(3, n + 1):
            next_tribe = t0 + t1 + t2

            t0, t1, t2 = t1, t2, next_tribe

        return t2


# @lc code=end
