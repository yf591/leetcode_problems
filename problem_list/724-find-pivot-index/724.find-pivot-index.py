#
# @lc app=leetcode id=724 lang=python3
#
# [724] Find Pivot Index
#


# @lc code=start
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        # Step 1: Calculate the total sum of all numbers in the array.
        total_sum = sum(nums)

        # Step 2: Initialize the sum of the numbers to the left of the pivot.
        left_sum = 0

        # Step 3: Iterate through the array to find the pivot.
        for i in range(len(nums)):
            # For the current index 'i', the right sum is the total sum minus
            # the left sum and the number at the current index.
            right_sum = total_sum - left_sum - nums[i]

            # Check if the two sums are equal.
            if left_sum == right_sum:
                # If they are, we've found the pivot index.
                return i

            # If not, update the left_sum by adding the current number
            # for the next iteration.
            left_sum += nums[i]

        # If the loop completes without finding a pivot, return -1.
        return -1


# @lc code=end
