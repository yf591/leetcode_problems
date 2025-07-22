#
# @lc app=leetcode id=20 lang=python3
#
# [20] Valid Parentheses
#


# @lc code=start
class Solution:
    def isValid(self, s: str) -> bool:
        # Use a list as a stack to keep track of opening brackets
        stack = []

        # Create a mapping of closing brackets to there opening conterparts
        bracket_map = {")": "(", "]": "[", "}": "{"}

        # Iterate through each character in the input string.
        for char in s:
            # If the character is a closing bracket...
            if char in bracket_map:
                # Check if the stack is empty or if the top of the stack
                # does not match the current closing bracket's opening pair.
                if not stack or stack[-1] != bracket_map[char]:
                    return False
                # If it matches, pop the opening bracket from the stack.
                stack.pop()
            else:
                # If it's an opening bracket , push it onto the stack.
                stack.append(char)

        # After the loop, if stack is empty, all brackets were correctly
        # matched and closed. If not, there are unclosed opening brackets.
        return not stack


# @lc code=end
