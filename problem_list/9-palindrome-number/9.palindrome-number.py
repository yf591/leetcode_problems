#
# @lc app=leetcode id=9 lang=python3
#
# [9] Palindrome Number
#


# @lc code=start
class Solution:
    def isPalindrome(self, x: int) -> bool:
        # As per the example, negative numbers are not palindromes
        if x < 0:
            return False
        # Convert the integer to a string and check if it equals its reverse
        # str(x)[::-1] is a Python trick to reverse a string
        return str(x) == str(x)[::-1]


# @lc code=end
