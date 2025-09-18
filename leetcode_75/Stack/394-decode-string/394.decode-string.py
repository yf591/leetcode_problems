#
# @lc app=leetcode id=394 lang=python3
#
# [394] Decode String
#


# @lc code=start
class Solution:
    def decodeString(self, s: str) -> str:

        stack = []
        current_num = 0
        current_string = ""

        for char in s:
            # If the character is a digit, build the number.
            if char.isdigit():
                current_num = current_num * 10 + int(char)

            # If it's an opening bracket, push the current state to the stack
            # and reset for the new nested string.
            elif char == "[":
                stack.append(current_string)
                stack.append(current_num)
                current_string = ""
                current_num = 0

            # If it's a closing bracket, decode the current string.
            elif char == "]":
                # Pop the number and the previous string from the stack.
                num = stack.pop()
                prev_string = stack.pop()

                # The new string is the previous one plus the current one repeated 'num' times.
                current_string = prev_string + current_string * num

            # If it's a letter, just append it to the current string.
            else:
                current_string += char

        return current_string


# @lc code=end
