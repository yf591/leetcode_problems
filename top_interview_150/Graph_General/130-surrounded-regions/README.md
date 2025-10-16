# 130\. Surrounded Regions - Solution Explanation

## Problem Overview

You are given an `m x n` grid (`board`) containing `'X'`s and `'O'`s. The task is to "capture" all the regions of `'O'`s that are completely surrounded by `'X'`s.

**Definitions:**

  - **Region**: A group of `'O'`s that are connected horizontally or vertically.
  - **Surrounded Region**: A region of `'O'`s where every `'O'` is surrounded by `'X'`s. Crucially, this means that **no `'O'` in the region can be on the border of the board**.
  - **Capture**: To capture a region, you must flip all of its `'O'`s to `'X'`s.
  - **In-place**: The modification must happen on the original board.

**Example:**

  - **Input Board:**
    ```
    [ ["X","X","X","X"],
      ["X","O","O","X"],
      ["X","X","O","X"],
      ["X","O","X","X"] ]
    ```
  - **Explanation**: The group of `'O'`s in the middle is surrounded. The single `'O'` at the bottom is on the border, so it (and any region connected to it) is *not* surrounded.
  - **Output Board:**
    ```
    [ ["X","X","X","X"],
      ["X","X","X","X"],
      ["X","X","X","X"],
      ["X","O","X","X"] ]
    ```

## Key Insights

### 1\. The "Chain Reaction" Trap

A naive approach might be to scan the grid, and for each `'O'`, check if it's surrounded. This is very difficult and inefficient. Another trap is to immediately flip an `'O'` to an `'X'` as you go. This destroys the original state of the board, which is needed to correctly determine the fate of its neighbors.

### 2\. Inverting the Logic: Find What to *Keep*, Not What to *Capture*

This is the most critical insight. Instead of trying to find all the complex "surrounded" regions, it's vastly simpler to find the **"unsurrounded" regions** and protect them. The rest can then be captured.

**What makes an 'O' unsourrounded (or "safe")?**

  - An `'O'` is safe if it is on the **border** of the board.
  - An `'O'` is also safe if it is **connected** (horizontally or vertically) to another safe `'O'`.

This means any region of `'O'`s that touches the border of the board is completely safe. All other `'O'`s are, by definition, surrounded.

### 3\. The "Border DFS" Strategy

This insight leads to a beautiful algorithm:

1.  **Start from the Borders**: Treat every `'O'` on the four edges of the board as a starting point.
2.  **Mark the Safe Zones**: From each of these border `'O'`s, perform a traversal (like a Depth-First Search or "flood fill") to find every single connected `'O'`. Mark all of these connected, "safe" `'O'`s with a temporary placeholder, like `'S'`.
3.  **Capture the Rest**: After you've marked all the safe zones, make a final pass through the entire grid.
      - Any cell that is still an `'O'` was never reached from the border. It must be a surrounded region. Flip it to an `'X'`.
      - Any cell marked `'S'` is part of a safe, border-connected region. Flip it back to `'O'`.

## Solution Approach

This solution implements the efficient two-pass DFS approach. The first pass identifies and marks all "safe" `'O'`s starting from the borders. The second pass performs the final flips based on these marks.

```python
from typing import List

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
            A recursive helper function to find all 'O's connected to a
            starting point and mark them as 'S' (Safe).
            """
            # Base case: Stop if out of bounds or if the cell is not an 'O'.
            if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != 'O':
                return
            
            # Mark the current cell as Safe to prevent re-visiting.
            board[r][c] = 'S'
            
            # Recursively call on all 4 neighbors.
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # --- Pass 1: Mark all 'O's connected to the border as 'S' ---
        
        # Iterate through the top and bottom borders.
        for c in range(cols):
            if board[0][c] == 'O': dfs(0, c)
            if board[rows - 1][c] == 'O': dfs(rows - 1, c)

        # Iterate through the left and right borders.
        for r in range(rows):
            if board[r][0] == 'O': dfs(r, 0)
            if board[r][cols - 1] == 'O': dfs(r, cols - 1)

        # --- Pass 2: Flip the remaining 'O's to 'X's and 'S's back to 'O's ---
        
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'
                elif board[r][c] == 'S':
                    board[r][c] = 'O'
```

## Detailed Code Analysis

### The `dfs(r, c)` Helper Function

This is our "flood fill" or marking tool.

  - **`if r < 0 or ... or board[r][c] != 'O': return`**: This is the base case for the recursion. The function stops if it goes off the board or if it hits a cell that isn't an `'O'` (it could be an `'X'` or an already-marked `'S'`).
  - **`board[r][c] = 'S'`**: This is the marking step. By changing the `'O'` to an `'S'`, we mark it as "safe" and simultaneously ensure we don't visit it again in an infinite loop.
  - **`dfs(r + 1, c)` etc.**: These are the recursive calls that propagate the search to all four neighbors, finding the entire connected region.

### Pass 1: The Marking Phase

```python
for c in range(cols):
    if board[0][c] == 'O': dfs(0, c)
    if board[rows - 1][c] == 'O': dfs(rows - 1, c)

for r in range(rows):
    if board[r][0] == 'O': dfs(r, 0)
    if board[r][cols - 1] == 'O': dfs(r, cols - 1)
```

  - These two loops systematically scan all four borders of the grid.
  - Whenever an `'O'` is found on a border, it triggers a `dfs` call. This `dfs` call will find every single `'O'` connected to that border `'O'` and mark them all as `'S'`.

### Pass 2: The Flipping Phase

```python
for r in range(rows):
    for c in range(cols):
        if board[r][c] == 'O':
            board[r][c] = 'X'
        elif board[r][c] == 'S':
            board[r][c] = 'O'
```

  - After Pass 1, the board is in an intermediate state with `'X'`, `'O'`, and `'S'` characters.
  - This final pass is simple. It iterates through every cell of the entire grid.
  - **`if board[r][c] == 'O'`**: If a cell is still an `'O'`, it means it was never reached by any of the border `dfs` calls. By our logic, it must be part of a surrounded region. We capture it by flipping it to `'X'`.
  - **`elif board[r][c] == 'S'`**: If a cell is an `'S'`, we know it's a safe, border-connected cell. We simply restore it back to its original `'O'` state.

## Step-by-Step Execution Trace

Let's trace `board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]`.

### **Initial Board:**

```
[ ["X","X","X","X"],
  ["X","O","O","X"],
  ["X","X","O","X"],
  ["X","O","X","X"] ]
```

-----

### **Pass 1: Marking from Borders**

1.  **Top Border `(0, c)`**: All `'X'`s. No `dfs` calls.
2.  **Bottom Border `(3, c)`**:
      - At `c=1`, `board[3][1]` is `'O'`. This is a border 'O'.
      - Call `dfs(3, 1)`.
      - `board[3][1]` is changed to `'S'`.
      - `dfs` checks its neighbors. `(2,1)` is `'X'`, `(3,0)` is `'X'`, `(3,2)` is `'X'`. There are no other `'O'`s connected to it. The `dfs` call ends.
3.  **Left Border `(r, 0)`**: All `'X'`s. No `dfs` calls.
4.  **Right Border `(r, 3)`**: All `'X'`s. No `dfs` calls.

**Board after Marking Pass:**

```
[ ["X","X","X","X"],
  ["X","O","O","X"],
  ["X","X","O","X"],
  ["X","S","X","X"] ]
```

-----

### **Pass 2: Flipping and Restoring**

  - The code iterates through every cell `(r, c)`.
  - It finds the `'O'` at `(1,1)`. The `if board[r][c] == 'O'` condition is true. It flips `board[1][1]` to `'X'`.
  - It finds the `'O'` at `(1,2)`. It flips `board[1][2]` to `'X'`.
  - It finds the `'O'` at `(2,2)`. It flips `board[2][2]` to `'X'`.
  - It finds the `'S'` at `(3,1)`. The `elif board[r][c] == 'S'` condition is true. It restores `board[3][1]` to `'O'`.

**Final Board:**

```
[ ["X","X","X","X"],
  ["X","X","X","X"],
  ["X","X","X","X"],
  ["X","O","X","X"] ]
```

The function modifies the board in-place and returns nothing.

## Performance Analysis

### Time Complexity: O(m \* n)

  - Where `m` is the number of rows and `n` is the number of columns.
  - In the first pass, we iterate the borders. The `dfs` function, in the worst case (a board of all `'O'`s), will visit every cell exactly once.
  - The second pass iterates through all `m * n` cells again.
  - The total time is proportional to the number of cells.

### Space Complexity: O(m \* n)

  - The space complexity is determined by the depth of the recursion call stack for the `dfs`. In the worst-case scenario (a long, snake-like path of `'O'`s that fills the grid), the recursion could go `m * n` levels deep. Therefore, the space is `O(m * n)`.