#
# @lc app=leetcode id=69 lang=python3
#
# [69] Sqrt(x)
#


# @lc code=start
class Solution:
    def mySqrt(self, x: int) -> int:
        # Handle the edge case for x = 0.
        if x == 0:
            return 0

        # Set up the search range for binary search.
        low, high = 1, x
        result = 0

        while low <= high:
            # Calculate the middle of the current range.
            mid = low + (high - low) // 2

            # Check if mid*mid is the square root.
            # To avoid potential overflow with mid*mid, we can use division.
            # If mid == x / mid, but it's safer to just check if mid*mid <= x.
            if mid * mid <= x:
                # mid could be our answer (since we round down).
                # Store it and try to find a larger integer square root.
                result = mid
                low = mid + 1
            else:
                # mid is too large, so we search in the left half.
                high = mid - 1

        return result


# @lc code=end
