#
# @lc app=leetcode id=128 lang=python3
#
# [128] Longest Consecutive Sequence
#


# @lc code=start
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:

        # Convert the list to a set for fast O(1) lookups and to handle duplicates.
        num_set = set(nums)
        max_length = 0

        # Iterate through each unique number in the original list.
        for num in num_set:
            # The key optimization: only start counting if 'num' is the
            # beginning of a sequence (i.e., num - 1 is not in the set).
            if (num - 1) not in num_set:
                current_num = num
                current_length = 1

                # Count the length of the sequence starting from 'num'.
                while current_num + 1 in num_set:
                    current_num += 1
                    current_length += 1

                # Update the maximum length found so far.
                max_length = max(max_length, current_length)

        return max_length


# @lc code=end
