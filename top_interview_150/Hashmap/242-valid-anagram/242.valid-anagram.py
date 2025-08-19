#
# @lc app=leetcode id=242 lang=python3
#
# [242] Valid Anagram
#


# @lc code=start
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # If the strings have different lengths, they cannot be anagrams.
        if len(s) != len(t):
            return False

        # collections.Counter is a specialized dictionary (hash map)
        # that is perfect for counting character frequencies.
        # It will create a map like {'a': 3, 'n': 1, ...} for "anagram".
        s_counts = collections.Counter(s)
        t_counts = collections.Counter(t)

        # If the two frequency maps are identical, the strings are anagrams.
        return s_counts == t_counts


# @lc code=end
