#
# @lc app=leetcode id=57 lang=python3
#
# [57] Insert Interval
#


# @lc code=start
class Solution:
    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:

        result = []
        i = 0
        n = len(intervals)

        # --- Phase 1: Add all intervals that end before the new one starts ---
        # These are guaranteed not to overlap.
        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        # --- Phase 2: Merge all overlapping intervals ---
        # This loop continues as long as the current interval starts before or
        # at the same time the newInterval ends.
        while i < n and intervals[i][0] <= newInterval[1]:
            # Merge by updating the newInterval to be the union of both.
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1

        # After the merging is done, add the final merged interval to the result.
        result.append(newInterval)

        # --- Phase 3: Add all remaining intervals that start after the new one ends ---
        while i < n:
            result.append(intervals[i])
            i += 1

        return result


# @lc code=end
