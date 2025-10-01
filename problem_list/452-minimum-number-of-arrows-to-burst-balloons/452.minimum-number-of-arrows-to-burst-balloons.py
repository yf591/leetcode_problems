#
# @lc app=leetcode id=452 lang=python3
#
# [452] Minimum Number of Arrows to Burst Balloons
#


# @lc code=start
class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:

        # Handle the edge case of no balloons.
        if not points:
            return 0

        # Step 1: Sort the balloons based on their end points (p[1]).
        points.sort(key=lambda p: p[1])

        # Step 2: Initialize. We need at least one arrow for the first balloon.
        arrow_count = 1
        # The position of our first arrow is at the end of the first balloon.
        arrow_pos = points[0][1]

        # Step 3: Iterate through the rest of the balloons.
        for balloon in points:
            # Check if the current balloon can be burst by the last arrow we shot.
            # A new arrow is needed only if the balloon starts AFTER
            # where the last arrow was shot.
            if balloon[0] > arrow_pos:
                # If we need a new arrow, increment our count.
                arrow_count += 1
                # Update the arrow position to the end of the current balloon.
                arrow_pos = balloon[1]

        return arrow_count


# @lc code=end
