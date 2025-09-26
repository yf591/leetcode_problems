#
# @lc app=leetcode id=3 lang=python3
#
# [3] Longest Substring Without Repeating Characters
#


# @lc code=start
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:

        # This set will store the characters in the current window.
        char_set = set()
        # 'left' is the starting pointer of our window.
        left = 0
        # 'max_length' will store our final answer.
        max_length = 0

        # 'right' is the ending pointer of our window, which expands as we loop.
        for right in range(len(s)):
            # --- Shrink the Window ---
            # If the new character s[right] is already in our set, it's a duplicate.
            # We must shrink the window from the left until the duplicate is removed.
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1

            # --- Expand the Window ---
            # Add the new character to our set. Now the window is valid again.
            char_set.add(s[right])

            # --- Update the Result ---
            # The length of the current valid window is (right - left + 1).
            # Update our max_length if this window is the new longest.
            max_length = max(max_length, right - left + 1)

        return max_length


# @lc code=end
