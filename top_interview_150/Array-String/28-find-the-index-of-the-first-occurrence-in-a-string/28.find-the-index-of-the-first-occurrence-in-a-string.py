#
# @lc app=leetcode id=28 lang=python3
#
# [28] Find the Index of the First Occurrence in a String
#


# @lc code=start
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        """
        # python's bult-in 'find()' method is perfect for this.
        # It returns the index of the first occurence of the substring.
        # If the substring is not found, it returns -1, which matches
        # the problem's requirements.
        return haystack.find(needle)
        """

        if not needle:
            return 0

        for i in range(len(haystack) - len(needle) + 1):
            if haystack[i : i + len(needle)] == needle:
                return i

        return -1


# @lc code=end
