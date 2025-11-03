#
# @lc app=leetcode id=1318 lang=python3
#
# [1318] Minimum Flips to Make a OR b Equal to c
#


# @lc code=start
class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:

        flips = 0

        # We continue as long as any of the numbers still have bits (are > 0)
        while a > 0 or b > 0 or c > 0:

            # Get the last bit (LSB) of each number
            a_bit = a & 1
            b_bit = b & 1
            c_bit = c & 1

            # Case 1: The target bit (c_bit) is 1
            if c_bit == 1:
                # We need (a_bit | b_bit) to be 1.
                # A flip is only needed if both are 0.
                if (a_bit | b_bit) == 0:
                    flips += 1

            # Case 2: The target bit (c_bit) is 0
            else:  # c_bit == 0
                # We need (a_bit | b_bit) to be 0.
                # This means both a_bit and b_bit must be 0.
                # We add 1 flip for each bit that is currently 1.
                flips += a_bit + b_bit

            # Right-shift all numbers to process the next bit position
            a >>= 1
            b >>= 1
            c >>= 1

        return flips


# @lc code=end
