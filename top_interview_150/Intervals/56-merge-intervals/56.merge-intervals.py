#
# @lc app=leetcode id=56 lang=python3
#
# [56] Merge Intervals
#


# @lc code=start
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:

        # Handle edge cases for empty or single-item lists.
        if not intervals:
            return []

        # Step 1: Sort the intervals based on their start time (the first element).
        intervals.sort(key=lambda x: x[0])

        # Step 2: Initialize the 'merged' list with the first interval.
        merged = [intervals[0]]

        # Step 3: Iterate through the rest of the sorted intervals.
        for i in range(1, len(intervals)):
            current_interval = intervals[i]
            # Get the last interval that was added to our result.
            last_merged_interval = merged[-1]

            # Step 4: Check for overlap.
            # Does the current interval start before or at the same time the last one ends?
            if current_interval[0] <= last_merged_interval[1]:
                # If yes, there is an overlap. Merge them.
                # The new end of the last interval is the maximum of the two ends.
                last_merged_interval[1] = max(
                    last_merged_interval[1], current_interval[1]
                )
            else:
                # If no, there is no overlap. Add the current interval as a new one.
                merged.append(current_interval)

        return merged


# @lc code=end
