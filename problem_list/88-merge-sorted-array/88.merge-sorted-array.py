#
# @lc app=leetcode id=88 lang=python3
#
# [88] Merge Sorted Array
#


# @lc code=start
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        # Initialize pointers for the last valid element of nums1, nums2,
        # and for the position to write to in nums1.
        p1 = m - 1
        p2 = n - 1
        p_write = m + n - 1

        # Loop backwards as long as there are elements in both arrays to compare.
        while p1 >= 0 and p2 >= 0:
            # Compare the elements and place the larger one at the end of nums1.
            if nums1[p1] > nums2[p2]:
                nums1[p_write] = nums1[p1]
                p1 -= 1
            else:
                nums1[p_write] = nums2[p2]
                p2 -= 1

            # Move the write pointer to the left.
            p_write -= 1

        # If there are any remaining elements in nums2 (meaning they are smaller
        # than all the remaining elements in nums1), copy them over.
        # We don't need to handle remaining elements in nums1 because they are
        # already in their correct sorted position.
        while p2 >= 0:
            nums1[p_write] = nums2[p2]
            p2 -= 1
            p_write -= 1


# @lc code=end
