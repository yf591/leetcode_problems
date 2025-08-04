#
# @lc app=leetcode id=228 lang=python3
#
# [228] Summary Ranges
#


# @lc code=start
class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        # Handle the edge case of an empty list.
        if not nums:
            return []

        ranges = []
        # The start of the our current range is the first number.
        start = nums[0]

        # iterate through the list to find the end of each range.
        for i in range(1, len(nums)):
            # Chack if the curent number is NOT consecutive with the previous number.
            # This means the range has just ended.
            if nums[i] != nums[i - 1] + 1:
                # Add the completed range to our list.
                if start == nums[i - 1]:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}->{nums[i-1]}")

                # Start a new range with the current number.
                start = nums[i]

        # After the loop, the very last range still needs to be added.
        if start == nums[-1]:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}->{nums[-1]}")

        return ranges


# @lc code=end
