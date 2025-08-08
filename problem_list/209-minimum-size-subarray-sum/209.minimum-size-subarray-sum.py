#
# @lc app=leetcode id=209 lang=python3
#
# [209] Minimum Size Subarray Sum
#


# @lc code=start
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        # 'left' is the starting pointer of our window.
        left = 0

        # 'current_sum' is the sum of the elements inside the current window.
        current_sum = 0

        # 'min_length' stores the smallest valid window length found so far.
        # Initialize it to a very large number.
        min_length = float("inf")

        # 'right' is the ending pointer, which expands the window.
        for right in range(len(nums)):
            # Add the new element to the window's sum.
            current_sum += nums[right]

            # Check if the current window is valid. If so, try to shrink it.
            while current_sum >= target:
                # We have a valid window so update our minimum length.
                current_length = right - left + 1
                min_length = min(min_length, current_length)

                # Shrink the window from the left to find a smaller valid window.
                current_sum -= nums[left]
                left += 1

        # If min_length was never updated, no valid subarray was found.
        if min_length == float("inf"):
            return 0
        else:
            return min_length


# @lc code=end
