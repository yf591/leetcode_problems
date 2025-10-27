#
# @lc app=leetcode id=1926 lang=python3
#
# [1926] Nearest Exit from Entrance in Maze
#


# @lc code=start
class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:

        rows, cols = len(maze), len(maze[0])
        start_row, start_col = entrance[0], entrance[1]

        # Queue stores tuples: (row, col, steps)
        queue = collections.deque([(start_row, start_col, 0)])
        # Visited set stores tuples: (row, col)
        visited = {(start_row, start_col)}

        # Directions for neighbors: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            r, c, steps = queue.popleft()

            # Explore neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # Check if the neighbor is valid
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and maze[nr][nc] == "."
                    and (nr, nc) not in visited
                ):

                    # Check if this valid neighbor is an exit
                    # Must be on the border AND not the entrance itself
                    is_border = nr == 0 or nr == rows - 1 or nc == 0 or nc == cols - 1
                    is_entrance = (
                        nr == start_row and nc == start_col
                    )  # Already checked by visited, but good for clarity

                    # We found the nearest exit!
                    if (
                        is_border
                    ):  # No need to check is_entrance because visited handles it
                        return steps + 1

                    # If it's not an exit, mark visited and add to queue
                    visited.add((nr, nc))
                    queue.append((nr, nc, steps + 1))

        # If the queue becomes empty and no exit was found
        return -1


# @lc code=end
