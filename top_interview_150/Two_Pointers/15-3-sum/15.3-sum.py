#
# @lc app=leetcode id=15 lang=python3
#
# [15] 3Sum
#


# @lc code=start
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        result = []
        # Step 1: Sort the array. This is crucial for the two-pointer approach
        # and for handling duplicates.
        nums.sort()
        n = len(nums)

        # Step 2: Iterate through the array to fix the first element of the triplet.
        for i in range(n - 2):
            # Optimization: If the current number is positive, the sum of three
            # positive numbers can't be zero. Since the array is sorted,
            # we can stop early.
            if nums[i] > 0:
                break

            # Skip duplicate first elements to avoid duplicate triplets.
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Step 3: Use two pointers for the rest of the array.
            left, right = i + 1, n - 1
            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]

                if current_sum < 0:
                    left += 1
                elif current_sum > 0:
                    right -= 1
                else:  # Found a triplet
                    result.append([nums[i], nums[left], nums[right]])

                    # Move pointers and skip duplicates for the other two elements.
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1

        return result


# @lc code=end
