#
# @lc app=leetcode id=994 lang=python3
#
# [994] Rotting Oranges
#


# @lc code=start
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        queue = collections.deque()
        fresh_oranges_count = 0
        minutes_elapsed = 0

        # --- Step 1: Initialize Queue and Count Fresh Oranges ---
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    # Add initially rotten oranges to queue with time 0
                    queue.append((r, c, 0))
                elif grid[r][c] == 1:
                    # Count fresh oranges
                    fresh_oranges_count += 1

        # Directions for neighbors: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # --- Step 2: Perform BFS ---
        while queue:
            r, c, time = queue.popleft()

            # Update the maximum time elapsed so far
            minutes_elapsed = max(minutes_elapsed, time)

            # Explore neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # Check if neighbor is valid and fresh
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    # Rot the fresh orange
                    grid[nr][nc] = 2
                    # Decrement the count of fresh oranges
                    fresh_oranges_count -= 1
                    # Add the newly rotten orange to the queue for the next minute
                    queue.append((nr, nc, time + 1))

        # --- Step 3: Check Result ---
        # If there are still fresh oranges left, return -1
        if fresh_oranges_count > 0:
            return -1
        else:
            # Otherwise, return the total time elapsed
            return minutes_elapsed


# @lc code=end
