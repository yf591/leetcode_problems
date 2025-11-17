#
# @lc app=leetcode id=72 lang=python3
#
# [72] Edit Distance
#


# @lc code=start
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m = len(word1)
        n = len(word2)

        # Create a DP table (grid) of size (m+1) x (n+1)
        # dp[i][j] will store the min distance to convert
        # word1[0...i-1] to word2[0...j-1]
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # --- Initialize Base Cases ---

        # Base Case 1: Cost to convert an empty string to word2[0...j-1]
        # This requires 'j' insertions.
        for j in range(n + 1):
            dp[0][j] = j

        # Base Case 2: Cost to convert word1[0...i-1] to an empty string
        # This requires 'i' deletions.
        for i in range(m + 1):
            dp[i][0] = i

        # --- Fill the DP table using the recurrence relation ---
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Note: We use i-1 and j-1 for 0-indexed strings
                if word1[i - 1] == word2[j - 1]:
                    # Case 1: Characters match. No operation needed.
                    # Cost is the same as the subproblem without these characters.
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # Case 2: Characters don't match.
                    # We must perform an operation. Find the minimum of the 3 choices.
                    insert_cost = dp[i][j - 1]
                    delete_cost = dp[i - 1][j]
                    replace_cost = dp[i - 1][j - 1]

                    dp[i][j] = 1 + min(insert_cost, delete_cost, replace_cost)

        # The final answer is in the bottom-right corner, representing
        # the cost to convert all of word1 to all of word2.
        return dp[m][n]


# @lc code=end
