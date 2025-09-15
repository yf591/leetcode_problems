#
# @lc app=leetcode id=1657 lang=python3
#
# [1657] Determine if Two Strings Are Close
#


# @lc code=start
class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:

        # Condition 0: If lengths are different, they can't be close.
        if len(word1) != len(word2):
            return False

        # Condition 1: They must contain the same unique characters.
        # set() creates a collection of unique items.
        if set(word1) != set(word2):
            return False

        # Condition 2: The collection of character counts must be the same.

        # Create frequency maps for both words.
        counts1 = collections.Counter(word1)
        counts2 = collections.Counter(word2)

        # .values() gets a list of the counts (e.g., [3, 2, 1]).
        # We sort these lists to compare them regardless of which character
        # had which count.
        return sorted(counts1.values()) == sorted(counts2.values())


# @lc code=end
