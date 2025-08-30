#
# @lc app=leetcode id=2215 lang=python3
#
# [2215] Find the Difference of Two Arrays
#


# @lc code=start
class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        # Step 1: Convert both lists to sets to get unique elements.
        set1 = set(nums1)
        set2 = set(nums2)

        # Step 2: Use the set difference operator (-) to find the elements
        # that are in one set but not the other.

        # Find elements that are in set1 but not in set2.
        diff1 = list(set1 - set2)

        # Find elements that are in set2 but not in set1.
        diff2 = list(set2 - set1)

        # Step 3: Return the two lists as the final answer.
        return [diff1, diff2]


# @lc code=end
