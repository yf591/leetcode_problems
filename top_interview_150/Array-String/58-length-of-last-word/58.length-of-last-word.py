#
# @lc app=leetcode id=58 lang=python3
#
# [58] Length of Last Word
#


# @lc code=start
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        # 1. Remove any leading or trailing whitespace from the string.
        # 2. Split the string by spaces to create a list of words.
        # 3. Return the last word from the list using the index [-1].
        # 4. Return the length of that last word.
        return len(s.strip().split()[-1])


# @lc code=end
