#
# @lc app=leetcode id=283 lang=python3
#
# [283] Move Zeroes
#


# @lc code=start
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """

        # The 'write_ptr' keeps track of the position where the next
        # non-zero element should be placed.
        write_ptr = 0

        # The 'read_ptr' scans through the entire array.
        for read_ptr in range(len(nums)):
            # If the element at the 'read_ptr' is not zero...
            if nums[read_ptr] != 0:
                # ...swap it with the element at the 'write_ptr' position.
                nums[write_ptr], nums[read_ptr] = nums[read_ptr], nums[write_ptr]

                # Advance the 'write_ptr' to the next available slot.
                write_ptr += 1


# @lc code=end
