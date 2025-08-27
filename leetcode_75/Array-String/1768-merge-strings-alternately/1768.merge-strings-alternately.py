#
# @lc app=leetcode id=1768 lang=python3
#
# [1768] Merge Strings Alternately
#


# @lc code=start
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        # A list to build our result string efficiently.
        result = []
        m, n = len(word1), len(word2)

        # We need to loop as many times as the length of the longer string.
        for i in range(max(m, n)):
            # If our index 'i' is still valid for word1, append its character.
            if i < m:
                result.append(word1[i])

            # If our index 'i' is still valid for word2, append its character.
            if i < n:
                result.append(word2[i])

        # Join all the characters in the list to form the final string.
        return "".join(result)


# @lc code=end
