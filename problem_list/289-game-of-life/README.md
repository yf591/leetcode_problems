# 289\. Game of Life - Solution Explanation

## Problem Overview

The task is to simulate one "generation" of Conway's Game of Life on an `m x n` grid. You are given the current state of the board, and you must update it to the next state **in-place**.

**State Definitions:**

  - `1`: Represents a **live** cell.
  - `0`: Represents a **dead** cell.

**The Four Rules of Life:**
The next state of every cell is determined **simultaneously** based on the state of its **eight neighbors** (horizontal, vertical, and diagonal).

1.  **Underpopulation**: A **live** cell with fewer than two live neighbors dies (becomes `0`).
2.  **Survival**: A **live** cell with two or three live neighbors lives on to the next generation (stays `1`).
3.  **Overpopulation**: A **live** cell with more than three live neighbors dies (becomes `0`).
4.  **Reproduction**: A **dead** cell with exactly three live neighbors becomes a live cell (becomes `1`).

**Example:**

  - **Input Board:**
    ```
    [ [0,1,0],
      [0,0,1],
      [1,1,1],
      [0,0,0] ]
    ```
  - **Output Board (Next Generation):**
    ```
    [ [0,0,0],
      [1,0,1],
      [0,1,1],
      [0,1,0] ]
    ```

## Key Insights

### The "Simultaneous Update" Challenge

The most critical rule is that all births and deaths occur **simultaneously**. This means that the state of a cell for the next generation must be calculated based on the **current, original state** of its neighbors.

  - **The Trap**: If you iterate through the grid and immediately update a cell (e.g., change a `1` to a `0`), when you later calculate the state of its neighbors, they will see this *new* state, not the original one. This will lead to an incorrect result.

### The `O(1)` Space Constraint and the "Extra States" Trick

A simple way to solve the simultaneity problem is to create a brand new copy of the board. You would read from the original board and write the new states to the copy. This works, but it uses `O(m * n)` extra space, which the problem's follow-up suggests is not optimal.

The key insight for an **in-place, `O(1)` space** solution is to use the board itself as memory. We can't just use `0` and `1`, as that would destroy the original state. So, we introduce **two new, temporary states** to store the transitions:

  - **State `2`**: "Was Live, Will Be Dead". A cell that was `1` and is scheduled to die.
  - **State `3`**: "Was Dead, Will Be Live". A cell that was `0` and is scheduled to be born.

This allows us to record the future state of a cell without erasing its past state. During the calculation, we can still tell that a cell with state `2` was originally live.

## Solution Approach

The solution is a two-pass algorithm. The first pass calculates the next state for every cell and marks them with our temporary states (`2` or `3`) if they change. The second pass cleans up the board, converting the temporary states into the final `0`s and `1`s.

```python
from typing import List

class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        rows, cols = len(board), len(board[0])
        
        # Directions for the 8 neighbors of a cell (horizontal, vertical, diagonal)
        neighbors = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

        # --- Pass 1: Mark cells that will change state ---
        # State 2: Was live (1), will be dead (0).
        # State 3: Was dead (0), will be live (1).
        
        for r in range(rows):
            for c in range(cols):
                live_neighbors = 0
                # Count live neighbors based on their ORIGINAL state.
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor is within bounds.
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # A neighbor is "live" if its original state was 1.
                        # This includes cells currently marked as 1 OR 2.
                        if board[nr][nc] == 1 or board[nr][nc] == 2:
                            live_neighbors += 1
                
                # Apply Game of Life rules to the ORIGINAL state.
                # Rule 1 & 3: A live cell (1) dies.
                if board[r][c] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                    board[r][c] = 2  # Mark as "was live, now dead"
                
                # Rule 4: A dead cell (0) becomes live.
                elif board[r][c] == 0 and live_neighbors == 3:
                    board[r][c] = 3  # Mark as "was dead, now live"

        # --- Pass 2: Finalize the board state ---
        # Convert the temporary states back to 0s and 1s.
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 2:
                    board[r][c] = 0
                elif board[r][c] == 3:
                    board[r][c] = 1
```

## Detailed Code Analysis

### Step 1: The Marking Pass

This is the main logic where we calculate the next state for every cell.

**Neighbor Counting:**

```python
live_neighbors = 0
for dr, dc in neighbors:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols:
        if board[nr][nc] == 1 or board[nr][nc] == 2:
            live_neighbors += 1
```

  - For each cell `(r, c)`, we iterate through the 8 `neighbors` directions.
  - `if 0 <= nr < rows and 0 <= nc < cols`: This is a crucial boundary check to ensure we don't look for neighbors outside the grid.
  - **`if board[nr][nc] == 1 or board[nr][nc] == 2:`**: This is the most clever part. How do we know if a neighbor was *originally* live? We check if its value is `1` (a live cell that won't change) or `2` (a live cell that is scheduled to die). Both of these were `1` at the start of the simulation. We ignore cells with `0` or `3`, as they were originally dead.

**Applying the Rules:**

```python
if board[r][c] == 1 and (live_neighbors < 2 or live_neighbors > 3):
    board[r][c] = 2
elif board[r][c] == 0 and live_neighbors == 3:
    board[r][c] = 3
```

  - We apply the rules to the cell `(r, c)` based on its *original* state (`board[r][c] == 1` or `board[r][c] == 0`).
  - If a cell is changing state, we assign it one of our temporary values, `2` or `3`.
  - If a cell's state does not change (e.g., a live cell with 2 or 3 neighbors), we do nothing and leave its value as `1` or `0`.

### Step 2: The Cleanup Pass

```python
for r in range(rows):
    for c in range(cols):
        if board[r][c] == 2:
            board[r][c] = 0
        elif board[r][c] == 3:
            board[r][c] = 1
```

  - This final pass is very simple. It scans the entire board again.
  - It converts any cell marked for death (`2`) to its final dead state (`0`).
  - It converts any cell marked for birth (`3`) to its final live state (`1`).
  - Cells that were originally `0` or `1` and didn't change are left untouched.

## Step-by-Step Execution Trace

Let's trace a 2x2 section of the input `board = [[0,1],[1,1]]`.

### **Initial Board:**

```
[ [0, 1],
  [1, 1] ]
```

-----

### **Pass 1: Marking**

  - **Cell (0,0)**: Is `0`. Has 3 live neighbors (at 0,1; 1,0; 1,1). Rule 4 applies. `board[0][0]` becomes **3**.
  - **Cell (0,1)**: Is `1`. Has 2 live neighbors (at 1,0; 1,1). Rule 2 applies (survival). It stays **1**.
  - **Cell (1,0)**: Is `1`. Has 2 live neighbors (at 0,1; 1,1). Rule 2 applies (survival). It stays **1**.
  - **Cell (1,1)**: Is `1`. Has 3 live neighbors (at 0,0; 0,1; 1,0). Rule 2 applies (survival). It stays **1**.

**Board after Marking Pass:**

```
[ [3, 1],
  [1, 1] ]
```

-----

### **Pass 2: Cleanup**

  - **Cell (0,0)**: Is `3`. It becomes **1**.
  - **Cell (0,1)**: Is `1`. No change.
  - **Cell (1,0)**: Is `1`. No change.
  - **Cell (1,1)**: Is `1`. No change.

**Final Board:**

```
[ [1, 1],
  [1, 1] ]
```

This matches the second example's output.

## Performance Analysis

### Time Complexity: O(m \* n)

  - Where `m` is the number of rows and `n` is the number of columns.
  - The algorithm makes two full passes over the grid. In the first pass, for each of the `m*n` cells, it checks a constant 8 neighbors. This is `O(m * n * 8)`, which is `O(m * n)`. The second pass is also `O(m * n)`.
  - The total time complexity is `O(m * n) + O(m * n)`, which simplifies to `O(m * n)`.

### Space Complexity: O(1)

  - This is the main advantage of this approach. The board is modified in-place. We only use a few variables for loops and counts. The extra space required is constant and does not depend on the size of the board.