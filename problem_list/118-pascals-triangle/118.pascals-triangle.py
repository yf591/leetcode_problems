#
# @lc app=leetcode id=118 lang=python3
#
# [118] Pascal's Triangle
#


# @lc code=start
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        # If numRows is 0, return an empty list.
        if numRows == 0:
            return []

        # Start our triangle with the first row.
        triangle = [[1]]

        # Loop to generate the remaining rows. If numRows is 1, this loop won't run.
        for i in range(1, numRows):
            # Get the previous row, which is the last row currently in our triangle.
            prev_row = triangle[-1]

            # Every new row starts with a 1.
            new_row = [1]

            # Calculate the middle elements of the new row.
            # This loop goes through adjacent pairs of the previous row.
            for j in range(len(prev_row) - 1):
                # The new element is the sum of the two above it.
                new_row.append(prev_row[j] + prev_row[j + 1])

            # Every new row also ends with a 1.
            new_row.append(1)

            # Add the completed new row to our triangle.
            triangle.append(new_row)

        return triangle


# @lc code=end
