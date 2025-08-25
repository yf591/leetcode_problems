#
# @lc app=leetcode id=45 lang=python3
#
# [45] Jump Game II
#


# @lc code=start
class Solution:
    def jump(self, nums: List[int]) -> int:
        # The number of jumps we've made.
        jumps = 0
        # The end of the range for the current jump.
        current_reach = 0
        # The farthest we can possibly reach from any position
        # within the current jump's range.
        farthest_reach = 0

        # We iterate through the array, stopping before the last element.
        # Once we can reach the last element, we don't need to jump from it.
        for i in range(len(nums) - 1):
            # Update the farthest reach possible from our current position.
            farthest_reach = max(farthest_reach, i + nums[i])

            # If our iterator 'i' has reached the end of the current jump's range...
            if i == current_reach:
                # ...it's time to take another jump.
                jumps += 1
                # The new jump's range extends to the farthest point we found.
                current_reach = farthest_reach

        return jumps


# @lc code=end
