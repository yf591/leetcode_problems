#
# @lc app=leetcode id=22 lang=python3
#
# [22] Generate Parentheses
#


# @lc code=start
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:

        # This list will hold all valid combinations found
        result = []

        def backtrack(current_string, open_count, close_count):
            # Base Case: If the string is the correct length (n pairs = 2*n chars),
            # we have found a valid combination.
            if len(current_string) == n * 2:
                result.append(current_string)
                return

            # Decision 1: Add an open bracket if we still have some left.
            if open_count < n:
                backtrack(current_string + "(", open_count + 1, close_count)

            # Decision 2: Add a close bracket if it balances an open bracket.
            # We can only close if we have more open brackets than closed ones.
            if close_count < open_count:
                backtrack(current_string + ")", open_count, close_count + 1)

        # Start the backtracking with an empty string and 0 counts
        backtrack("", 0, 0)

        return result


# @lc code=end
