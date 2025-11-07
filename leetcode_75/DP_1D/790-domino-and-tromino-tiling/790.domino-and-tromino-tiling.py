#
# @lc app=leetcode id=790 lang=python3
#
# [790] Domino and Tromino Tiling
#


# @lc code=start
class Solution:
    def numTilings(self, n: int) -> int:

        # This problem has a recurrence relation:
        # f(n) = 2 * f(n-1) + f(n-3)
        # where f(n) is the number of ways to tile a 2 x n board.

        MOD = 10**9 + 7

        # Handle the base cases given by the relation's dependencies
        if n == 1:
            return 1
        if n == 2:
            return 2

        # We need to keep track of the last 3 states:
        # dp_minus_3 will be f(n-3)
        # dp_minus_2 will be f(n-2)
        # dp_minus_1 will be f(n-1)

        # Initialize for n = 3:
        dp_minus_3 = 1  # f(0)
        dp_minus_2 = 1  # f(1)
        dp_minus_1 = 2  # f(2)

        # Iterate from 3 up to n
        for i in range(3, n + 1):
            # Calculate the new f(i)
            # dp_current = 2 * f(i-1) + f(i-3)
            dp_current = (2 * dp_minus_1 + dp_minus_3) % MOD

            # "Slide" the variables for the next iteration
            dp_minus_3 = dp_minus_2
            dp_minus_2 = dp_minus_1
            dp_minus_1 = dp_current

        # The final answer is the last-calculated f(n)
        return dp_minus_1


# @lc code=end
