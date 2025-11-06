#
# @lc app=leetcode id=198 lang=python3
#
# [198] House Robber
#


# @lc code=start
class Solution:
    def rob(self, nums: List[int]) -> int:
        # We need two variables to store the max profit from two steps ago
        # and one step ago.

        # 'rob_prev' will hold the max profit from the previous house (i-1).
        # 'rob_prev_prev' will hold the max profit from the house two steps ago (i-2).
        rob_prev = 0
        rob_prev_prev = 0

        # Iterate through each house in the list.
        for current_money in nums:
            # We calculate the max profit we can have at this *current* house.
            # We have two choices:
            # 1. Skip this house: The profit is just the max profit from the previous house.
            #    (rob_prev)
            # 2. Rob this house: The profit is the current house's money plus the
            #    max profit from two houses ago.
            #    (current_money + rob_prev_prev)

            temp_max = max(current_money + rob_prev_prev, rob_prev)

            # Now, update our pointers for the next iteration:
            # The "previous" (rob_prev) now becomes the "two ago" (rob_prev_prev).
            rob_prev_prev = rob_prev
            # The "current max" (temp_max) now becomes the "previous" (rob_prev).
            rob_prev = temp_max

        # After the loop, 'rob_prev' will hold the max profit from the
        # very last house, which is our final answer.
        return rob_prev


# @lc code=end
