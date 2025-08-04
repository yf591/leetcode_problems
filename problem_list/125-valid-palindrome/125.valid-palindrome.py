#
# @lc app=leetcode id=125 lang=python3
#
# [125] Valid Palindrome
#


# @lc code=start
class Solution:
    def isPalindrome(self, s: str) -> bool:
        # Step 1: Create a new string containing only alphanumeric characters
        # from the orginal string, converted to lowercase.

        # We can build a new list of characters first.
        filtered_chars = []
        for char in s:
            # The isalnum() method checks if a character is a letter or number.
            if char.isalnum():
                filtered_chars.append(char.lower())

        # Join the list of characters into a single "cleaned" string.
        cleaned_s = "".join(filtered_chars)

        # Step 2: Check if the cleaned string is equal to its reverse.
        # The slice [::-1] is a common Python trick to reverse a string.
        return cleaned_s == cleaned_s[::-1]


# @lc code=end
