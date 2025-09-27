#
# @lc app=leetcode id=73 lang=python3
#
# [73] Set Matrix Zeroes
#


# @lc code=start
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """

        rows, cols = len(matrix), len(matrix[0])
        first_col_has_zero = False

        # Step 1: Use the first row and column as markers.
        # Check if the first column needs to be zeroed out.
        for r in range(rows):
            if matrix[r][0] == 0:
                first_col_has_zero = True
                break

        # Check if the first row needs to be zeroed out.
        # We can use matrix[0][0] for this, but a flag is cleaner.
        first_row_has_zero = False
        for c in range(cols):
            if matrix[0][c] == 0:
                first_row_has_zero = True
                break

        # Step 2: Iterate through the rest of the matrix to mark the first row/col.
        for r in range(1, rows):
            for c in range(1, cols):
                if matrix[r][c] == 0:
                    matrix[0][c] = 0
                    matrix[r][0] = 0

        # Step 3: Zero out cells based on the markers.
        for r in range(1, rows):
            for c in range(1, cols):
                if matrix[r][0] == 0 or matrix[0][c] == 0:
                    matrix[r][c] = 0

        # Step 4: Zero out the first row and column if they originally had a zero.
        if first_row_has_zero:
            for c in range(cols):
                matrix[0][c] = 0

        if first_col_has_zero:
            for r in range(rows):
                matrix[r][0] = 0


# @lc code=end
