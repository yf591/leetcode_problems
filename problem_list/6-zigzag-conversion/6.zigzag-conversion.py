#
# @lc app=leetcode id=6 lang=python3
#
# [6] Zigzag Conversion
#


# @lc code=start
class Solution:
    def convert(self, s: str, numRows: int) -> str:

        # Edge case: If numRows is 1, the output is the same as the input.
        if numRows == 1:
            return s

        # Create a list of lists to hold the characters for each row.
        rows = [[] for _ in range(numRows)]

        current_row = 0
        # This will be 1 for moving down, -1 for moving up.
        direction = 1

        for char in s:
            # Add the character to the correct row.
            rows[current_row].append(char)

            # Check if we need to change direction (if we're at the top or bottom).
            if current_row == 0:
                direction = 1
            elif current_row == numRows - 1:
                direction = -1

            # Move to the next row.
            current_row += direction

        # Join all the characters back into a single string.
        # First, join the characters in each row's list.
        # Then, join all the row strings together.
        final_string = ""
        for row in rows:
            final_string += "".join(row)

        return final_string


# @lc code=end
