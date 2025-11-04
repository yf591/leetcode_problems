#
# @lc app=leetcode id=1143 lang=python3
#
# [1143] Longest Common Subsequence
#


# @lc code=start
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:

        m, n = len(text1), len(text2)

        # Create a DP table (grid) of size (m+1) x (n+1) initialized with 0s.
        # dp[i][j] will store the LCS of text1[:i] and text2[:j]
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Iterate through the grid, starting from 1 (0 row/col are base cases)
        for i in range(1, m + 1):
            for j in range(1, n + 1):

                # Compare the characters at the corresponding positions in the strings
                # Note: We use i-1 and j-1 because strings are 0-indexed,
                # but our DP table is (m+1)x(n+1)

                # Case 1: The characters match
                if text1[i - 1] == text2[j - 1]:
                    # The LCS length is 1 + the LCS of the strings before this char
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    # Case 2: The characters do not match
                    # The LCS is the best we can get by either
                    # excluding the char from text1 or excluding the char from text2.
                    dp[i][j] = max(
                        dp[i - 1][j], dp[i][j - 1]  # (excluding char from text1)
                    )  # (excluding char from text2)

        # The final answer is in the bottom-right corner, representing
        # the LCS of the entire text1 and text2.
        return dp[m][n]


# @lc code=end
