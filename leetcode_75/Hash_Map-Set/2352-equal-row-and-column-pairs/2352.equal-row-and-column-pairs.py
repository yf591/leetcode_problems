#
# @lc app=leetcode id=2352 lang=python3
#
# [2352] Equal Row and Column Pairs
#


# @lc code=start
class Solution:
    def equalPairs(self, grid: List[List[int]]) -> int:

        n = len(grid)
        pair_count = 0

        # Step 1: Create a frequency map of all the row patterns.
        # We convert each row (which is a list) into a tuple so it can be
        # used as a key in the Counter (hash map).
        row_counts = collections.Counter(tuple(row) for row in grid)

        # Step 2: Iterate through each column of the grid.
        for c in range(n):
            # Step 2a: Construct the current column as a tuple.
            current_col = []
            for r in range(n):
                current_col.append(grid[r][c])
            current_col = tuple(current_col)

            # Step 2b: Check if this column pattern exists in our row map.
            if current_col in row_counts:
                # If it does, add the number of matching rows to our total count.
                pair_count += row_counts[current_col]

        return pair_count


# @lc code=end
