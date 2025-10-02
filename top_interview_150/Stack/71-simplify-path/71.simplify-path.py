#
# @lc app=leetcode id=71 lang=python3
#
# [71] Simplify Path
#


# @lc code=start
class Solution:
    def simplifyPath(self, path: str) -> str:

        # Use a list as a stack to keep track of the valid directory path.
        stack = []

        # Step 1: Split the path by '/' to get all components.
        # e.g., "/home//foo/" -> ['', 'home', '', 'foo', '']
        components = path.split("/")

        # Step 2: Iterate through each component.
        for component in components:
            # If the component is '..', go up one directory.
            if component == "..":
                # We can only go up if we are not at the root level (stack is not empty).
                if stack:
                    stack.pop()
            # If the component is not empty and not '.', it's a valid directory name.
            elif component and component != ".":
                # Go down into the directory by pushing it onto the stack.
                stack.append(component)
            # Otherwise, the component is '' or '.', which we ignore.

        # Step 3: Join the components in the stack to form the final path.
        # The result must start with a single '/'.
        return "/" + "/".join(stack)


# @lc code=end
