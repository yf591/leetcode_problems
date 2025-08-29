#
# @lc app=leetcode id=1732 lang=python3
#
# [1732] Find the Highest Altitude
#


# @lc code=start
class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        # Start at altitude 0. This is also the highest point seen so far.
        current_altitude = 0
        max_altitude = 0

        # Go through each step of the trip.
        for altitude_gain in gain:
            # Calculate the new altitude after the current step.
            current_altitude += altitude_gain

            # Update the maximum altitude if the current one is higher.
            max_altitude = max(max_altitude, current_altitude)

        return max_altitude


# @lc code=end
