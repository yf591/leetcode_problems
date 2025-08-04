#
# @lc app=leetcode id=27 lang=python3
#
# [27] Remove Element
#


# @lc code=start
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        # 'k' will be the index where the next element that is NOT equal to val
        # should be placed. It also serves as a counter for the valid elements.
        k = 0

        # Iterate through the entire array using index 'i'.
        for i in range(len(nums)):
            # If the current element is not the value we want to remove...
            if nums[i] != val:
                # ...then it's a 'valid' element. We move it to the k-th position.
                # This efficiently overwrites any 'val' elements that were there.
                nums[k] = nums[i]
                # Increment k to mark the next position for a valid element.
                k += 1

        # After the loop, the first 'k' element of nums are the ones we want to keep.
        # and 'k' is the count of these elements.
        return k


# @lc code=end
