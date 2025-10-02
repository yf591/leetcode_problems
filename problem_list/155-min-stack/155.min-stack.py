#
# @lc app=leetcode id=155 lang=python3
#
# [155] Min Stack
#


# @lc code=start
class MinStack:

    def __init__(self):
        """
        Initializes the two stacks.
        """
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        """
        Pushes a value onto the main stack and updates the min_stack.
        """
        # Always push the new value onto the main stack.
        self.stack.append(val)

        # For the min_stack, decide what the new current minimum is.
        if not self.min_stack:
            # If the min_stack is empty, the new value is the first minimum.
            self.min_stack.append(val)
        else:
            # The new minimum is the smaller of the new value and the previous minimum.
            current_min = self.min_stack[-1]
            self.min_stack.append(min(val, current_min))

    def pop(self) -> None:
        """
        Pops from both stacks to keep them in sync.
        """
        # The problem guarantees pop is called on a non-empty stack.
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        """
        Returns the top of the main stack.
        """
        return self.stack[-1]

    def getMin(self) -> int:
        """
        Returns the current overall minimum, which is always at the top of min_stack.
        """
        return self.min_stack[-1]


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
# @lc code=end
