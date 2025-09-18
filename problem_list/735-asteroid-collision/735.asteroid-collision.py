#
# @lc app=leetcode id=735 lang=python3
#
# [735] Asteroid Collision
#


# @lc code=start
class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:

        # The stack will store the asteroids that have survived collisions so far.
        stack = []

        for new_ast in asteroids:
            # This loop handles the collisions for the new asteroid.
            # It continues as long as a collision is possible and the new asteroid
            # is still moving (hasn't exploded).
            while stack and new_ast < 0 and stack[-1] > 0:
                # Get the last asteroid from the stack (moving right).
                last_ast = stack[-1]

                # Case 1: Both asteroids are the same size; both explode.
                if abs(new_ast) == abs(last_ast):
                    stack.pop()  # Remove the last asteroid
                    break  # The new asteroid also explodes

                # Case 2: The asteroid on the stack is bigger.
                elif abs(last_ast) > abs(new_ast):
                    # The new asteroid explodes; the one on the stack survives.
                    break  # End the collision checks for the new asteroid.

                # Case 3: The new asteroid is bigger.
                else:  # abs(new_ast) > abs(last_ast)
                    # The asteroid on the stack explodes.
                    stack.pop()
                    # The loop continues to check the new asteroid against
                    # the next element on the stack.
            else:
                # This 'else' block runs if the 'while' loop's condition
                # was never met, or if it completed without hitting a 'break'.
                # This means the new asteroid survived all collisions.
                stack.append(new_ast)

        return stack


# @lc code=end
