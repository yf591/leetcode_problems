#
# @lc app=leetcode id=11 lang=python3
#
# [11] Container With Most Water
#


# @lc code=start
class Solution:
    def maxArea(self, height: List[int]) -> int:

        # Initialize pointers at the start and end of the array.
        left = 0
        right = len(height) - 1

        # Variable to store the maximum area found so far.
        max_area = 0

        # Loop until the pointers meet.
        while left < right:
            # The height of the container is limited by the shorter of the two lines.
            current_height = min(height[left], height[right])
            # The width is the distance between the pointers.
            width = right - left

            # Calculate the area of the current container.
            current_area = current_height * width

            # Update the maximum area if the current one is larger.
            max_area = max(max_area, current_area)

            # --- The Greedy Move ---
            # Move the pointer of the shorter line inward to search for a
            # potentially taller line that could create a larger area.
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_area


# @lc code=end
