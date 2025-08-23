#
# @lc app=leetcode id=80 lang=python3
#
# [80] Remove Duplicates from Sorted Array II
#


# @lc code=start
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # 'k' is the "write" pointer. It represents the length of the
        # valid part of the array that we are building.
        k = 0

        # Iterate through each number 'num' in the input array.
        for num in nums:
            # We decide if we should keep 'num' and place it at index 'k'.
            # The condition to keep 'num' is:
            # 1. If 'k' is less than 2, meaning we are at the beginning of the
            #    array. The first two elements are always allowed.
            # OR
            # 2. If the current 'num' is greater than the element at k-2.
            #    This cleverly checks if the current number is a new number,
            #    preventing a third duplicate from being added.
            if k < 2 or num > nums[k - 2]:
                nums[k] = num
                k += 1

        # After the loop, 'k' is the new length of the array.
        return k


# @lc code=end
