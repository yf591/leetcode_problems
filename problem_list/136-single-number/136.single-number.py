#
# @lc app=leetcode id=136 lang=python3
#
# [136] Single Number
#


# @lc code=start
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        # Initialize a variable to 0.
        # XORing with 0 doesn't change the number (x ^ 0 = x).
        result = 0

        # Iterate through all numbers in the list.
        for num in nums:
            # Apply the XOR operation between the running result and the current number.
            result ^= num

        # The final result will be the single, unique number.
        return result


# @lc code=end
