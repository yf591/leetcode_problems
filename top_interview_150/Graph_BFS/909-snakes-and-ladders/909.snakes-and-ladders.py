#
# @lc app=leetcode id=909 lang=python3
#
# [909] Snakes and Ladders
#

import collections
from typing import List


# @lc code=start
class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)

        # Helper function to convert a square number to its (row, col) coordinate.
        def get_coords(square):
            # Adjust for 0-based indexing used in arrays.
            s_minus_1 = square - 1

            # Row is determined from the bottom up.
            row_from_bottom = s_minus_1 // n
            row = (n - 1) - row_from_bottom

            # Colmun depend on the direction of the row.
            if row_from_bottom % 2 == 0:  # Even rows (from bottom) go left-to-right
                col = s_minus_1 % n
            else:  # Odd rows (from bottom) go right-left
                col = (n - 1) - (s_minus_1 % n)

            return row, col

        # BFS setup
        queue = collections.deque([(1, 0)])  # (current_square, number_of_moves)
        visited = {1}

        while queue:
            square, moves = queue.popleft()

            # Simulate a dice roll from 1 to 6
            for i in range(1, 7):
                next_square = square + i

                # If we go past the last square, we can stop checking this roll
                if next_square > n * n:
                    break

                # Find the actual destination after a potential snake or ladder.
                r, c = get_coords(next_square)
                if board[r][c] != -1:
                    destination = board[r][c]
                else:
                    destination = next_square

                # If we have reached the goal, return the number of moves.
                if destination == n * n:
                    return moves + 1

                # If we have not visited this destination before, add it to the queue.
                if destination not in visited:
                    visited.add(destination)
                    queue.append((destination, moves + 1))

        # If the queue becomes empty and we never reached the end, it's impossible.
        return -1


# @lc code=end
