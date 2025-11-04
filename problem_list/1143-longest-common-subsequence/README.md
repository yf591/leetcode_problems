# 1143\. Longest Common Subsequence - Solution Explanation

## Problem Overview

You are given two strings, `text1` and `text2`. The task is to find the length of their **longest common subsequence (LCS)**.

**Key Definitions:**

  - **Subsequence**: A new string generated from an original string by deleting *some* (or no) characters, *without changing the relative order* of the remaining characters.
      - Example: `"ace"` is a subsequence of `"abcde"`. We deleted 'b' and 'd'.
  - **Common Subsequence**: A subsequence that is common to *both* strings.
      - Example: For `text1 = "abc"` and `text2 = "ac"`, the LCS is `"ac"`, with length 2.
  - **The Goal**: Return the *length* of the LCS, not the string itself.

**Examples:**

```python
Input: text1 = "abcde", text2 = "ace" 
Output: 3  
Explanation: The longest common subsequence is "ace", and its length is 3.

Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no common subsequence, so the result is 0.
```

## Deep Dive: What is Dynamic Programming (DP)? 🧠

Before we solve the problem, let's understand the core technique.

**Dynamic Programming (DP)** is a powerful algorithmic technique for solving complex problems by breaking them down into simpler, **overlapping subproblems**.

Think of it as building a solution from the ground up, solving the smallest possible versions of the problem first, and then using those answers to solve slightly larger versions, until you have solved the main problem.

It relies on two main properties:

1.  **Overlapping Subproblems**: The problem can be broken down into subproblems that are reused multiple times. For example, to find the LCS of `"abcde"` and `"ace"`, you will at some point need the LCS of `"abcd"` and `"ac"`. You'll also need this *same* answer when you're solving other subproblems. Instead of re-calculating it, DP says we should **store this answer** and look it up later.
2.  **Optimal Substructure**: The optimal solution to the main problem can be constructed from the optimal solutions to its subproblems.

**How we use it here:**
We will create a 2D "memoization" table (a grid) where `dp[i][j]` will store the answer to a very specific subproblem: "What is the length of the LCS for `text1` up to its `i`-th character and `text2` up to its `j`-th character?"

By solving this for `(0, 0)`, then `(0, 1)`, etc., we can build our way up to the final answer for `(len(text1), len(text2))`, which will be in the bottom-right corner of our table.

## Key Insights: The Recurrence Relation

To fill our DP table, we need a rule. This rule is called a **recurrence relation**. Let's figure it out by considering the characters at `text1[i]` and `text2[j]`.

### Case 1: The characters match.

  - Example: `text1 = "abc"` and `text2 = "aec"`. We are comparing the last characters, `'c'` and `'c'`.
  - Since they match, we *know* this character (`'c'`) is part of our LCS.
  - The length of the LCS is therefore **1** (for the `'c'`) **+** (the LCS of the strings *before* it, which are `"ab"` and `"ae"`).
  - **Formula**: `dp[i][j] = 1 + dp[i - 1][j - 1]`

### Case 2: The characters do *not* match.

  - Example: `text1 = "ab"` and `text2 = "ae"`. We are comparing `'b'` and `'e'`.
  - Since they don't match, the LCS must be made from a smaller subproblem. We have two choices:
    1.  Maybe the LCS is the same as the LCS of `"a"` and `"ae"` (we "ignore" the `'b'`).
    2.  Maybe the LCS is the same as the LCS of `"ab"` and `"a"` (we "ignore" the `'e'`).
  - We want the *longest* common subsequence, so we just take the **maximum** of these two possibilities.
  - **Formula**: `dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])`

These two rules are the *only* logic we need to fill the entire table.

## Solution Approach

This solution implements the bottom-up 2D Dynamic Programming approach. It creates a grid of size `(m+1) x (n+1)` to handle the empty string base cases, then fills the grid using the recurrence relation.

```python
from typing import List

class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        
        m, n = len(text1), len(text2)
        
        # Step 1: Create a DP table of size (m+1) x (n+1).
        # We add 1 to the dimensions to create a "dummy" first row and column.
        # This row/col of 0s acts as our base case (LCS of "" with any string is 0),
        # which simplifies our logic.
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Step 2: Iterate through the grid, starting from index 1.
        # i corresponds to characters in text1
        for i in range(1, m + 1):
            # j corresponds to characters in text2
            for j in range(1, n + 1):
                
                # --- This is the most important part ---
                # We use i-1 and j-1 because our dp table is 1-indexed (due to the
                # dummy row/col), but our strings are 0-indexed.
                # So, dp[i][j] corresponds to text1[i-1] and text2[j-1].
                
                # Case 1: The characters at these positions match.
                if text1[i - 1] == text2[j - 1]:
                    # The LCS is 1 (for this char) + the LCS of the strings
                    # before this char (which is at dp[i-1][j-1]).
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    # Case 2: The characters do not match.
                    # The LCS is the best we can get by either
                    # (A) ignoring the char from text1 (dp[i-1][j])
                    # (B) or ignoring the char from text2 (dp[i][j-1]).
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                                   
        # Step 3: The final answer is in the bottom-right corner.
        return dp[m][n]
```

## Detailed Code Analysis

### Step 1: The DP Table

```python
m, n = len(text1), len(text2)
dp = [[0] * (n + 1) for _ in range(m + 1)]
```

  - We create a 2D list (a grid) filled with `0`s.
  - If `m=5` and `n=3`, we create a `6x4` grid.
  - `dp[i][j]` will store the LCS of `text1[0...i-1]` and `text2[0...j-1]`.
  - This means `dp[0][0]` is the LCS of `""` and `""` (which is 0). `dp[0][j]` (the first row) and `dp[i][0]` (the first column) will all remain `0`, which is our base case.

### Step 2: The Loops

```python
for i in range(1, m + 1):
    for j in range(1, n + 1):
```

  - We start our loops at `1` (not `0`) because the 0-th row and 0-th column are our base cases and are already correctly filled with zeros.
  - The outer loop `i` iterates through each character of `text1`.
  - The inner loop `j` iterates through each character of `text2`.

### Step 3: The `if/else` Logic

```python
if text1[i - 1] == text2[j - 1]:
    dp[i][j] = 1 + dp[i - 1][j - 1]
else:
    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
```

  - **`text1[i - 1] == text2[j - 1]`**: This is the check for **Case 1 (Match)**. We use `i-1` and `j-1` to get the correct characters from the 0-indexed strings.
      - `dp[i-1][j-1]` is the result from the subproblem *diagonally* above and to the left, which represents the LCS *before* these matching characters.
  - **`else:`**: This is **Case 2 (No Match)**.
      - `dp[i - 1][j]`: The result from the cell directly **above**. (This is the LCS if we ignore the `text1` character).
      - `dp[i][j - 1]`: The result from the cell directly to the **left**. (This is the LCS if we ignore the `text2` character).
      - `max(...)` takes the better of these two options.

### Step 4: The Final Result

```python
return dp[m][n]
```

  - After the loops complete, the cell at `dp[m][n]` (the very bottom-right) holds the solution for the full strings, `LCS(text1[0...m-1], text2[0...n-1])`.

## Step-by-Step Execution Trace

Let's trace `text1 = "ace"` and `text2 = "abc"` with extreme detail.

  - `m = 3`, `n = 3`. We create a `4x4` grid.

**Initial `dp` table:**

```
  j=0 "" | j=1 "a" | j=2 "b" | j=3 "c"
----------------------------------------
i=0 "" |  0  |   0   |   0   |   0
i=1 "a"|  0  |   0   |   0   |   0
i=2 "c"|  0  |   0   |   0   |   0
i=3 "e"|  0  |   0   |   0   |   0
```

-----

**Filling `i = 1` (row "a")**

  - `dp[1][1]` (`a` vs `a`): Match\! `1 + dp[0][0]` -\> `1 + 0 = 1`.
  - `dp[1][2]` (`a` vs `b`): No match. `max(dp[0][2], dp[1][1])` -\> `max(0, 1) = 1`.
  - `dp[1][3]` (`a` vs `c`): No match. `max(dp[0][3], dp[1][2])` -\> `max(0, 1) = 1`.

**`dp` table after row 1:**

```
  ""| "a" | "b" | "c"
---------------------
""| 0 |  0  |  0  |  0
"a"| 0 |  1  |  1  |  1
"c"| 0 |  0  |  0  |  0
"e"| 0 |  0  |  0  |  0
```

-----

**Filling `i = 2` (row "c")**

  - `dp[2][1]` (`c` vs `a`): No match. `max(dp[1][1], dp[2][0])` -\> `max(1, 0) = 1`.
  - `dp[2][2]` (`c` vs `b`): No match. `max(dp[1][2], dp[2][1])` -\> `max(1, 1) = 1`.
  - `dp[2][3]` (`c` vs `c`): Match\! `1 + dp[1][2]` -\> `1 + 1 = 2`.

**`dp` table after row 2:**

```
  ""| "a" | "b" | "c"
---------------------
""| 0 |  0  |  0  |  0
"a"| 0 |  1  |  1  |  1
"c"| 0 |  1  |  1  |  2
"e"| 0 |  0  |  0  |  0
```

-----

**Filling `i = 3` (row "e")**

  - `dp[3][1]` (`e` vs `a`): No match. `max(dp[2][1], dp[3][0])` -\> `max(1, 0) = 1`.
  - `dp[3][2]` (`e` vs `b`): No match. `max(dp[2][2], dp[3][1])` -\> `max(1, 1) = 1`.
  - `dp[3][3]` (`e` vs `c`): No match. `max(dp[2][3], dp[3][2])` -\> `max(2, 1) = 2`.

**Final `dp` table:**

```
  ""| "a" | "b" | "c"
---------------------
""| 0 |  0  |  0  |  0
"a"| 0 |  1  |  1  |  1
"c"| 0 |  1  |  1  |  2
"e"| 0 |  1  |  1  |  2
```

-----

### **Final Result:**

  - The loop finishes.
  - The function returns `dp[m][n]`, which is `dp[3][3]`.
  - The value is **2**. (The LCS of "ace" and "abc" is "ac").

## Performance Analysis

### Time Complexity: O(m \* n)

  - Where `m` and `n` are the lengths of the two strings.
  - We must fill every cell in an `(m+1) x (n+1)` grid.
  - The work to fill each cell is `O(1)` (a simple comparison, addition, or `max` operation).
  - Therefore, the total time is proportional to the size of the grid.

### Space Complexity: O(m \* n)

  - The space complexity is determined by the `dp` table. We need to store `(m+1) * (n+1)` values, which simplifies to `O(m * n)`.
  - *(Advanced Note: This can be optimized to `O(min(m, n))` space, because calculating the current row only requires values from the previous row, not the entire table.)*