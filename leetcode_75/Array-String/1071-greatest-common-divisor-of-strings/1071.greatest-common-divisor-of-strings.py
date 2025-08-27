#
# @lc app=leetcode id=1071 lang=python3
#
# [1071] Greatest Common Divisor of Strings
#


# @lc code=start
class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        # Step 1: Check if a common divisor string is even possible.
        # If str1 + str2 is not the same as str2 + str1, no solution exists.
        if str1 + str2 != str2 + str1:
            return ""

        # Step 2: Find the greatest common divisor of the two lengths.
        # This will be the length of our result string.
        len1 = len(str1)
        len2 = len(str2)
        gcd_length = math.gcd(len1, len2)

        # Step 3: The result is the prefix of either string with that GCD length.
        return str1[:gcd_length]


# @lc code=end
