#
# @lc app=leetcode id=202 lang=python3
#
# [202] Happy Number
#


# @lc code=start
class Solution:
    def isHappy(self, n: int) -> bool:

        def get_sum_of_squares(num: int) -> int:
            """Helper function to calculate the sum of the squares of the digits."""
            output = 0
            while num > 0:
                digit = num % 10
                output += digit**2
                num //= 10
            return output

        # A set to store numbers we've already seen to detect a cycle.
        seen = set()

        # Continue the process as long as n is not 1 and we haven't seen n before.
        while n != 1 and n not in seen:
            # Add the current number to our set of seen numbers.
            seen.add(n)
            # Calculate the next number in the sequence.
            n = get_sum_of_squares(n)

        # If the loop ended, it's either because n is 1 (happy) or
        # because we found a cycle (n is in seen, but is not 1).
        # We can just check if n is 1 to get the final answer.
        return n == 1


# @lc code=end
