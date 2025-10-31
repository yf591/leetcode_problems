#
# @lc app=leetcode id=62 lang=python3
#
# [62] Unique Paths
#


# @lc code=start
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:

        # We can use a 1D DP array (representing a row) of size n.
        # Initialize it with all 1s. This represents the top row (row 0),
        # as there is exactly 1 way to reach any cell in the first row.
        row = [1] * n

        # We have m rows. We already calculated the first row (our init).
        # So, we loop m - 1 more times to calculate the remaining rows.
        for i in range(m - 1):

            # For each new row, we update the values in our 1D array.
            # We skip the first column (j=0) because the number of paths
            # to any cell in the first column is always 1, and our
            # array already has a 1 in that position.
            for j in range(1, n):
                # The value for the new row at j is:
                # row[j] (the value from the cell above it, from the previous row)
                # +
                # row[j-1] (the value from the cell to its left, from the new row)
                row[j] = row[j] + row[j - 1]

        # After all rows are computed, the final answer is the value
        # in the last cell (bottom-right corner).
        return row[n - 1]


# @lc code=end
