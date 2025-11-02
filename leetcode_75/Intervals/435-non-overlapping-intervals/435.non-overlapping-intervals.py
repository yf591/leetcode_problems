#
# @lc app=leetcode id=435 lang=python3
#
# [435] Non-overlapping Intervals
#


# @lc code=start
class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:

        # If there are no intervals, we remove 0.
        if not intervals:
            return 0

        # Step 1: Sort the intervals by their end time.
        # This is the key greedy choice.
        intervals.sort(key=lambda x: x[1])

        # Step 2: Initialize variables.
        # We automatically "keep" the first interval, which finishes earliest.
        intervals_kept = 1
        last_end_time = intervals[0][1]

        # Step 3: Iterate from the *second* interval onwards.
        for i in range(1, len(intervals)):
            current_start = intervals[i][0]

            # Step 4: Check for non-overlap.
            # If the current interval starts after or at the same time
            # the last kept interval ended, they don't overlap.
            if current_start >= last_end_time:
                # We can keep this interval.
                intervals_kept += 1
                # Update the "last end time" to this interval's end.
                last_end_time = intervals[i][1]

            # If they do overlap (current_start < last_end_time),
            # we do nothing. We are "removing" the current interval
            # by not counting it in intervals_kept.

        # Step 5: The result is the total count minus the ones we kept.
        return len(intervals) - intervals_kept


# @lc code=end
