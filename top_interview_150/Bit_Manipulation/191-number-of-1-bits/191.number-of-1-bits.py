#
# @lc app=leetcode id=191 lang=python3
#
# [191] Number of 1 Bits
#


# @lc code=start
class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0

        # Loop until all bits have been checked (n becomes 0).
        while n > 0:
            # The expression (n & 1) isolates the last bit.
            # If the last bit is 1, it will be True.
            if n & 1:
                count += 1

            # Right-shift the number to process the next bit in the next iteration.
            n >>= 1

        return count


# @lc code=end
