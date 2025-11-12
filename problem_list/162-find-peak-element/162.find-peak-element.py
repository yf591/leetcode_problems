#
# @lc app=leetcode id=162 lang=python3
#
# [162] Find Peak Element
#


# @lc code=start
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:

        # Initialize the search space boundaries.
        left = 0
        # The right boundary is the last index.
        right = len(nums) - 1

        # Standard binary search loop.
        # We use 'left < right' because 'right' is a valid index,
        # and the loop will terminate when left == right.
        while left < right:
            # Calculate the middle index.
            mid = (left + right) // 2

            # Case 1: We are on an "uphill" slope (e.g., ...4, 5...)
            # A peak must be to our right.
            if nums[mid] < nums[mid + 1]:
                # Discard the left half, including 'mid'.
                left = mid + 1

            # Case 2: We are on a "downhill" slope (e.g., ...5, 4...)
            # The peak is either at 'mid' or to its left.
            else:
                # Discard the right half, but keep 'mid' as a
                # potential peak.
                right = mid

        # When the loop terminates, 'left' and 'right' will be at the
        # same index, which is guaranteed to be a peak.
        return left


# @lc code=end
