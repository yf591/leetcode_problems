#
# @lc app=leetcode id=33 lang=python3
#
# [33] Search in Rotated Sorted Array
#


# @lc code=start
class Solution:
    def search(self, nums: List[int], target: int) -> int:

        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            # Case 1: We found the target immediately
            if nums[mid] == target:
                return mid

            # Determine which side is sorted
            if nums[left] <= nums[mid]:
                # Left side is sorted.
                # Check if the target is within this sorted range.
                if nums[left] <= target < nums[mid]:
                    right = mid - 1  # Target is in the left half
                else:
                    left = mid + 1  # Target is in the right half
            else:
                # Right side is sorted.
                # Check if the target is within this sorted range.
                if nums[mid] < target <= nums[right]:
                    left = mid + 1  # Target is in the right half
                else:
                    right = mid - 1  # Target is in the left half

        return -1


# @lc code=end
