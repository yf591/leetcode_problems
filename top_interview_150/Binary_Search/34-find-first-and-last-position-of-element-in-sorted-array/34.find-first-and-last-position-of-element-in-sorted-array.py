#
# @lc app=leetcode id=34 lang=python3
#
# [34] Find First and Last Position of Element in Sorted Array
#

from types import List


# @lc code=start
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:

        def findBound(isFirst: bool) -> int:
            left, right = 0, len(nums) - 1
            bound_idx = -1

            while left <= right:
                mid = (left + right) // 2

                if nums[mid] == target:
                    # Found the target! Store the index.
                    bound_idx = mid

                    # The crucial divergence:
                    if isFirst:
                        # If looking for the FIRST occurrence, narrow search to the LEFT half
                        right = mid - 1
                    else:
                        # If looking for the LAST occurrence, narrow search to the RIGHT half
                        left = mid + 1

                elif nums[mid] < target:
                    # Target is to the right
                    left = mid + 1
                else:
                    # Target is to the left
                    right = mid - 1

            return bound_idx

        # 1. Find the starting position
        start = findBound(True)

        # Optimization: If start is -1, the target doesn't exist.
        if start == -1:
            return [-1, -1]

        # 2. Find the ending position
        end = findBound(False)

        return [start, end]


# @lc code=end
