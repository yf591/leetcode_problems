#
# @lc app=leetcode id=746 lang=python3
#
# [746] Min Cost Climbing Stairs
#


# @lc code=start
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:

        # Get the number of steps.
        n = len(cost)

        # Iterate from the third step (index 2) to the end of the array.
        # The costs for the first two steps (0 and 1) are just their own values,
        # as you can start on either one.
        for i in range(2, n):
            # The minimum cost to reach the current step 'i' is its own cost
            # plus the minimum of the costs to reach the previous two steps.
            cost[i] += min(cost[i - 1], cost[i - 2])

        # The final destination is one step past the end. You can get there
        # from either the last step (cost[n-1]) or the second-to-last step (cost[n-2]).
        # The minimum of these two is the answer.
        return min(cost[n - 1], cost[n - 2])


# @lc code=end
