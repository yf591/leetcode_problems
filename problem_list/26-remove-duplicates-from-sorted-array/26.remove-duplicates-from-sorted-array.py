#
# @lc app=leetcode id=26 lang=python3
#
# [26] Remove Duplicates from Sorted Array
#


# @lc code=start
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # If the list is empty, there are no unique elements.
        if not nums:
            return 0

        # 'k' is the index whwere the next unique element should be placed.
        # The first element is always unique, so we start k at 1.
        k = 1

        # Itarete through the list starting from the second element.
        for i in range(1, len(nums)):
            # If the current element is different from the previous one,
            # it is a unique element.
            if nums[i] != nums[i - 1]:
                # Place the unique element at the position k.
                nums[k] = nums[i]
                # Move the "unique element" pointer forward.
                k += 1

        # k now holds the count of inique elements.
        return k


# @lc code=end
