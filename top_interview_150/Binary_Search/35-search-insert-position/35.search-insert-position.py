#
# @lc app=leetcode id=35 lang=python3
#
# [35] Search Insert Position
#


# @lc code=start
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        # Initialize pointers for the start and end of the search range.
        low, high = 0, len(nums) - 1

        # Perform binary search.
        while low <= high:
            # Find the middle index to avoid potential overflow.
            mid = low + (high - low) // 2

            # If the middle element is the target, we've found it.
            if nums[mid] == target:
                return mid

            # If the target is greater, discard the left half.
            elif nums[mid] < target:
                low = mid + 1

            # If the target is smaller, discard the right half.
            else:
                high = mid - 1

        # If the loop finishes, the target was not found.
        # The 'low' pointer is now at the index where the target
        # would be inserted to maintain order.
        return low


# @lc code=end
