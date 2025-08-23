#
# @lc app=leetcode id=189 lang=python3
#
# [189] Rotate Array
#


# @lc code=start
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        # Handle k > n
        k %= n

        def reverse(start: int, end: int):
            """Helper function to reverse a portion of the array."""
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1

        # Step 1: Reverse the entire array.
        # [1,2,3,4,5,6,7] -> [7,6,5,4,3,2,1]
        reverse(0, n - 1)

        # Step 2: Reverse the first k elements.
        # [7,6,5, 4,3,2,1] -> [5,6,7, 4,3,2,1]
        reverse(0, k - 1)

        # Step 3: Reverse the remaining n-k elements.
        # [5,6,7, 4,3,2,1] -> [5,6,7, 1,2,3,4]
        reverse(k, n - 1)


# @lc code=end
