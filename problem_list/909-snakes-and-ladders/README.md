# 909\. Snakes and Ladders - Solution Explanation

## Problem Overview

You are asked to find the **minimum number of moves** to get from square 1 to the final square (`n*n`) on a Snakes and Ladders board.

**Key Rules:**

1.  **Board Layout**: The board is numbered in a "Boustrophedon" style, meaning it starts at the bottom-left and zig-zags up, with every other row reversing direction.
2.  **Movement**: You move by a standard 1-6 dice roll.
3.  **Snakes & Ladders**: If you land on a square with a number other than `-1`, you must immediately move to the destination square indicated by that number.
4.  **No Chaining**: You only take a snake or ladder once per turn. If a ladder takes you to the start of another snake, you do not follow it.

## Key Insights

### Shortest Path -\> Breadth-First Search (BFS)

The phrase "least number of dice rolls" is the biggest clue. This is a classic **shortest path problem** on an unweighted graph (since each dice roll counts as one move). The best algorithm for this is **Breadth-First Search (BFS)**. BFS explores the graph level by level, guaranteeing that the first time we reach the destination, it will be via the shortest possible path.

### Coordinate Conversion

The main sub-problem is that the game is played with square numbers (1, 2, 3...), but the snakes and ladders are stored in a 2D grid (`board[row][col]`). We need a reliable helper function to convert any square number into its `(row, col)` coordinate.

## Solution Approach

Our solution uses BFS to explore the board. A queue will store the states `(square, moves)`, and a `visited` set will prevent us from processing the same square multiple times.

```python
import collections
from typing import List

class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)
        
        def get_coords(square):
            s_minus_1 = square - 1
            row_from_bottom = s_minus_1 // n
            row = (n - 1) - row_from_bottom
            col = s_minus_1 % n if row_from_bottom % 2 == 0 else (n - 1) - (s_minus_1 % n)
            return row, col

        queue = collections.deque([(1, 0)])
        visited = {1}
        
        while queue:
            square, moves = queue.popleft()
            
            for i in range(1, 7):
                next_square = square + i
                if next_square > n * n:
                    break
                
                r, c = get_coords(next_square)
                destination = board[r][c] if board[r][c] != -1 else next_square
                
                if destination == n * n:
                    return moves + 1
                
                if destination not in visited:
                    visited.add(destination)
                    queue.append((destination, moves + 1))
                    
        return -1
```

**Strategy:**

1.  **Coordinate Helper**: Create a function `get_coords` that handles the complex Boustrophedon mapping.
2.  **BFS Setup**: Initialize a queue with the starting state `(square=1, moves=0)` and a `visited` set.
3.  **Process Queue**: While the queue is not empty, dequeue a state.
4.  **Explore Moves**: For the dequeued square, simulate a 6-sided dice roll to find all possible next squares.
5.  **Find True Destination**: For each next square, use the helper function to get its coordinates and check the board for a snake or ladder, determining the final destination.
6.  **Check for Win/Enqueue**: If the destination is the final square, return the move count. If it's a new, unvisited square, add it to the `visited` set and the queue.
7.  **Handle Impossible Cases**: If the queue becomes empty and the final square was never reached, return `-1`.

## Detailed Code Analysis

### `get_coords(square)` Helper Function

```python
def get_coords(square):
    s_minus_1 = square - 1
    row_from_bottom = s_minus_1 // n
    row = (n - 1) - row_from_bottom
    col = s_minus_1 % n if row_from_bottom % 2 == 0 else (n - 1) - (s_minus_1 % n)
    return row, col
```

  - This function is the bridge between the 1D game logic and the 2D board storage.
  - It uses integer division (`//`) to determine the row from the bottom and the modulo operator (`%`) to determine the column, reversing the column calculation for odd-numbered rows (from the bottom) to account for the Boustrophedon style.

### BFS Initialization

```python
queue = collections.deque([(1, 0)])
visited = {1}
```

  - We use `collections.deque` for an efficient queue implementation. We start at square `1` with `0` moves.
  - The `visited` set is crucial to prevent re-visiting squares and getting caught in infinite loops (e.g., a snake leading to a ladder that goes back up).

### Main BFS Loop

```python
while queue:
    square, moves = queue.popleft()
    # ...
```

  - The loop continues as long as there are reachable squares to explore.

### Dice Roll and Destination Logic

```python
for i in range(1, 7):
    next_square = square + i
    # ...
    r, c = get_coords(next_square)
    destination = board[r][c] if board[r][c] != -1 else next_square
```

  - This inner loop simulates the dice roll.
  - It finds the `(r,c)` of the landing square and then checks for a snake or ladder to determine the final `destination` for that move.

## Step-by-Step Execution Trace

### Example: `board = [[-1,-1],[-1,3]]` (n=2, goal=4)

| `queue` | `visited` | Dequeued `(sq, mv)` | `next_sq` → `dest` | Action |
| :--- | :--- | :--- | :--- | :--- |
| `deque([(1, 0)])` | `{1}` | | | Initial state |
| `deque([])` | `{1}` | `(1, 0)` | | Dequeue `(1,0)` |
| ... | ... | ... | 1+1=2 → 3 | `3` not in `visited`. Add 3 to `visited` and `queue`. |
| `deque([(3, 1)])` | `{1, 3}` | | 1+2=3 → 3 | `3` is in `visited`. Do nothing. |
| ... | ... | ... | 1+3=4 → 4 | `4` is goal\! Return `moves + 1` = `0 + 1` = **1**. |

  - The function correctly returns `1`.

## Performance Analysis

### Time Complexity: O(n^2)

  - Where `n` is the side length of the board. In the worst case, BFS will visit every square on the `n x n` board exactly once. The work done at each square is constant (a loop of 6).

### Space Complexity: O(n^2)

  - In the worst case, the `queue` and the `visited` set could store all `n^2` squares.

## Alternative Approaches Comparison

### Approach 1: Breadth-First Search (BFS - Our Solution)

  - ✅ Guarantees finding the shortest path in terms of moves.
  - ✅ The standard, optimal algorithm for this type of problem.

### Approach 2: Depth-First Search (DFS)

  - ❌ Would find *a* path to the end, but it's **not guaranteed** to be the shortest one.
  - ❌ A poor choice for "least number of..." problems.

## Key Learning Points

  - Recognizing "shortest/least/minimum moves" problems as BFS problems.
  - The implementation of BFS using a queue and a `visited` set.
  - Breaking down a problem into a core algorithm (BFS) and a helper function (coordinate conversion).

## Real-World Applications

  - **Shortest Path Finding**: The core application. This is used in GPS systems (e.g., Google Maps), network routing (finding the fastest way for data to travel), and game AI.
  - **Web Crawling**: Crawlers often explore websites level by level, similar to BFS.
  - **Social Networks**: Finding the "degrees of separation" between two people.