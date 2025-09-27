#
# @lc app=leetcode id=48 lang=python3
#
# [48] Rotate Image
#


# @lc code=start
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """

        n = len(matrix)

        # --- Step 1: Transpose the matrix ---
        # We iterate through the upper triangle of the matrix.
        for i in range(n):
            for j in range(i + 1, n):
                # Swap the element at (i, j) with the element at (j, i).
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        # --- Step 2: Reverse each row ---
        for i in range(n):
            # The list.reverse() method modifies the list in-place.
            matrix[i].reverse()


# @lc code=end
