#
# @lc app=leetcode id=1679 lang=python3
#
# [1679] Max Number of K-Sum Pairs
#


# @lc code=start
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:

        # Use a Counter to get the frequency of each number in O(n) time.
        counts = collections.Counter(nums)
        operations = 0

        # Iterate through each unique number 'num' and its count.
        for num, num_count in counts.items():
            # Calculate the complement we are looking for.
            complement = k - num

            if num == complement:
                # If the number is its own complement (e.g., num=3, k=6),
                # we can form pairs of this number. Each pair uses two.
                operations += num_count // 2
            elif num < complement and complement in counts:
                # If the number is smaller than its complement, we find how many
                # pairs of (num, complement) we can form. This is limited by
                # the smaller of the two counts.
                complement_count = counts[complement]
                pairs = min(num_count, complement_count)
                operations += pairs

        return operations


# @lc code=end
