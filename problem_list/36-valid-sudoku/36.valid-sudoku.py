from typing import List
import collections

#
# @lc app=leetcode id=36 lang=python3
#
# [36] Valid Sudoku
#


# @lc code=start
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # Use defaultdicts to store sets of seen numbers for each row, col, box.
        rows = collections.defaultdict(set)
        cols = collections.defaultdict(set)
        boxes = collections.defaultdict(set)

        # Iterate through every cell on the 9x9 board.
        for r in range(9):
            for c in range(9):
                val = board[r][c]

                # If the cell is empty, skip it.
                if val == ".":
                    continue

                # --- Check for rule violations ---

                # 1. Check if the number is already in the current row.
                if val in rows[r]:
                    return False

                # 2. Check if the number is already in the current column.
                if val in cols[c]:
                    return False

                # 3. Check if the number is already in the current 3x3 box.
                box_key = (r // 3, c // 3)
                if val in boxes[box_key]:
                    return False

                # --- If no violations, add the number to our records ---
                rows[r].add(val)
                cols[c].add(val)
                boxes[box_key].add(val)

        # If we get through the entire board without returning False, it's valid
        return True


# @lc code=end
