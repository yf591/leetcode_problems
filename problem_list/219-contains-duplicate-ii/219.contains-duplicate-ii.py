#
# @lc app=leetcode id=219 lang=python3
#
# [219] Contains Duplicate II
#


# @lc code=start
class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        # Use a hash map to store the most recent index of each number.
        # Format: {number: index}
        seen_map = {}

        # Enumerate gives us both the index 'i' and the value 'num'.
        for i, num in enumerate(nums):
            # Check if we've seen this number before AND if it's close enough.
            if num in seen_map and i - seen_map[num] <= k:
                # If both conditions are true, we've found our pair.
                return True

            # If not, update the map with the current number's most recent index.
            seen_map[num] = i

        # If the loop completes, no pair was found.
        return False


# @lc code=end
