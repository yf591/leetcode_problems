# 72\. Edit Distance - Solution Explanation

## Problem Overview

You are given two strings, `word1` and `word2`. The task is to find the **minimum number of operations** required to convert `word1` into `word2`.

You are allowed to perform exactly three types of operations:

1.  **Insert** a character.
2.  **Delete** a character.
3.  **Replace** a character.

**Example:**

```python
Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation:
1. horse -> rorse (replace 'h' with 'r')
2. rorse -> rose (delete 'r')
3. rose -> ros (delete 'e')
```

## Deep Dive: What is DP - Multidimensional? 🧠

**Dynamic Programming (DP)** is a technique for solving complex problems by breaking them down into simpler, **overlapping subproblems**.

  - **1D DP (like House Robber):** The solution for a problem at step `i` (e.g., `dp[i]`) depends only on previous steps in one dimension, like `dp[i-1]` or `dp[i-2]`. The subproblem is "what's the best answer for the first `i` items?"

  - **Multidimensional (2D) DP (like this problem):** This is used when the state of the problem depends on **two or more variables**.

      - In this problem, a subproblem isn't just "how to convert the first `i` chars of `word1`?" It's "how to convert the first `i` chars of `word1` *into* the first `j` chars of `word2`?"
      - This subproblem, `dp[i][j]`, naturally maps to a **2D grid** (a table or matrix). Each cell in this grid stores the answer to a smaller, specific subproblem. We fill this grid from the simplest subproblems (like converting an empty string) up to the main problem we want to solve.

## Key Insights: The Recurrence Relation

This is the heart of the algorithm. We will build a 2D DP table, `dp[i][j]`, which will store the minimum edit distance between the first `i` characters of `word1` and the first `j` characters of `word2`.

To calculate the value for `dp[i][j]`, we look at the characters `word1[i-1]` and `word2[j-1]` (we use `i-1` and `j-1` because strings are 0-indexed, but our DP table will be 1-indexed to help with base cases).

### Case 1: The characters match (`word1[i-1] == word2[j-1]`)

  - **Example**: Converting "app**l**" to "ape**l**". The last characters match.
  - This is the "free" move. No operation is needed for these characters.
  - The cost to convert `"appl"` to `"apel"` is the same as the cost to convert `"app"` to `"ape"`.
  - **Formula**: `dp[i][j] = dp[i-1][j-1]` (cost is the same as the subproblem diagonally to the top-left).

### Case 2: The characters do *not* match

  - **Example**: Converting "ho**r**" to "ro**s**". The characters `'r'` and `'s'` do not match.

  - We *must* perform one operation. We have three choices, and we will pick the one that results in the **minimum** total cost.

    1.  **Insert**: We can insert `'s'` into `word1` to make it "hors". Now we just need to convert `"hor"` to `"ro"`.
          - **Cost**: `1` (for the insertion) + `dp[i][j-1]` (cost from the cell to the **left**).
    2.  **Delete**: We can delete `'r'` from `"hor"`. Now we need to convert `"ho"` to `"ros"`.
          - **Cost**: `1` (for the deletion) + `dp[i-1][j]` (cost from the cell **above**).
    3.  **Replace**: We can replace `'r'` in `"hor"` with `'s'`. Now we need to convert `"ho"` to `"ro"`.
          - **Cost**: `1` (for the replacement) + `dp[i-1][j-1]` (cost from the cell **diagonally**).

  - **Formula**: `dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])`

### Base Cases (The "Gutter" Row and Column)

  - `dp[0][j]`: The cost to convert an empty string `""` to the first `j` characters of `word2`. This requires `j` insertions. So, `dp[0][j] = j`.
  - `dp[i][0]`: The cost to convert the first `i` characters of `word1` to an empty string `""`. This requires `i` deletions. So, `dp[i][0] = i`.
  - `dp[0][0] = 0` (cost to convert `""` to `""` is 0).

## Solution Approach

This solution implements the bottom-up 2D DP. It first creates the `(m+1) x (n+1)` grid, initializes the base cases in the 0-th row and 0-th column, and then fills the rest of the grid using the two-case recurrence relation. The final answer is the value in the bottom-right cell.

```python
from typing import List

class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        
        m = len(word1)
        n = len(word2)
        
        # Step 1: Create a DP table of size (m+1) x (n+1).
        # We add 1 to the dimensions to hold the base cases for empty strings.
        # dp[i][j] = min cost to convert word1[0...i-1] to word2[0...j-1]
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # --- Step 2: Initialize Base Cases ---
        
        # Base Case (Row 0): Cost to convert "" to word2[0...j-1]
        # This requires 'j' insertions.
        for j in range(n + 1):
            dp[0][j] = j
            
        # Base Case (Column 0): Cost to convert word1[0...i-1] to ""
        # This requires 'i' deletions.
        for i in range(m + 1):
            dp[i][0] = i
            
        # --- Step 3: Fill the rest of the DP table ---
        
        # Iterate from i=1 (first char of word1)
        for i in range(1, m + 1):
            # Iterate from j=1 (first char of word2)
            for j in range(1, n + 1):
                
                # We use i-1 and j-1 because strings are 0-indexed.
                char1 = word1[i - 1]
                char2 = word2[j - 1]
                
                if char1 == char2:
                    # Case 1: Characters match. No cost.
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # Case 2: Characters don't match. Find the min cost of 3 operations.
                    insert_cost = dp[i][j - 1]   # Cost of "inserting" char2
                    delete_cost = dp[i - 1][j]   # Cost of "deleting" char1
                    replace_cost = dp[i - 1][j - 1] # Cost of "replacing" char1 with char2
                    
                    dp[i][j] = 1 + min(insert_cost, delete_cost, replace_cost)
                    
        # The final answer is in the bottom-right corner.
        return dp[m][n]
```

## Step-by-Step Execution Trace

Let's trace the algorithm with `word1 = "ros"` and `word2 = "horse"` with extreme detail.
(Note: I'm swapping the example to show all 3 operations clearly, finding cost to convert "ros" to "horse").

  - `m = 3` (`ros`), `n = 5` (`horse`). We create a `4 x 6` grid.

### **Step 1 & 2: Base Case Initialization**

The grid is filled with the cost to convert to/from an empty string.

```
  j=0 "" | j=1 "h" | j=2 "o" | j=3 "r" | j=4 "s" | j=5 "e"
------------------------------------------------------------
i=0 "" |  0  |   1   |   2   |   3   |   4   |   5
i=1 "r"|  1  |   0   |   0   |   0   |   0   |   0
i=2 "o"|  2  |   0   |   0   |   0   |   0   |   0
i=3 "s"|  3  |   0   |   0   |   0   |   0   |   0
```

-----

### **Step 3: Fill the DP Table (Row by Row)**

**Filling `i = 1` (char 'r')**

  - `dp[1][1]` ('r' vs 'h'): No match. `1 + min(dp[0][1], dp[1][0], dp[0][0])` -\> `1 + min(1, 1, 0) = 1` (Replace)
  - `dp[1][2]` ('r' vs 'o'): No match. `1 + min(dp[0][2], dp[1][1], dp[0][1])` -\> `1 + min(2, 1, 1) = 2`
  - `dp[1][3]` ('r' vs 'r'): **Match\!** `dp[0][2]` -\> `2`.
  - `dp[1][4]` ('r' vs 's'): No match. `1 + min(dp[0][4], dp[1][3], dp[0][3])` -\> `1 + min(4, 2, 3) = 3`
  - `dp[1][5]` ('r' vs 'e'): No match. `1 + min(dp[0][5], dp[1][4], dp[0][4])` -\> `1 + min(5, 3, 4) = 4`

**Table after `i=1`:**

```
  ""| "h" | "o" | "r" | "s" | "e"
-----------------------------------
""| 0 |  1  |  2  |  3  |  4  |  5
"r"| 1 |  1  |  2  |  2  |  3  |  4
"o"| 2 |  0  |  0  |  0  |  0  |  0
"s"| 3 |  0  |  0  |  0  |  0  |  0
```

-----

**Filling `i = 2` (char 'o')**

  - `dp[2][1]` ('o' vs 'h'): No match. `1 + min(dp[1][1], dp[2][0], dp[1][0])` -\> `1 + min(1, 2, 1) = 2`
  - `dp[2][2]` ('o' vs 'o'): **Match\!** `dp[1][1]` -\> `1`.
  - `dp[2][3]` ('o' vs 'r'): No match. `1 + min(dp[1][3], dp[2][2], dp[1][2])` -\> `1 + min(2, 1, 2) = 2`
  - `dp[2][4]` ('o' vs 's'): No match. `1 + min(dp[1][4], dp[2][3], dp[1][3])` -\> `1 + min(3, 2, 2) = 3`
  - `dp[2][5]` ('o' vs 'e'): No match. `1 + min(dp[1][5], dp[2][4], dp[1][4])` -\> `1 + min(4, 3, 3) = 4`

**Table after `i=2`:**

```
  ""| "h" | "o" | "r" | "s" | "e"
-----------------------------------
""| 0 |  1  |  2  |  3  |  4  |  5
"r"| 1 |  1  |  2  |  2  |  3  |  4
"o"| 2 |  2  |  1  |  2  |  3  |  4
"s"| 3 |  0  |  0  |  0  |  0  |  0
```

-----

**Filling `i = 3` (char 's')**

  - `dp[3][1]` ('s' vs 'h'): No match. `1 + min(dp[2][1], dp[3][0], dp[2][0])` -\> `1 + min(2, 3, 2) = 3`
  - `dp[3][2]` ('s' vs 'o'): No match. `1 + min(dp[2][2], dp[3][1], dp[2][1])` -\> `1 + min(1, 3, 2) = 2`
  - `dp[3][3]` ('s' vs 'r'): No match. `1 + min(dp[2][3], dp[3][2], dp[2][2])` -\> `1 + min(2, 2, 1) = 2`
  - `dp[3][4]` ('s' vs 's'): **Match\!** `dp[2][3]` -\> `2`.
  - `dp[3][5]` ('s' vs 'e'): No match. `1 + min(dp[2][5], dp[3][4], dp[2][4])` -\> `1 + min(4, 2, 3) = 3`

**Final `dp` table:**

```
  ""| "h" | "o" | "r" | "s" | "e"
-----------------------------------
""| 0 |  1  |  2  |  3  |  4  |  5
"r"| 1 |  1  |  2  |  2  |  3  |  4
"o"| 2 |  2  |  1  |  2  |  3  |  4
"s"| 3 |  3  |  2  |  2  |  2  |  3
```

-----

### **Final Result:**

  - The loop finishes.
  - The function returns `dp[m][n]`, which is `dp[3][5]`.
  - The value is **3**.

(This matches the example: `ros` -\> `rose` (insert 'e') -\> `rorse` (insert 'r') -\> `horse` (replace 's' with 'h'). Wait, that's not right. Let's trace the example `horse` -\> `ros`.
`horse` (del 'e') -\> `hors`
`hors` (del 'r') -\> `hos`
`hos` (rep 'h' with 'r') -\> `ros`
Total cost: 3. The algorithm is correct, my manual trace was just one of many paths.)

## Performance Analysis

### Time Complexity: O(m \* n)

  - Where `m` and `n` are the lengths of `word1` and `word2`.
  - We must fill every cell in an `(m+1) x (n+1)` grid.
  - The work to fill each cell is `O(1)` (a simple comparison, addition, or `min` operation).
  - Therefore, the total time is proportional to the size of the grid.

### Space Complexity: O(m \* n)

  - The space complexity is determined by the `dp` table. We need to store `(m+1) * (n+1)` values, which simplifies to `O(m * n)`.
  - *(Advanced Note: This can be optimized to `O(min(m, n))` space, because calculating the current row only requires values from the previous row, not the entire table.)*