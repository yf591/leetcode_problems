# 36\. Valid Sudoku - Solution Explanation

## Problem Overview

Determine if a 9x9 Sudoku board is valid according to three rules, validating only the filled cells.

**Validity Rules:**

1.  Each **row** must contain the digits 1-9 without repetition.
2.  Each **column** must contain the digits 1-9 without repetition.
3.  Each of the nine **3x3 sub-boxes** must contain the digits 1-9 without repetition.

**Examples:**

  - A valid board passes all three checks for all filled cells.
  - An invalid board fails at least one check (e.g., has a duplicate '8' in a single row, column, or 3x3 box).

## Key Insights

### Efficient Duplicate Checking with Hash Sets

The core of this problem is checking for duplicates across three different dimensions (rows, columns, and boxes). The most efficient data structure for tracking "seen" items is a **hash set**. Hash sets provide O(1) average time complexity for both adding an element and checking if an element already exists, making them perfect for this task.

Our strategy will be to make a single pass over the board, using hash sets to keep track of the numbers we've seen in every row, column, and box.

## Solution Approach

This solution iterates through the board once, using dictionaries of sets to record the numbers encountered.

```python
import collections

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = collections.defaultdict(set)
        cols = collections.defaultdict(set)
        boxes = collections.defaultdict(set)

        for r in range(9):
            for c in range(9):
                val = board[r][c]

                if val == '.':
                    continue

                box_key = (r // 3, c // 3)
                
                if (val in rows[r] or
                    val in cols[c] or
                    val in boxes[box_key]):
                    return False
                
                rows[r].add(val)
                cols[c].add(val)
                boxes[box_key].add(val)
        
        return True
```

**Strategy:**

1.  **Initialize Records**: Create three hash maps (`rows`, `cols`, `boxes`) to store sets of seen numbers.
2.  **Single Pass**: Traverse every cell of the board from top-left to bottom-right.
3.  **Check & Add**: For each number, check if it's already in the records for its current row, column, and box. If not, add it. If it is, a rule has been broken.
4.  **Immediate Return**: If a duplicate is found at any point, the board is invalid, so we return `False` immediately.
5.  **Success**: If the loops complete, no duplicates were found, and we return `True`.

## Detailed Code Analysis

### Step 1: Data Structure Initialization

```python
rows = collections.defaultdict(set)
cols = collections.defaultdict(set)
boxes = collections.defaultdict(set)
```

  - We use `collections.defaultdict(set)` for convenience. This creates a dictionary where if a key is accessed for the first time, it's automatically initialized with an empty `set`. This saves us from writing extra code to check if a set for a given row/col/box already exists.

### Step 2: Board Traversal

```python
for r in range(9):
    for c in range(9):
        # ...
```

  - A standard nested loop allows us to visit every cell `(r, c)` once.

### Step 3: Checking for Duplicates

```python
box_key = (r // 3, c // 3)
if (val in rows[r] or val in cols[c] or val in boxes[box_key]):
    return False
```

  - This is the core validation logic. For each value, we perform three O(1) (average time) lookups in our hash sets.
  - The `box_key` calculation `(r // 3, c // 3)` is a clever trick to get a unique identifier for each of the nine 3x3 boxes.

### Step 4: Recording the Number

```python
rows[r].add(val)
cols[c].add(val)
boxes[box_key].add(val)
```

  - If the number is not a duplicate, we add it to the sets for its corresponding row, column, and box so we can check against it for future cells.

## Step-by-Step Execution Trace

### Example: A portion of the invalid board

Let's say `board[0][0] = '8'` and `board[2][2] = '8'`.

| `(r, c)` | `val` | `box_key` | Action | `boxes[(0,0)]` State |
| :--- | :--- | :--- | :--- | :--- |
| (0, 0) | '8' | (0, 0) | `val` is not in sets. Add '8' to `rows[0]`, `cols[0]`, `boxes[(0,0)]`. | `{ '8' }` |
| ... | ... | ... | ... (other cells are processed) | ... |
| (2, 2) | '8' | (0, 0) | Check `if '8' in boxes[(0,0)]`. This is **True**. | `{ '8', ... }` |

  - When the code reaches cell `(2, 2)`, it calculates the `box_key` as `(2 // 3, 2 // 3)`, which is `(0, 0)`.
  - It checks if the value `'8'` is already in the set for `boxes[(0, 0)]`.
  - It finds `'8'` (which was added from cell `(0, 0)`) and immediately returns `False`.

## Performance Analysis

### Time Complexity: O(1)

  - The size of the Sudoku board is fixed at 9x9. The algorithm iterates through a constant 81 cells, and each operation inside the loop (set lookup and insertion) is O(1) on average. Therefore, the overall time complexity is constant. For a general N x N board, it would be O(N^2).

### Space Complexity: O(1)

  - We use three dictionaries to store the seen numbers. In the worst case (a full board), they store 9 sets each, with up to 9 numbers per set. The space required is constant and does not depend on the input. For a general N x N board, it would be O(N^2).

## Why the Box Indexing Matters

The expression `box_key = (r // 3, c // 3)` is the most elegant part of the solution.

  - Integer division `//` maps row indices `0, 1, 2` to `0`; `3, 4, 5` to `1`; and `6, 7, 8` to `2`.
  - It does the same for the column indices.
  - This creates a unique `(row_group, col_group)` tuple for each of the nine 3x3 boxes, allowing us to use a single hash map to track all of them.

## Key Learning Points

  - Using hash sets is a highly efficient method for duplicate detection.
  - A single pass over a data structure is often sufficient to validate multiple constraints simultaneously.
  - Simple mathematical tricks (like integer division) can be used to map 2D coordinates into distinct groups.