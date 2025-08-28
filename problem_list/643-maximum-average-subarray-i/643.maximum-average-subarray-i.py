#
# @lc app=leetcode id=643 lang=python3
#
# [643] Maximum Average Subarray I
#


# @lc code=start
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        # Step 1: Calculate the sum of the first window of size 'k'.
        current_sum = sum(nums[:k])
        # This is the maximum sum we've seen so far.
        max_sum = current_sum

        # Step 2: Slide the window from the k-th element to the end of the array.
        for i in range(k, len(nums)):
            # To get the new sum, we add the new element (nums[i]) and
            # subtract the element that's leaving the window (nums[i - k]).
            current_sum += nums[i] - nums[i - k]

            # Update our maximum sum if the current window's sum is greater.
            max_sum = max(max_sum, current_sum)

        # Step 3: The maximum average is the maximum sum divided by k.
        return max_sum / k


# @lc code=end
