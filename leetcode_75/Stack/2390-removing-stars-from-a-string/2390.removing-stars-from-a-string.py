#
# @lc app=leetcode id=2390 lang=python3
#
# [2390] Removing Stars From a String
#


# @lc code=start
class Solution:
    def removeStars(self, s: str) -> str:

        # We can use a list as a stack to build the result.
        stack = []

        # Iterate through each character of the input string.
        for char in s:
            # If the character is a star, it removes the last added character.
            # This is equivalent to popping from the stack.
            if char == "*":
                # The problem guarantees this operation is always possible,
                # so the stack will not be empty when we pop.
                if stack:  # if len(stack) > 0:
                    stack.pop()
            # If it's a normal character, add it to our result.
            # This is equivalent to pushing onto the stack.
            else:
                stack.append(char)

        # Join the characters remaining in the stack to form the final string.
        return "".join(stack)


# @lc code=end
