#
# @lc app=leetcode id=739 lang=python3
#
# [739] Daily Temperatures
#


# @lc code=start
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        # Initialize the answer array with all 0s (the default value)
        answer = [0] * n
        # This stack will store the indices of the days
        stack = []

        # Iterate through the array once, with both index and temperature
        for current_day, current_temp in enumerate(temperatures):

            # While the stack has items AND the current temp is warmer
            # than the temp of the day at the top of the stack...
            while stack and current_temp > temperatures[stack[-1]]:
                # ...we've found the answer for that day.
                prev_day_index = stack.pop()
                answer[prev_day_index] = current_day - prev_day_index

            # After resolving all possible days, add the current day to the stack
            # to wait for its own warmer day.
            stack.append(current_day)

        # Any indices left on the stack never found a warmer day,
        # but their 'answer' values are already 0, so we're done.
        return answer


# @lc code=end
