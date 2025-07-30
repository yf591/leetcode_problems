#
# @lc app=leetcode id=70 lang=python3
#
# [70] Climbing Stairs
#


# @lc code=start
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        # This is a Fibonacci sequence. We only need the previous two values
        # to calculate the next one.
        # 'one_step_before' stores the ways to get to step (i-1).
        # 'two_steps_before' stores the ways to get to step (i-2).
        two_steps_before = 1  # Way to climb 1 step
        one_step_before = 2  # Way to climb 2 steps

        # Iterate from the 3rd step up to the n-th step.
        for i in range(3, n + 1):
            # The number of way to reach the current step is the sum of the ways
            # to reach the previous two steps.
            current_ways = one_step_before + two_steps_before

            # Update our pointers for the next iteration.
            two_steps_before = one_step_before
            one_step_before = current_ways

        # After the loop, 'one_step_before' holds the total ways for n steps.
        return one_step_before


# @lc code=end
