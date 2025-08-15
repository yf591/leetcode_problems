#
# @lc app=leetcode id=190 lang=python3
#
# [190] Reverse Bits
#


# @lc code=start
class Solution:
    def reverseBits(self, n: int) -> int:
        # Initialize our result to 0
        result = 0

        # We need to process all 32 bits of the input integer.
        for i in range(32):
            # 1. Shift the result to the left to make space for the next bit.
            result <<= 1

            # 2. Get the last bit of 'n' using the bitwise AND operator.
            last_bit = n & 1

            # 3. Add this bit to our result using the bitwise OR operator.
            result |= last_bit

            # 4. Discard the last bit of 'n' by shifting it to the right.
            n >>= 1

        return result


# @lc code=end
