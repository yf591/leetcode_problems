#
# @lc app=leetcode id=74 lang=python3
#
# [74] Search a 2D Matrix
#


# @lc code=start
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:

        if not matrix:
            return False

        m = len(matrix)  # Number of rows
        n = len(matrix[0])  # Number of columns

        # Initialize binary search boundaries for the "virtual" 1D array.
        # Range is from 0 to total_elements - 1
        left = 0
        right = (m * n) - 1

        while left <= right:
            # Calculate the middle index in the virtual 1D array
            mid = (left + right) // 2

            # Convert the 1D mid index back to 2D matrix coordinates
            # Row is quotient, Column is remainder
            row = mid // n
            col = mid % n

            mid_val = matrix[row][col]

            if mid_val == target:
                return True
            elif mid_val < target:
                # Target is in the right half
                left = mid + 1
            else:
                # Target is in the left half
                right = mid - 1

        return False


# @lc code=end
