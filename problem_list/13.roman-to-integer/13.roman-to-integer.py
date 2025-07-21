#
# @lc app=leetcode id=13 lang=python3
#
# [13] Roman to Integer
#


# @lc code=start
class Solution:
    def romanToInt(self, s: str) -> int:
        # Map Roman numerals to integers
        roman_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

        total = 0

        # Iterate through the string from left to right
        for i in range(len(s)):
            # Chcke if the cuurent numeral is less than the next numeral
            # This indicates a subtranction case (like "IV" or "IX")
            if i + 1 < len(s) and roman_map[s[i]] < roman_map[s[i + 1]]:
                total -= roman_map[s[i]]
            else:
                # Otherwise, it's an addition case
                total += roman_map[s[i]]

        return total


# @lc code=end
