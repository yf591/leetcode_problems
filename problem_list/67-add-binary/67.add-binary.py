#
# @lc app=leetcode id=67 lang=python3
#
# [67] Add Binary
#


# @lc code=start
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        # Convert binary string 'a' an integer . The '2' tells the
        # int() function that the string is in base 2 (binary).
        int_a = int(a, 2)

        # Convert the binary string 'b' to an integer.
        int_b = int(b, 2)

        # Add the two integers together.
        sum_int = int_a + int_b

        # Convert the sum back to a binary string. the bin()
        # function return a string with a "0bA" prefix (e.g., "0b100").
        sum_bin = bin(sum_int)

        # Return the binary string, slicing off the "0b" prefix.
        return sum_bin[2:]


# @lc code=end
