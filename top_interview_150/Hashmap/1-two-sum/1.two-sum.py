#
# @lc app=leetcode id=1 lang=python3
#
# [1] Two Sum
#


# @lc code=start

from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_map = {}
        for index, num in enumerate(nums):
            complement = target - num
            if complement in num_map:
                return [num_map[complement], index]
            num_map[num] = index

        return []


solver = Solution()
nums1 = [2, 7, 11, 15]
target1 = 9
result1 = solver.twoSum(nums1, target1)
print(result1)  # Expected output: [0, 1]

nums2 = [3, 2, 4]
target2 = 6
result2 = solver.twoSum(nums2, target2)
print(result2)  # Expected output: [1, 2]

nums3 = [3, 3]
target3 = 6
result3 = solver.twoSum(nums3, target3)
print(result3)  # Expected output: [0, 1]


# @lc code=end
