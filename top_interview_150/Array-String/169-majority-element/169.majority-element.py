#
# @lc app=leetcode id=169 lang=python3
#
# [169] Majority Element
#


# @lc code=start
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        # First, sort the array
        nums.sort()

        # The majority element is guaranteed to be at the middle index
        # because it appears more than n/2 times.
        middle_index = len(nums) // 2

        return nums[middle_index]


# @lc code=end
