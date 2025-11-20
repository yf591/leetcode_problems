# 79\. Word Search - Solution Explanation

## Problem Overview

You are given an `m x n` grid of characters (`board`) and a string (`word`). The task is to check if the `word` exists in the grid.

**Rules for Constructing the Word:**

1.  The word can be constructed from letters of sequentially adjacent cells.
2.  **Adjacent** means horizontally or vertically neighboring (Up, Down, Left, Right).
3.  The same letter cell may **not** be used more than once in a single word path.

**Example:**

```python
Input: board = [
  ["A","B","C","E"],
  ["S","F","C","S"],
  ["A","D","E","E"]
], word = "ABCCED"

Output: true
```

**Path:** `(0,0) 'A' -> (0,1) 'B' -> (0,2) 'C' -> (1,2) 'C' -> (2,2) 'E' -> (2,1) 'D'`

## Deep Dive: What is Backtracking? 🧠

**Backtracking** is a general algorithmic technique that considers searching every possible combination in order to solve a computational problem.

Think of it like walking through a maze:

1.  **Start**: You stand at a junction.
2.  **Choice**: You choose to go down the path to the **Left**.
3.  **Constraint Check**: You walk for a bit.
      * If you hit a **Dead End** (or a wall), you realize this path won't work.
      * If you find the **Exit**, you win\!
4.  **Backtrack**: If you hit a dead end, you must **walk back** to the junction where you made the decision.
5.  **Next Choice**: Now that you are back at the junction, you try the path to the **Right**.

**In this problem:**

  - **Choice**: "I am at 'A', should I go Up, Down, Left, or Right to find the next letter?"
  - **Constraint**: "Is the neighbor cell the correct letter? Have I visited it already?"
  - **Backtrack**: "The neighbor was wrong (or led to a dead end). I need to un-mark my current position and tell the previous step that this direction failed."

## Key Insights

### 1\. Why DFS (Depth-First Search)?

We are looking for a specific *sequence* or *path*. DFS is ideal for this because it dives deep into one possibility (e.g., `A -> B -> C...`) before giving up and trying another. BFS (Breadth-First Search) spreads out like oil and is harder to manage for specific sequence finding.

### 2\. The "Visited" State

Since we cannot use the same cell twice in one path, we need to mark cells as "visited" as we walk over them.

  - **Naive Approach**: Use a separate `set` or `boolean matrix` to store visited coordinates. This takes extra memory.
  - **Optimized Approach**: Modify the board **in-place**. We can temporarily change the character on the board to a special symbol (like `#`) to mark it as visited. When we backtrack, we change it back to the original letter.

### 3\. Starting Point

We don't know where the word starts. The word could begin at any cell in the grid. Therefore, we must iterate through *every* cell in the grid to attempt to start the search.

## Solution Approach

This solution iterates through every cell. If a cell matches the first letter of the word, it launches a recursive backtracking function (`backtrack`) to try and find the rest of the word.

```python
from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        
        # The recursive helper function
        def backtrack(r, c, index):
            # --- Base Case 1: Success ---
            # We have matched all characters in the word.
            if index == len(word):
                return True
            
            # --- Base Case 2: Failure ---
            # 1. Out of bounds?
            # 2. Character doesn't match the one we need?
            # 3. Already visited (marked as '#')?
            if (r < 0 or r >= rows or 
                c < 0 or c >= cols or 
                board[r][c] != word[index]):
                return False

            # --- Recursive Step: Explore ---
            
            # 1. Mark as visited
            # Save the original character so we can restore it later.
            temp = board[r][c]
            board[r][c] = "#"
            
            # 2. Explore all 4 directions
            # We look for the NEXT character (index + 1)
            found = (backtrack(r + 1, c, index + 1) or  # Down
                     backtrack(r - 1, c, index + 1) or  # Up
                     backtrack(r, c + 1, index + 1) or  # Right
                     backtrack(r, c - 1, index + 1))    # Left
            
            # 3. Backtrack (Un-mark)
            # Restore the original value. This effectively "un-visits" the node
            # so it can be used in other path attempts.
            board[r][c] = temp
            
            return found

        # Main Loop: Try to start the word from every position
        for r in range(rows):
            for c in range(cols):
                # Optimization: Only start DFS if the first letter matches
                if board[r][c] == word[0] and backtrack(r, c, 0):
                    return True
                    
        return False
```

## Detailed Code Analysis

### Step 1: The Main Loop

```python
for r in range(rows):
    for c in range(cols):
        if board[r][c] == word[0] and backtrack(r, c, 0):
            return True
```

  - This loop acts as the "starter." It scans the grid looking for the first letter of the word.
  - `backtrack(r, c, 0)`: This calls the recursive function starting at row `r`, col `c`, looking for the character at `word[0]` (index 0).

### Step 2: The `backtrack` Function - Base Cases

```python
if index == len(word):
    return True
```

  - **Success**: If `index` reaches the length of the word, it means we successfully found matches for `0` to `len-1`. We are done.

<!-- end list -->

```python
if (r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[index]):
    return False
```

  - **Failure**: This checks three things:
    1.  Are we off the grid?
    2.  Does the current cell NOT match the letter we are looking for (`word[index]`)?
    3.  Is the current cell marked as visited (`#`)? (Since `#` won't equal the target letter, this logic is covered by `!= word[index]`).

### Step 3: Marking and Exploring

```python
temp = board[r][c]
board[r][c] = "#"
```

  - We store the current letter in `temp` (e.g., 'A').
  - We overwrite the board with `#`. This prevents the subsequent recursive calls from coming back to this cell.

<!-- end list -->

```python
found = (backtrack(r + 1, c, index + 1) or ...)
```

  - We recursively call the function for all 4 neighbors. Note that we increment `index` to `index + 1` because we are now looking for the *next* letter in the word.
  - The `or` operator is efficient (short-circuiting). If the `Down` path returns `True`, it stops checking the others and returns `True` immediately.

### Step 4: Backtracking (The Cleanup)

```python
board[r][c] = temp
return found
```

  - **Crucial Step**: Before we return to the previous caller, we *must* restore the board to its original state. If we don't, the `#` will remain, and future searches starting from different locations might fail because they think this cell is blocked.

## Step-by-Step Execution Trace

Let's trace a scenario where we have to backtrack.
**Board**:

```
A B
C D
```

**Word**: `"ABDC"`

1.  **Start at (0,0) 'A'**: Matches `word[0]`. Mark `(0,0)` as `#`.
      * **Look neighbors for 'B'**:
          * Right `(0,1)` is 'B'. Match\! Mark `(0,1)` as `#`.
              * **Look neighbors for 'D'**:
                  * Down `(1,1)` is 'D'. Match\! Mark `(1,1)` as `#`.
                      * **Look neighbors for 'C'**:
                          * Left `(1,0)` is 'C'. Match\! Mark `(1,0)` as `#`.
                              * **Look neighbors for next char**: Index == Len. **Success\!**
                              * Return `True`.
                          * (Backtrack): Unmark `(1,0)` to 'C'.
                      * Return `True`.
                  * (Backtrack): Unmark `(1,1)` to 'D'.
              * Return `True`.
          * (Backtrack): Unmark `(0,1)` to 'B'.
      * Return `True`.

Now consider a failing path. **Word**: `"ABE"`

1.  **Start at (0,0) 'A'**. Mark `#`.
      * **Go Right to (0,1) 'B'**. Mark `#`.
          * **Look for 'E'**:
              * Up: Out of bounds.
              * Down: 'D' \!= 'E'.
              * Right: Out of bounds.
              * Left: '\#' (visited).
              * **Result**: False.
          * **Backtrack**: Unmark `(0,1)` back to 'B'.
      * **Go Down to (1,0) 'C'**. 'C' \!= 'B'. False.
      * **Result**: False.
      * **Backtrack**: Unmark `(0,0)` back to 'A'.
2.  Return `False`.

## Performance Analysis

### Time Complexity: O(N \* 3^L)

  - `N`: Total number of cells in the board.
  - `L`: Length of the word.
  - **Logic**: We iterate through every cell (`N`). For each cell, we start a DFS. In the DFS, we can go in 4 directions, but we immediately subtract 1 direction (where we came from), leaving at most 3 choices at each step. The depth of the recursion is `L`.
  - This gives roughly `N * 3^L`. This is loose, but indicates it's exponential with respect to the word length.

### Space Complexity: O(L)

  - The space is dominated by the recursion stack.
  - In the worst case, the recursion goes as deep as the length of the word (`L`).
  - Since we modify the board in-place, we don't use extra space for a `visited` array.