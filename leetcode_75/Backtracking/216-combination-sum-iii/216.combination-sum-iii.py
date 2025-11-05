#
# @lc app=leetcode id=216 lang=python3
#
# [216] Combination Sum III
#


# @lc code=start
class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:

        results = []

        def backtrack(start_num: int, current_sum: int, current_path: List[int]):
            """
            A recursive helper to find combinations.
            :param start_num: The smallest number we are allowed to add next.
            :param current_sum: The sum of numbers in current_path.
            :param current_path: The list of numbers chosen so far.
            """

            # --- Base Case 1: Success ---
            # If we have the right number of elements AND the right sum.
            if len(current_path) == k:
                if current_sum == n:
                    # We must append a *copy* of the path.
                    results.append(list(current_path))
                # Stop this path: either we succeeded or len=k but sum!=n.
                return

            # --- Base Case 2: Pruning (Failure) ---
            # If we've gone too far, stop exploring this path.
            if len(current_path) > k or current_sum > n:
                return

            # --- Recursive Step ---
            # Try adding each number from 'start_num' to 9.
            for num in range(start_num, 10):
                # 1. Choose: Add the number to our current path.
                current_path.append(num)

                # 2. Explore: Recurse for the next number.
                # The next number must be at least 'num + 1'.
                backtrack(num + 1, current_sum + num, current_path)

                # 3. Unchoose (Backtrack): Remove the number to try the next
                #    number in the loop.
                current_path.pop()

        # Start the backtracking process.
        # We can start with any number from 1.
        # The initial sum is 0.
        # The initial path is empty.
        backtrack(1, 0, [])

        return results


# @lc code=end
