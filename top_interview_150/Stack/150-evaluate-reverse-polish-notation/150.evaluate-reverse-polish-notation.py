#
# @lc app=leetcode id=150 lang=python3
#
# [150] Evaluate Reverse Polish Notation
#


# @lc code=start
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:

        # A list can be used as a stack in Python.
        stack = []

        for token in tokens:
            # Check if the token is an operator.
            if token == "+":
                # Pop the last two numbers, add them, and push the result.
                stack.append(stack.pop() + stack.pop())
            elif token == "-":
                # Order matters: b is popped first, then a. The operation is a - b.
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            elif token == "*":
                stack.append(stack.pop() * stack.pop())
            elif token == "/":
                b, a = stack.pop(), stack.pop()
                # Use int(a / b) to handle truncation towards zero correctly.
                stack.append(int(a / b))
            else:
                # If the token is not an operator, it's a number.
                # Convert it to an integer and push it onto the stack.
                stack.append(int(token))

        # The final result is the only item left on the stack.
        return stack[0]


# @lc code=end
