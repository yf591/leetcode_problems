# 1926\. Nearest Exit from Entrance in Maze - Solution Explanation

## Problem Overview

You are given an `m x n` `maze` represented by a grid. Cells can be empty (`.`) or walls (`+`). You start at a given `entrance` cell (`[row, col]`), which is guaranteed to be empty.

**The Goal:**
Find the **shortest path** (minimum number of steps) from the `entrance` to the nearest **exit**.

**Definitions:**

  - **Movement**: You can move one step up, down, left, or right.
  - **Restrictions**: You cannot move into a wall (`+`) or outside the maze boundaries.
  - **Exit**: An exit is an **empty cell (`.`)** located on the **border** of the maze (first/last row or first/last column).
  - **Important**: The `entrance` cell itself **does not count** as an exit, even if it's on the border.

**Output:**

  - Return the number of steps in the shortest path to an exit.
  - Return `-1` if no exit is reachable from the entrance.

**Example 1:**

```python
Input: maze = [["+","+",".","+"],[".",".",".","+"],["+","+","+","."]], entrance = [1,2]
Output: 1
Explanation: From [1,2], you can move up to [0,2]. [0,2] is on the border and is empty, making it an exit. This takes 1 step.
```

## Key Insights

### 1\. Shortest Path -\> Breadth-First Search (BFS)

The problem explicitly asks for the **"nearest exit"** or the **"shortest path"** in terms of the number of steps. In graph theory (and grids can be thought of as graphs), the standard algorithm for finding the shortest path in an unweighted graph (where each step has a cost of 1) is **Breadth-First Search (BFS)**.

### 2\. Level-by-Level Exploration

BFS works by exploring the maze outwards from the starting point, layer by layer.

  - It first visits all cells reachable in 1 step.
  - Then, it visits all *new* cells reachable in 2 steps.
  - Then, all *new* cells reachable in 3 steps, and so on.

Because of this level-by-level exploration, the **first time** BFS reaches an exit cell, it is guaranteed to have found the path with the minimum number of steps.

### 3\. Necessary Tools for BFS

To implement BFS on a grid, we need:

  - **A Queue**: To keep track of the cells to visit. Since we need the number of steps, we'll store tuples `(row, col, steps)` in the queue. Python's `collections.deque` is ideal.
  - **A Visited Set**: To avoid re-visiting the same cell multiple times (which would be inefficient and could lead to infinite loops if there were cycles, though not possible in a simple maze pathfinding). A `set` provides fast `O(1)` average time complexity for checking if we've been somewhere.

## Solution Approach

This solution implements the BFS algorithm. It starts at the `entrance`, explores valid neighbors layer by layer, and returns the step count as soon as the first exit is found.

```python
import collections
from typing import List

class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        rows, cols = len(maze), len(maze[0])
        start_row, start_col = entrance[0], entrance[1]
        
        # Initialize the queue with the starting position and 0 steps.
        # Queue stores tuples: (row, col, steps)
        queue = collections.deque([(start_row, start_col, 0)])
        
        # Initialize a set to keep track of visited cells.
        # Add the entrance immediately.
        visited = {(start_row, start_col)}
        
        # Define the 4 possible movement directions (dr, dc).
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
        
        # --- Start BFS ---
        while queue:
            # Dequeue the current cell and its step count.
            r, c, steps = queue.popleft()
            
            # Explore all 4 potential neighbors.
            for dr, dc in directions:
                nr, nc = r + dr, c + dc # Calculate neighbor coordinates
                
                # --- Check if the neighbor is valid ---
                # 1. Is it within the grid boundaries?
                if 0 <= nr < rows and 0 <= nc < cols:
                    # 2. Is it an empty cell (not a wall)?
                    if maze[nr][nc] == '.':
                        # 3. Have we visited it before?
                        if (nr, nc) not in visited:
                            
                            # --- Found a valid, unvisited neighbor ---
                            
                            # Check if this neighbor is an exit.
                            is_border = (nr == 0 or nr == rows - 1 or nc == 0 or nc == cols - 1)
                            
                            # (The entrance itself is handled by the visited check)
                            if is_border:
                                # Found the nearest exit! Return the steps taken to reach it.
                                return steps + 1

                            # If it's not an exit, mark it as visited and add to queue.
                            visited.add((nr, nc))
                            queue.append((nr, nc, steps + 1))
                            
        # If the queue becomes empty and we never returned, it means no exit was reachable.
        return -1
```

## Detailed Code Analysis

### Step 1: Initialization

```python
rows, cols = len(maze), len(maze[0])
start_row, start_col = entrance[0], entrance[1]
queue = collections.deque([(start_row, start_col, 0)])
visited = {(start_row, start_col)}
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
```

  - We get the dimensions of the maze.
  - We initialize the `queue` using `collections.deque` for efficiency. The first element is a tuple containing the starting row, starting column, and the initial step count `0`.
  - We initialize the `visited` set and immediately add the starting `(row, col)` tuple to it. This prevents us from re-visiting the entrance and incorrectly classifying it as an exit if it happens to be on the border.
  - `directions` stores the changes in `(row, col)` for moving up, down, left, and right.

### Step 2: The Main BFS Loop

```python
while queue:
    r, c, steps = queue.popleft()
    # ... explore neighbors ...
```

  - The loop continues as long as there are cells in the queue to explore.
  - `r, c, steps = queue.popleft()`: We get the coordinates and the steps taken *so far* to reach this cell from the front of the queue (FIFO).

### Step 3: Neighbor Exploration

```python
for dr, dc in directions:
    nr, nc = r + dr, c + dc
    # ... validation checks ...
```

  - We loop through the four possible `directions`.
  - `nr, nc = r + dr, c + dc`: We calculate the coordinates of the potential `neighbor`.

### Step 4: Neighbor Validation

```python
if 0 <= nr < rows and 0 <= nc < cols and \
   maze[nr][nc] == '.' and (nr, nc) not in visited:
```

  - This multi-part `if` statement checks if the calculated neighbor `(nr, nc)` is a valid place to move:
      - `0 <= nr < rows and 0 <= nc < cols`: Checks if it's within the grid boundaries.
      - `maze[nr][nc] == '.'`: Checks if it's an empty cell (not a wall `+`).
      - `(nr, nc) not in visited`: Checks if we have already processed this cell.

### Step 5: Exit Check

```python
is_border = (nr == 0 or nr == rows - 1 or nc == 0 or nc == cols - 1)
if is_border:
    return steps + 1
```

  - If the neighbor passed all the validation checks, we now check if it's an exit.
  - An exit must be on the border (`is_border` check).
  - **Crucially**, we do *not* need an explicit `and (nr, nc) != (start_row, start_col)` check here. Why? Because we added the `entrance` to the `visited` set at the very beginning. If the neighbor *was* the entrance, the `(nr, nc) not in visited` check in Step 4 would have already failed, and we wouldn't have reached this point.
  - If `is_border` is true, we have found the nearest exit. The number of steps is the `steps` taken to reach the *previous* cell `(r, c)`, plus one more step to reach this neighbor. We return `steps + 1`.

### Step 6: Enqueueing Non-Exits

```python
visited.add((nr, nc))
queue.append((nr, nc, steps + 1))
```

  - If the valid neighbor was *not* an exit, we need to continue the search from it.
  - `visited.add((nr, nc))`: We mark it as visited so we don't process it again.
  - `queue.append((nr, nc, steps + 1))`: We add it to the back of the queue, along with the incremented step count.

### Step 7: No Path Found

```python
return -1
```

  - If the `while queue:` loop finishes, it means the queue became empty, but we never encountered an exit cell. Therefore, no exit is reachable, and we return `-1`.

## Step-by-Step Execution Trace

Let's trace `maze = [["+","+",".","+"],[".",".",".","+"],["+","+","+","."]]`, `entrance = [1,2]`.

### **Initial State:**

  - `rows=3`, `cols=4`
  - `start=(1,2)`
  - `queue = deque([(1, 2, 0)])`
  - `visited = {(1, 2)}`

-----

### **BFS Loop - Iteration 1**

1.  Dequeue `(1, 2, 0)`. `r=1, c=2, steps=0`.
2.  Explore Neighbors of `(1, 2)`:
      - **Up `(-1, 0)` -\> `(0, 2)`**: Valid? Yes (In bounds, '.', not visited). Is Exit? Yes (border). **Return `steps + 1` = `0 + 1 = 1`**.

The algorithm finds the exit at `(0, 2)` in just one step and terminates immediately, returning `1`.

## Performance Analysis

### Time Complexity: O(m \* n)

  - Where `m` is the number of rows and `n` is the number of columns.
  - In the worst case, the BFS algorithm might visit every single empty cell (`.`) in the maze exactly once. Each visit involves checking neighbors, which is a constant amount of work.

### Space Complexity: O(m \* n)

  - The space complexity is determined by the maximum size of the `queue` and the `visited` set.
  - In the worst case (e.g., a maze mostly filled with empty cells), both the queue and the visited set could potentially store coordinates for nearly all `m * n` cells.