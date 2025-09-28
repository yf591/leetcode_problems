#
# @lc app=leetcode id=289 lang=python3
#
# [289] Game of Life
#


# @lc code=start
class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """

        rows, cols = len(board), len(board[0])

        # Directions to check the 8 neighbors of a cell
        neighbors = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        # --- Pass 1: Mark cells that will change state ---
        # We'll use two new states:
        # - 2: Represents a cell that was live (1) but will die (0).
        # - 3: Represents a cell that was dead (0) but will become live (1).

        for r in range(rows):
            for c in range(cols):
                live_neighbors = 0
                # Count live neighbors in the original state
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and (board[nr][nc] == 1 or board[nr][nc] == 2)
                    ):
                        live_neighbors += 1

                # Apply Game of Life rules based on the original state
                # Rule 1 & 3: A live cell dies
                if board[r][c] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                    board[r][c] = 2  # Mark as "will die"

                # Rule 4: A dead cell becomes live
                elif board[r][c] == 0 and live_neighbors == 3:
                    board[r][c] = 3  # Mark as "will become live"

        # --- Pass 2: Finalize the board state ---
        # Convert the temporary states back to 0s and 1s.
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 2:
                    board[r][c] = 0
                elif board[r][c] == 3:
                    board[r][c] = 1


# @lc code=end
