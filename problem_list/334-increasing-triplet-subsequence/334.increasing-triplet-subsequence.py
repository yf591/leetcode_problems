#
# @lc app=leetcode id=334 lang=python3
#
# [334] Increasing Triplet Subsequence
#


# @lc code=start
class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:

        # 'first' will hold the smallest number of a potential triplet.
        # 'second' will hold the second smallest number.
        # We initialize them to infinity.
        first = float("inf")
        second = float("inf")

        for num in nums:
            # If the current number is the smallest we've seen, it becomes our
            # new best candidate for the first element of the triplet.
            if num <= first:
                first = num
            # Else, if it's not smaller than 'first' but is smaller than 'second',
            # it becomes our new best candidate for the second element.
            elif num <= second:
                second = num
            # If the number is greater than both 'first' and 'second',
            # it means we have found our third element, completing the triplet.
            else:  # num > first and num > second
                return True

        # If we get through the entire loop without finding such a triplet,
        # it doesn't exist.
        return False


# @lc code=end
