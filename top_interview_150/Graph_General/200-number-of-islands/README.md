# 200\. Number of Islands - Solution Explanation

## Problem Overview

Given a 2D grid of `'1'`s (land) and `'0'`s (water), count the number of distinct islands.

**Island Definition:**
An island is a group of `'1'`s that are connected to each other either horizontally or vertically. The grid is surrounded by water.

**Examples:**

```
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1 (All '1's are connected)

Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3 (There are three distinct groups of connected '1's)
```

## Key Insights

### Graph Traversal on a Grid

The key insight is to treat the grid as a graph. Each `'1'` is a node, and an edge exists between adjacent `'1'`s. The problem then becomes: **"Count the number of connected components in the graph."**

### "Sinking" the Island (Marking as Visited)

To count the components, we can iterate through the grid. When we find a piece of land (`'1'`), we know we've found an island. We then need to explore and find *all* parts of that same island. To avoid counting it again, we can change all its `'1'`s to `'0'`s. This is like "sinking" the island after we've counted it.

## Solution Approach

The strategy is to iterate through the grid, and each time we find a `'1'`, we increment our island count and then use a traversal algorithm like Depth-First Search (DFS) to find and sink the entire island.

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        island_count = 0

        def dfs(r, c):
            # Base case to stop recursion: if out of bounds or on water
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == '0':
                return

            # "Sink" the current land cell to mark it as visited
            grid[r][c] = '0'

            # Visit all 4 neighbors recursively
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # Main loop to scan the grid
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    island_count += 1
                    dfs(r, c)
        
        return island_count
```

**Strategy:**

1.  **Initialize**: Set `island_count` to 0.
2.  **Scan**: Loop through every cell `(r, c)` of the grid.
3.  **Find**: If a cell `grid[r][c]` is a `'1'`, we've found a new island.
4.  **Count & Sink**: Increment `island_count` and call a helper function (`dfs`) to recursively find and "sink" all connected parts of this island by changing their `'1'`s to `'0'`s.
5.  **Return**: After scanning the whole grid, return `island_count`.

## Detailed Code Analysis

### `numIslands` Function

```python
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == '1':
            island_count += 1
            dfs(r, c)
```

  - The nested loops ensure we visit every cell.
  - The `if grid[r][c] == '1':` condition is the trigger. It only acts on land cells that have not already been "sunk" by a previous `dfs` call. This ensures we only count each island once.

### `dfs(r, c)` Helper Function

```python
if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == '0':
    return
```

  - This is the **base case** for the recursion. It stops the exploration if the search goes out of the grid's boundaries or hits a water cell.

<!-- end list -->

```python
grid[r][c] = '0'
```

  - This is the critical "sinking" or "marking" step. By immediately changing the `'1'` to a `'0'`, we ensure that we don't visit this cell again in an infinite loop.

<!-- end list -->

```python
dfs(r + 1, c) # and other 3 directions
```

  - These are the **recursive steps**. The function calls itself on its four neighbors, propagating the search throughout the entire connected landmass.

## Step-by-Step Execution Trace

### Example: A small 3x3 grid `[["1","1","0"],["1","0","1"],["0","1","1"]]`

1.  **Start Scan**: `island_count = 0`.
2.  **At `(0,0)`**: `grid[0][0]` is `'1'`.
      - Increment `island_count` to **1**.
      - Call `dfs(0,0)`. The DFS will recursively visit and change `(0,0)`, `(0,1)`, and `(1,0)` to `'0'`s. The grid becomes `[["0","0","0"],["0","0","1"],["0","1","1"]]`.
3.  **Continue Scan**: The main loop continues. It skips all the new `'0'`s.
4.  **At `(1,2)`**: `grid[1][2]` is `'1'`.
      - Increment `island_count` to **2**.
      - Call `dfs(1,2)`. The DFS will visit and sink `(1,2)`, `(2,1)`, and `(2,2)`. The grid becomes all `'0'`s.
5.  **Scan Finishes**: The main loop completes.
6.  **Return `island_count`**: The final answer is **2**.

## Performance Analysis

### Time Complexity: O(m \* n)

  - Where `m` is the number of rows and `n` is the number of columns.
  - Although we have nested loops and recursion, each cell in the grid is visited at most a constant number of times. The main loop touches each cell, and the `dfs` function touches each land cell once before sinking it.

### Space Complexity: O(m \* n)

  - This is the space used by the recursion call stack in the worst-case scenario. If the grid is entirely land, the recursion could go `m * n` levels deep before backtracking.

## Alternative Approaches Comparison

### Approach 1: Depth-First Search (DFS - Our Solution)

  - ✅ Elegant and concise when implemented recursively.
  - ❌ Can lead to a stack overflow error on extremely large/deep islands (not an issue with LeetCode's constraints).

### Approach 2: Breadth-First Search (BFS)

  - Uses a `queue` data structure instead of recursion.
  - ✅ Avoids recursion depth issues.
  - ❌ Requires slightly more code to manage the queue explicitly.

## Why the "Sinking" Matters

The line `grid[r][c] = '0'` is the most important part of the `dfs` function.

  - **It Marks the Node as Visited**: This prevents the main loop from counting the same island multiple times.
  - **It Prevents Infinite Loops**: Without this line, a `dfs` call on `(r, c)` would visit its neighbor `(r, c+1)`, which would then immediately call `dfs` back on `(r, c)`, creating an infinite recursion.

## Key Learning Points

  - How to model a grid as an implicit graph.
  - How to find "connected components" using a traversal algorithm.
  - The implementation and logic of Depth-First Search (DFS).
  - The critical importance of marking nodes as "visited" during a graph traversal.

## Real-World Applications

  - **Image Processing**: Finding contiguous regions of pixels ("blob detection") to identify objects.
  - **Network Analysis**: Finding clusters of connected computers or nodes.
  - **Geographic Information Systems (GIS)**: Analyzing connected landmasses or flood plains on a map.
  - **Game Development**: For pathfinding algorithms or determining connected areas on a game map.