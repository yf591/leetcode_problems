#
# @lc app=leetcode id=714 lang=python3
#
# [714] Best Time to Buy and Sell Stock with Transaction Fee
#


# @lc code=start
class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        # 'cash': The max profit we have if we are NOT holding a stock.
        cash = 0
        # 'hold': The max profit we have if we ARE holding a stock.
        # Start at -infinity because it's impossible to hold a stock
        # before the first day, and this forces the first "buy".
        hold = -float("inf")

        for price in prices:
            # Store the 'cash' value from the previous day.
            prev_cash = cash

            # Update 'cash':
            # We can either:
            # 1. Do nothing (keep the 'cash' from yesterday).
            # 2. Sell the stock we were holding ('hold') for today's 'price', minus the 'fee'.
            cash = max(cash, hold + price - fee)

            # Update 'hold':
            # We can either:
            # 1. Do nothing (keep the 'hold' from yesterday).
            # 2. Buy a stock today, using the 'cash' we had yesterday.
            # We use 'prev_cash' to prevent selling and buying on the same day.
            hold = max(hold, prev_cash - price)

        # After iterating through all prices, the maximum profit is
        # the 'cash' state (we can't end with a stock, as we need cash profit).
        return cash


# @lc code=end
