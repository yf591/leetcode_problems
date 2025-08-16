#
# @lc app=leetcode id=200 lang=python3
#
# [200] Number of Islands
#


# @lc code=start
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # Handle the edge case of an empty grid.
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        island_count = 0

        def dfs(r, c):
            """
            This is our Depth-First Search helper function.
            It "sinks" an island by turning all its '1's into '0's.
            """
            # Base cases to stop the recursion
            # 1. If we go out of the grid's bounds.
            # 2. If the current cell is already water ('0')
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == "0":
                return

            # 'Sink' the current piece of the land by changing it to '0'
            # This also marks it as visited.
            grid[r][c] = "0"

            # Recursively call dfs on all 4 adjacent neighbors.
            dfs(r + 1, c)  # Down
            dfs(r - 1, c)  # Up
            dfs(r, c + 1)  # Right
            dfs(r, c - 1)  # Left

        # --- Main Logic ---
        # Iterate through each cell of the grid.
        for r in range(rows):
            for c in range(cols):
                # If we find a '1' it's the start of a new, unvisited island.
                if grid[r][c] == "1":
                    island_count += 1
                    # Start the DFS traversal to find and sink the entire island.
                    dfs(r, c)

        return island_count


# @lc code=end
