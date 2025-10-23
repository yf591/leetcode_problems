#
# @lc app=leetcode id=844 lang=python3
#
# [844] Backspace String Compare
#


# @lc code=start
class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:

        def build(input_str: str) -> str:
            """
            Builds the final string after processing backspaces.
            """
            stack = []
            for char in input_str:
                if char == "#":
                    # If stack is not empty, pop the last character
                    if stack:
                        stack.pop()
                else:
                    # If it's a letter, push onto the stack
                    stack.append(char)
            # Join the characters remaining in the stack
            return "".join(stack)

        # Build the final strings for s and t
        final_s = build(s)
        final_t = build(t)

        # Compare the final strings
        return final_s == final_t


# @lc code=end
