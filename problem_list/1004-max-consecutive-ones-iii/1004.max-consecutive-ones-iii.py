#
# @lc app=leetcode id=1004 lang=python3
#
# [1004] Max Consecutive Ones III
#


# @lc code=start
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:

        left = 0
        max_length = 0
        zero_count = 0

        # 'right' pointer expands the window by iterating through the array.
        for right in range(len(nums)):
            # If the new element entering the window is a zero, increment our count.
            if nums[right] == 0:
                zero_count += 1

            # If our window is invalid (too many zeros), we must shrink it.
            while zero_count > k:
                # If the element leaving the window from the left is a zero...
                if nums[left] == 0:
                    # ...decrement the zero count.
                    zero_count -= 1
                # Move the left pointer to the right to shrink the window.
                left += 1

            # After ensuring the window is valid, update the max_length.
            # The current valid window's length is (right - left + 1).
            max_length = max(max_length, right - left + 1)

        return max_length


# @lc code=end
