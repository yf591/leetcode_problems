# 994\. Rotting Oranges - Solution Explanation

## Problem Overview

You are given an `m x n` grid where each cell represents one of three things:

  - `0`: An empty cell.
  - `1`: A **fresh** orange.
  - `2`: A **rotten** orange.

The rule is that every minute, any fresh orange (`1`) that is **4-directionally adjacent** (up, down, left, right) to a rotten orange (`2`) becomes rotten itself.

The goal is to determine the **minimum number of minutes** required until there are no fresh oranges left in the grid. If it's impossible for all fresh oranges to rot (e.g., some are isolated), return `-1`.

**Examples:**

```python
Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
Output: 4
# Minute 0: [[2,1,1],[1,1,0],[0,1,1]]
# Minute 1: [[2,2,1],[2,1,0],[0,1,1]]
# Minute 2: [[2,2,2],[2,2,0],[0,1,1]]
# Minute 3: [[2,2,2],[2,2,0],[0,2,1]]
# Minute 4: [[2,2,2],[2,2,0],[0,2,2]] - All fresh are rotten.

Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
Output: -1
# The orange at (2,0) is blocked by empty cells and never rots.

Input: grid = [[0,2]]
Output: 0
# No fresh oranges initially, so 0 minutes needed.
```

## Key Insights

### 1\. Simultaneous Process -\> Level-by-Level

The core mechanic is that *all* oranges adjacent to rotten ones become rotten *simultaneously* each minute. This step-by-step, simultaneous progression across the grid strongly suggests a **level-order traversal**.

### 2\. Shortest Time -\> Breadth-First Search (BFS)

The problem asks for the *minimum* time. BFS is the standard algorithm for finding the shortest path (in terms of steps or levels) from a starting point to a target in an unweighted graph (or grid). Here, each "minute" corresponds to one level of the BFS.

### 3\. Multi-Source BFS

The rotting process doesn't start from just one orange; it starts from *all* oranges that are initially rotten (`2`). This means we need a **Multi-Source BFS**. The algorithm handles this naturally: we simply add *all* initial rotten oranges to the queue at the beginning, all with a starting time of `0`.

### 4\. Tracking State

To solve this, we need to keep track of:

  - The coordinates of rotten oranges that can still spread (`queue`).
  - The time (minutes) elapsed for each rotting event.
  - Whether any fresh oranges remain at the end.

## Solution Approach

This solution implements a Multi-Source BFS. It first scans the grid to initialize the queue with all initially rotten oranges and to count the total number of fresh oranges. Then, it runs the BFS simulation. Each level of the BFS corresponds to one minute. During the traversal, fresh oranges are marked as rotten (by changing their value in the grid), and the count of fresh oranges is decremented. The time is tracked, and the final check determines the result.

```python
import collections
from typing import List

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        # Queue stores tuples: (row, col, time_when_rotted)
        queue = collections.deque()
        fresh_oranges_count = 0
        # minutes_elapsed will track the time of the last rotting event
        minutes_elapsed = 0
        
        # --- Step 1: Initialize Queue and Count Fresh Oranges ---
        # Scan the grid to find initial state
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    # Add initially rotten oranges to queue with time 0
                    queue.append((r, c, 0))
                elif grid[r][c] == 1:
                    # Count the total number of fresh oranges
                    fresh_oranges_count += 1
        
        # Define the 4 directions for neighbors
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
        
        # --- Step 2: Perform BFS (Simulate Rotting) ---
        while queue:
            r, c, time = queue.popleft()
            
            # Keep track of the maximum time reached
            minutes_elapsed = max(minutes_elapsed, time)
            
            # Explore the 4 neighbors of the currently rotten orange
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # Check if the neighbor is valid and is a fresh orange
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    # Rot the fresh orange (mark as visited and rotten)
                    grid[nr][nc] = 2
                    # Decrement the count of remaining fresh oranges
                    fresh_oranges_count -= 1
                    # Add the newly rotten orange to the queue to spread in the next minute
                    queue.append((nr, nc, time + 1))
                    
        # --- Step 3: Check Result ---
        # If fresh_oranges_count is 0, all oranges rotted. Return the time of the last event.
        # Otherwise, some oranges were unreachable.
        return minutes_elapsed if fresh_oranges_count == 0 else -1
```

## Detailed Code Analysis

### Step 1: Initialization

```python
rows, cols = len(grid), len(grid[0])
queue = collections.deque()
fresh_oranges_count = 0
minutes_elapsed = 0
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == 2:
            queue.append((r, c, 0))
        elif grid[r][c] == 1:
            fresh_oranges_count += 1
```

  - We get the grid dimensions.
  - We initialize an empty `deque` to serve as our BFS queue.
  - `fresh_oranges_count`: This is crucial. We need to know how many fresh oranges exist initially to determine if all of them eventually rot.
  - `minutes_elapsed`: This will track the timestamp of the last orange to rot.
  - The nested loops scan the initial grid:
      - If a cell is `2` (rotten), its coordinates `(r, c)` and starting time `0` are added to the queue. This sets up the multi-source start.
      - If a cell is `1` (fresh), we increment `fresh_oranges_count`.

### Step 2: The Main BFS Loop

```python
while queue:
    r, c, time = queue.popleft()
    minutes_elapsed = max(minutes_elapsed, time)
    # ... explore neighbors ...
```

  - The loop continues as long as there are rotten oranges in the queue that might still spread.
  - `r, c, time = queue.popleft()`: We get the coordinates of a rotten orange and the `time` (minute) at which it became rotten.
  - `minutes_elapsed = max(minutes_elapsed, time)`: We update our overall timer. Since BFS processes level by level, the `time` value of the very last orange dequeued will represent the total minutes needed.

### Step 3: Neighbor Exploration and Infection

```python
for dr, dc in directions:
    nr, nc = r + dr, c + dc
    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
        grid[nr][nc] = 2
        fresh_oranges_count -= 1
        queue.append((nr, nc, time + 1))
```

  - We iterate through the 4 possible directions.
  - `nr, nc = r + dr, c + dc`: Calculate the neighbor's coordinates.
  - The `if` condition checks three things:
    1.  `0 <= nr < rows and 0 <= nc < cols`: Is the neighbor within the grid bounds?
    2.  `grid[nr][nc] == 1`: Is the neighbor a fresh orange? (We don't care about empty cells or already rotten ones).
  - If the neighbor is valid and fresh:
      - `grid[nr][nc] = 2`: We infect it\! Changing the value to `2` also marks it as "visited" for the purpose of this BFS, preventing it from being added to the queue multiple times.
      - `fresh_oranges_count -= 1`: We decrement our count of remaining fresh oranges.
      - `queue.append((nr, nc, time + 1))`: We add the newly rotten orange to the queue. Its time is `time + 1` because it rots in the *next* minute.

### Step 4: The Final Check

```python
return minutes_elapsed if fresh_oranges_count == 0 else -1
```

  - After the `while` loop finishes (the queue is empty, meaning the rotting process has stopped spreading), we check our `fresh_oranges_count`.
  - If `fresh_oranges_count == 0`: All the initial fresh oranges were successfully reached and rotted. We return `minutes_elapsed`, which holds the time the last orange finished rotting.
  - If `fresh_oranges_count > 0`: Some fresh oranges were unreachable (like the one in Example 2). We return `-1`.

## Step-by-Step Execution Trace

Let's trace `grid = [[2,1,1],[1,1,0],[0,1,1]]` with extreme detail.

### **Initial State:**

  - `rows=3`, `cols=3`
  - `queue = deque([(0, 0, 0)])` (only one initial rotten orange)
  - `fresh_oranges_count = 6`
  - `minutes_elapsed = 0`

-----

### **BFS Loop - Minute 0**

1.  Dequeue `(0, 0, 0)`. `minutes_elapsed = max(0, 0) = 0`.
2.  Neighbors of `(0, 0)`: `(1, 0)` and `(0, 1)`.
      - Neighbor `(1, 0)`: Is `1`. Mark `grid[1][0]=2`. `fresh_oranges_count`=5. Enqueue `(1, 0, 1)`.
      - Neighbor `(0, 1)`: Is `1`. Mark `grid[0][1]=2`. `fresh_oranges_count`=4. Enqueue `(0, 1, 1)`.
        **Queue State**: `deque([(1, 0, 1), (0, 1, 1)])`
        **Grid State**: `[[2,2,1],[2,1,0],[0,1,1]]`

-----

### **BFS Loop - Minute 1**

1.  Dequeue `(1, 0, 1)`. `minutes_elapsed = max(0, 1) = 1`.
2.  Neighbors of `(1, 0)`: `(0, 0)`(2), `(2, 0)`(0), `(1, 1)`(1).
      - Neighbor `(1, 1)`: Is `1`. Mark `grid[1][1]=2`. `fresh_oranges_count`=3. Enqueue `(1, 1, 2)`.
3.  Dequeue `(0, 1, 1)`. `minutes_elapsed = max(1, 1) = 1`.
4.  Neighbors of `(0, 1)`: `(0, 0)`(2), `(1, 1)`(2, just rotted), `(0, 2)`(1).
      - Neighbor `(0, 2)`: Is `1`. Mark `grid[0][2]=2`. `fresh_oranges_count`=2. Enqueue `(0, 2, 2)`.
        **Queue State**: `deque([(1, 1, 2), (0, 2, 2)])`
        **Grid State**: `[[2,2,2],[2,2,0],[0,1,1]]`

-----

### **BFS Loop - Minute 2**

1.  Dequeue `(1, 1, 2)`. `minutes_elapsed = max(1, 2) = 2`.
2.  Neighbors of `(1, 1)`: `(0, 1)`(2), `(2, 1)`(1), `(1, 0)`(2), `(1, 2)`(0).
      - Neighbor `(2, 1)`: Is `1`. Mark `grid[2][1]=2`. `fresh_oranges_count`=1. Enqueue `(2, 1, 3)`.
3.  Dequeue `(0, 2, 2)`. `minutes_elapsed = max(2, 2) = 2`.
4.  Neighbors of `(0, 2)`: `(1, 2)`(0), `(0, 1)`(2). No fresh neighbors.
    **Queue State**: `deque([(2, 1, 3)])`
    **Grid State**: `[[2,2,2],[2,2,0],[0,2,1]]`

-----

### **BFS Loop - Minute 3**

1.  Dequeue `(2, 1, 3)`. `minutes_elapsed = max(2, 3) = 3`.
2.  Neighbors of `(2, 1)`: `(1, 1)`(2), `(2, 0)`(0), `(2, 2)`(1).
      - Neighbor `(2, 2)`: Is `1`. Mark `grid[2][2]=2`. `fresh_oranges_count`=0. Enqueue `(2, 2, 4)`.
        **Queue State**: `deque([(2, 2, 4)])`
        **Grid State**: `[[2,2,2],[2,2,0],[0,2,2]]`

-----

### **BFS Loop - Minute 4**

1.  Dequeue `(2, 2, 4)`. `minutes_elapsed = max(3, 4) = 4`.
2.  Neighbors of `(2, 2)`: `(1, 2)`(0), `(2, 1)`(2). No fresh neighbors.
    **Queue State**: `deque([])`

-----

### **End of Traversal**

  - The `while queue:` condition is now **False**. The loop terminates.

### **Final Check**

  - `fresh_oranges_count` is 0.
  - The condition `fresh_oranges_count == 0` is True.
  - The function returns `minutes_elapsed`, which is **4**.

## Performance Analysis

### Time Complexity: O(m \* n)

  - Where `m` is the number of rows and `n` is the number of columns.
  - The initial scan of the grid takes `O(m * n)` time.
  - The BFS process visits each cell at most once. Enqueueing and dequeueing are `O(1)`.
  - The total time complexity is dominated by the grid traversals, making it `O(m * n)`.

### Space Complexity: O(m \* n)

  - In the worst-case scenario (e.g., a grid where all oranges are initially rotten or become rotten quickly), the `queue` could potentially hold all `m * n` cells.
  - Therefore, the space complexity is `O(m * n)`.