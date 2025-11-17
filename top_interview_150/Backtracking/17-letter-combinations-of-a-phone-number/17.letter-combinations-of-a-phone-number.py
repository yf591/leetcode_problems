#
# @lc app=leetcode id=17 lang=python3
#
# [17] Letter Combinations of a Phone Number
#


# @lc code=start
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:

        # Handle the edge case of an empty input string.
        if not digits:
            return []

        # Mapping from digits to letters.
        digit_to_char = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }

        # List to store the final combinations.
        result = []

        def backtrack(index: int, current_combination: str):
            # Base Case: If the current combination is the desired length,
            # we've found a complete combination. Add it to the result.
            if len(current_combination) == len(digits):
                result.append(current_combination)
                return  # Stop exploring this path

            # Recursive Step: Explore letters for the current digit.
            current_digit = digits[index]
            possible_letters = digit_to_char[current_digit]

            for letter in possible_letters:
                # Make a choice (add the letter) and explore further.
                backtrack(index + 1, current_combination + letter)
                # No explicit "undo" needed here because we pass a new string
                # in the recursive call, effectively branching.

        # Start the backtracking process from the first digit (index 0)
        # with an empty combination string.
        backtrack(0, "")

        return result


# @lc code=end
