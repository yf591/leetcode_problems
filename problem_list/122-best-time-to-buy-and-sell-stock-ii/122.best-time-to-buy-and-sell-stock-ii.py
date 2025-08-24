#
# @lc app=leetcode id=122 lang=python3
#
# [122] Best Time to Buy and Sell Stock II
#


# @lc code=start
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # Initialize total profit to zero
        total_profit = 0

        # Iterate through the prices starting from the second day
        for i in range(1, len(prices)):
            # If the current price is greater than the previous day's price,
            # it means we can make a profit by buying on day i-1 and selling on day i.
            if prices[i] > prices[i - 1]:
                # Add this incremental profit to our total
                total_profit += prices[i] - prices[i - 1]

        # Return the total maximum profit
        return total_profit


# @lc code=end
