#
# @lc app=leetcode id=119 lang=python3
#
# [119] Pascal's Triangle II
#


# @lc code=start
class Solution:
    def getRow(self, rowIndex: int) -> List[int]:

        # Initialize the row with the first element.
        # This represents row 0.
        row = [1]

        # We need to evolve this row 'rowIndex' times.
        for _ in range(rowIndex):
            # Step 1: Add a 1 to the end. This increases the size of the row
            # to prepare for the next level.
            # e.g., [1] -> [1, 1]
            row.append(1)

            # Step 2: Update the middle elements in-place.
            # Iterate backwards from the second-to-last element down to index 1.
            # We iterate backwards so we don't overwrite the values we need
            # for the next calculation step.
            for j in range(len(row) - 2, 0, -1):
                row[j] = row[j] + row[j - 1]

        return row


# @lc code=end
