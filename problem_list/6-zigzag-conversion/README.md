# 6\. Zigzag Conversion - Solution Explanation

## Problem Overview

You are given a string `s` and an integer `numRows`. The task is to write the string's characters in a zigzag pattern across a specified number of rows and then read the string back out, row by row.

**The Zigzag Pattern:**
The characters are written top-to-bottom, then diagonally up-to-right, then top-to-bottom again, and so on.

**Example (`s = "PAYPALISHIRING"`, `numRows = 4`):**

```
P     I    N
A   L S  I G
Y A   H R
P     I
```

**Reading it back row by row gives:** `"PINALSIGYAHRPI"`

## Key Insights

### Simulating the Path

The most direct way to solve this is to **simulate** the path of the character being written. We don't need a complex mathematical formula to figure out where each character goes. Instead, we can create a data structure to represent our rows and then simply iterate through the input string, placing each character into the correct row, just like you would by hand.

### Tracking the State

To simulate the zigzag movement, we only need to keep track of two things:

1.  **`current_row`**: Which row (from `0` to `numRows - 1`) are we currently writing on?
2.  **`direction`**: Are we currently moving down the grid or diagonally up? We can represent this with a number, for example, `1` for down and `-1` for up.

The direction will flip every time we hit the top row (`row 0`) or the bottom row (`row numRows - 1`).

## Solution Approach

This solution creates a list of strings, one for each row. It then iterates through the input string `s` one character at a time, appending each character to the correct row by tracking the current row and the direction of movement.

```python
from typing import List

class Solution:
    def convert(self, s: str, numRows: int) -> str:
        # Edge Case: If there's only one row, or enough rows for every character,
        # the zigzag pattern is just the string itself.
        if numRows == 1 or numRows >= len(s):
            return s
            
        # Create a list to hold the string for each row.
        rows = [''] * numRows
        
        current_row = 0
        direction = 1 # 1 means moving down, -1 means moving up.
        
        # Iterate through the string character by character.
        for char in s:
            # Append the character to the string for the current row.
            rows[current_row] += char
            
            # Check if we've hit the top or bottom boundary to reverse direction.
            if current_row == 0:
                direction = 1
            elif current_row == numRows - 1:
                direction = -1
            
            # Move to the next row according to the current direction.
            current_row += direction
            
        # Join all the row strings together to get the final result.
        return "".join(rows)
```

## Detailed Code Analysis

### Step 1: The Edge Case

```python
if numRows == 1 or numRows >= len(s):
    return s
```

  - This handles a simple case first. If `numRows` is 1, there is no zigzag, just a single horizontal line. If there are more rows than characters, each character gets its own row, and reading it line by line just gives the original string back.

### Step 2: Initialization

```python
rows = [''] * numRows
current_row = 0
direction = 1
```

  - `rows = [''] * numRows`: We create a list of `numRows` empty strings. Each string in this list will be built up to become one of the final rows in our zigzag pattern.
  - `current_row = 0`: Our "pen" starts at the very first row (index 0).
  - `direction = 1`: We initialize our direction to `1`, which will mean we are moving downwards.

### Step 3: The Main Loop

```python
for char in s:
```

  - This loop iterates through every single character in the input string `s`.

### Step 4: Placing the Character

```python
rows[current_row] += char
```

  - This is where we "write" the character. We append the current `char` to the string located at the `current_row` index in our `rows` list.

### Step 5: The Direction Flip Logic

```python
if current_row == 0:
    direction = 1
elif current_row == numRows - 1:
    direction = -1
```

  - This is the core of the zigzag logic. It checks if our "pen" has hit a boundary.
  - **`if current_row == 0:`**: If we have just written to the top row, we know our next move must be downwards. We set `direction` to `1`.
  - **`elif current_row == numRows - 1:`**: If we have just written to the bottom row, we know our next move must be upwards. We set `direction` to `-1`.

### Step 6: Moving to the Next Row

```python
current_row += direction
```

  - After placing the character and determining the *next* direction, we update our `current_row` by adding the `direction` (either `1` or `-1`).

### Step 7: Final String Construction

```python
return "".join(rows)
```

  - After the `for` loop has processed all characters, our `rows` list contains the complete, separated lines of the zigzag pattern.
  - `"".join(rows)` is an efficient Python method that concatenates all the strings in the `rows` list into a single final string.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `s = "PAYPAL"` and `numRows = 3` with extreme detail.

1.  **Initialization**: `rows = ['', '', '']`, `current_row = 0`, `direction = 1`.

| `char` | `current_row` (before append) | `rows` (after append) | `direction` (after check) | `current_row` (after update) |
| :--- | :--- | :--- | :--- | :--- |
| **Start**| 0 | `['', '', '']` | 1 | 0 |
| **'P'** | 0 | `['P', '', '']` | 1 | `0 + 1 = 1` |
| **'A'** | 1 | `['P', 'A', '']` | 1 | `1 + 1 = 2` |
| **'Y'** | 2 | `['P', 'A', 'Y']` | **-1** (hit bottom) | `2 + (-1) = 1` |
| **'P'** | 1 | `['P', 'AP', 'Y']` | -1 | `1 + (-1) = 0` |
| **'A'** | 0 | `['PA', 'AP', 'Y']` | **1** (hit top) | `0 + 1 = 1` |
| **'L'** | 1 | `['PA', 'APL', 'Y']`| 1 | `1 + 1 = 2` |

2.  **End of Loop**: The `for` loop finishes.
3.  **Final `rows` state**: `['PA', 'APL', 'Y']`
4.  **Return**: `"".join(['PA', 'APL', 'Y'])` -\> **`"PAAPLY"`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the length of the string `s`. We iterate through the string exactly once.

### Space Complexity: O(n)

  - The space required is to store the `rows` list. In the end, this list will contain all `n` characters from the original string.