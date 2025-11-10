#
# @lc app=leetcode id=901 lang=python3
#
# [901] Online Stock Span
#


# @lc code=start
class StockSpanner:

    def __init__(self):
        # The stack will store tuples of (price, span)
        # It will be a monotonically decreasing stack (by price)
        self.stack = []

    def next(self, price: int) -> int:
        # Start with a span of 1 (for today's price)
        current_span = 1

        # As long as the stack is not empty AND
        # today's price is greater than or equal to the price at the top of the stack...
        while self.stack and price >= self.stack[-1][0]:
            # ...it means the new price's span can "absorb" the previous day's span.
            # Pop the previous item (price, span)
            popped_price, popped_span = self.stack.pop()
            # Add its span to our current span
            current_span += popped_span

        # After the loop, the stack is either empty or the top
        # element is a "blocker" (a price greater than the current one).

        # Add the new price and its calculated span to the stack.
        self.stack.append((price, current_span))

        # Return the span we just calculated.
        return current_span


# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)
# @lc code=end
