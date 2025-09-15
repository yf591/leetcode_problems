#
# @lc app=leetcode id=1493 lang=python3
#
# [1493] Longest Subarray of 1's After Deleting One Element
#


# @lc code=start
class Solution:
    def longestSubarray(self, nums: List[int]) -> int:

        left = 0
        zero_count = 0
        max_window_len = 0

        # 'right' pointer expands the window by iterating through the array.
        for right in range(len(nums)):
            # If the new element entering the window is a zero, increment our count.
            if nums[right] == 0:
                zero_count += 1

            # If our window is invalid (it has more than one zero),
            # we must shrink it from the left until it's valid again.
            while zero_count > 1:
                # If the element leaving the window is a zero...
                if nums[left] == 0:
                    # ...decrement the zero count.
                    zero_count -= 1
                # Move the left pointer to the right to shrink the window.
                left += 1

            # Update the max_window_len with the size of the current valid window.
            max_window_len = max(max_window_len, right - left + 1)

        # The result is the longest window with at most one zero, minus the one
        # element that needs to be deleted.
        return max_window_len - 1


# @lc code=end
