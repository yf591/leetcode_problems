#
# @lc app=leetcode id=130 lang=python3
#
# [130] Surrounded Regions
#


# @lc code=start
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """

        if not board:
            return

        rows, cols = len(board), len(board[0])

        def dfs(r, c):
            """
            A helper function to find all 'O's connected to a starting point
            and mark them as 'S' (Safe).
            """
            # Base case: Stop if out of bounds or if the cell is not an 'O'.
            if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != "O":
                return

            # Mark the current cell as Safe.
            board[r][c] = "S"

            # Recursively call on all 4 neighbors.
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # --- Pass 1: Mark all 'O's connected to the border as 'S' ---

        # Check the top and bottom borders.
        for c in range(cols):
            if board[0][c] == "O":
                dfs(0, c)
            if board[rows - 1][c] == "O":
                dfs(rows - 1, c)

        # Check the left and right borders.
        for r in range(rows):
            if board[r][0] == "O":
                dfs(r, 0)
            if board[r][cols - 1] == "O":
                dfs(r, cols - 1)

        # --- Pass 2: Flip the remaining 'O's to 'X's and 'S's back to 'O's ---

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == "O":
                    board[r][c] = "X"  # Capture surrounded regions.
                elif board[r][c] == "S":
                    board[r][c] = "O"  # Restore safe regions.


# @lc code=end
