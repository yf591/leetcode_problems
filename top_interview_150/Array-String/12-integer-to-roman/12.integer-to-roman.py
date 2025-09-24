#
# @lc app=leetcode id=12 lang=python3
#
# [12] Integer to Roman
#


# @lc code=start
class Solution:
    def intToRoman(self, num: int) -> str:

        # Create a mapping of values to Roman numeral symbols,
        # including the special subtractive cases.
        # It's crucial that this is ordered from largest to smallest.
        symbols = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]

        # A list to build our result string efficiently.
        result = []

        # Greedily subtract the largest possible values.
        for value, symbol in symbols:
            # While the number is large enough to subtract the current value...
            while num >= value:
                # ...append the corresponding symbol to our result...
                result.append(symbol)
                # ...and subtract the value from our number.
                num -= value

        # Join the list of symbols into the final string.
        return "".join(result)


# @lc code=end
