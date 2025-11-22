#
# @lc app=leetcode id=53 lang=python3
#
# [53] Maximum Subarray
#


# @lc code=start
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:

        # Initialize variables based on the first element.
        # max_sum tracks the highest sum found globally.
        max_sum = nums[0]

        # current_sum tracks the max sum of the subarray ending at the current index.
        current_sum = nums[0]

        # Iterate through the rest of the array starting from the second element.
        for i in range(1, len(nums)):
            # Logic: Should we start a new subarray at current number nums[i]?
            # Or should we extend the previous subarray (current_sum + nums[i])?
            # We choose whichever is larger.

            # If current_sum was negative, adding it to nums[i] makes the result smaller
            # than nums[i] itself. So, we would pick nums[i] (start fresh).
            current_sum = max(nums[i], current_sum + nums[i])

            # Update the global maximum if the new current_sum is higher.
            max_sum = max(max_sum, current_sum)

        return max_sum


# @lc code=end
