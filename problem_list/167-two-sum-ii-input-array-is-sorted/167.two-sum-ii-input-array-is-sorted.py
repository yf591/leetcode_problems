#
# @lc app=leetcode id=167 lang=python3
#
# [167] Two Sum II - Input Array Is Sorted
#


# @lc code=start
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:

        left, right = 0, len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]

            if current_sum == target:
                # Found the solution, return 1-indexed indices
                return [left + 1, right + 1]
            elif current_sum < target:
                # Sum is too small, need a bigger number
                left += 1
            else:  # current_sum > target
                # Sum is too big, need a smaller number
                right -= 1


# @lc code=end
