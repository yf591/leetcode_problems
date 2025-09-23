#
# @lc app=leetcode id=134 lang=python3
#
# [134] Gas Station
#


# @lc code=start
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:

        # Check if a solution is possible. If total gas is less than total cost,
        # it's impossible to complete the circuit.
        if sum(gas) < sum(cost):
            return -1

        # If a solution is possible, we can find it in one pass.
        total_tank = 0
        start_index = 0

        for i in range(len(gas)):
            # Track the tank level as we travel from the current start_index.
            total_tank += gas[i] - cost[i]

            # If the tank level drops below zero...
            if total_tank < 0:
                # ...it means we can't reach station 'i' from the current start_index.
                # The new potential start must be the station *after* this failure point.
                start_index = i + 1
                # Reset the tank for the new potential journey segment.
                total_tank = 0

        # Because we've already confirmed that a solution exists (from the sum check),
        # the 'start_index' we are left with at the end of the loop must be the one.
        return start_index


# @lc code=end
