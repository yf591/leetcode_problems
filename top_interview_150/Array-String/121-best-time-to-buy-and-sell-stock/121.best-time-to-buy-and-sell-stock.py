#
# @lc app=leetcode id=121 lang=python3
#
# [121] Best Time to Buy and Sell Stock
#


# @lc code=start
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # Initialize the minimum price to a very large number.
        min_price_so_far = float("inf")
        # Initialize the maximum profit to 0, as we can't have negative profit.
        max_profit = 0

        # Iterate through each price in the list.
        for price in prices:
            # First, we check what the profit would be if we sold on the current day.
            # The best buy price would be the minimum price we've seen so far.
            potential_profit = price - min_price_so_far

            # We update our max_profit if this potential profit is better.
            max_profit = max(max_profit, potential_profit)

            # After checking for profit, we update our minimum price for the next day.
            # Is today's price a new low?
            min_price_so_far = min(min_price_so_far, price)

        return max_profit


# @lc code=end
