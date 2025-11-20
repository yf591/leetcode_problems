# 22\. Generate Parentheses - Solution Explanation

## Problem Overview

Given an integer `n`, the task is to generate **all possible combinations** of well-formed parentheses using exactly `n` pairs.

**Well-formed** means every opening bracket `(` has a corresponding closing bracket `)`, and they are properly nested.

**Examples:**

```python
Input: n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]

Input: n = 1
Output: ["()"]
```

## Deep Dive: What is Backtracking? 🧠

**Backtracking** is an algorithmic technique for solving problems recursively by trying to build a solution incrementally, one piece at a time.

Think of it as exploring a **Decision Tree**.

1.  **Start**: You start with a blank slate (empty string).
2.  **The Choice**: At each step, you have options. Here, the options are adding `(` or adding `)`.
3.  **Constraints**: You can't just pick any option. You must follow rules to ensure the solution remains valid.
      - *Rule A*: You can't add more than `n` opening brackets total.
      - *Rule B*: You can't add a closing bracket unless there is an unmatched opening bracket waiting to be closed.
4.  **The "Backtrack"**: If you reach a valid solution, you save it. If you reach a state where no valid moves are possible, you "backtrack"—you return to the previous state and try a different option.

## Key Insights

### 1\. Brute Force vs. Backtracking

A brute-force approach would generate every possible string of length `2*n` (like `))((`, `())(`) and then check if they are valid. This is incredibly inefficient.

Backtracking is smarter. It **only builds valid prefixes**. By strictly following the constraints (rules A and B above), we ensure that we never waste time building a string that is already broken (like starting with `)`).

### 2\. The Two Counters

To make our decisions, we only need to track two numbers:

1.  **`open_count`**: How many `(` we have placed so far.
2.  **`close_count`**: How many `)` we have placed so far.

### 3\. The Decision Logic

At any point in the recursion, we have two potential decisions:

  - **Can we place `(`?** Yes, if `open_count < n`. (We still have opening brackets left to use).
  - **Can we place `)`?** Yes, if `close_count < open_count`. (We have an open bracket that needs closing).

## Solution Approach

This solution uses a recursive helper function `backtrack` that builds the string character by character. It passes the current state (`current_string`, `open_count`, `close_count`) down to the next step.

```python
from typing import List

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        # This list will hold all valid combinations found.
        result = []
        
        def backtrack(current_string, open_count, close_count):
            # --- Base Case: Success ---
            # If the string is the correct length (2 * n), it means we have
            # successfully used all n pairs. Add to result.
            if len(current_string) == n * 2:
                result.append(current_string)
                return

            # --- Decision 1: Add Open Bracket ---
            # We can add '(' if we haven't used all n of them yet.
            if open_count < n:
                backtrack(current_string + "(", open_count + 1, close_count)
            
            # --- Decision 2: Add Close Bracket ---
            # We can add ')' only if there are unclosed '(' available.
            # This ensures the string remains well-formed.
            if close_count < open_count:
                backtrack(current_string + ")", open_count, close_count + 1)

        # Start the recursion with an empty string and 0 counts.
        backtrack("", 0, 0)
        
        return result
```

## Detailed Code Analysis

### Step 1: Initialization

```python
result = []
```

  - We create a container `result` to store our valid strings. Since it's defined outside the inner function, the recursive calls can access and append to it (via closure).

### Step 2: The `backtrack` Function Signature

```python
def backtrack(current_string, open_count, close_count):
```

  - **`current_string`**: The string we have built *so far* in this branch of the recursion.
  - **`open_count`**: The integer count of how many `(` are in `current_string`.
  - **`close_count`**: The integer count of how many `)` are in `current_string`.

### Step 3: The Base Case

```python
if len(current_string) == n * 2:
    result.append(current_string)
    return
```

  - Since we need `n` pairs, the total length must be `2 * n`.
  - If our string reaches this length, we know it must be valid because our constraints prevented invalid moves along the way. We save it and `return` (stop this path).

### Step 4: Recursive Step - Opening

```python
if open_count < n:
    backtrack(current_string + "(", open_count + 1, close_count)
```

  - If `n=3` and we have only used 2 `(` so far, we are allowed to add another.
  - We call the function recursively. Notice we create a **new string** `current_string + "("` and increment the `open_count`.

### Step 5: Recursive Step - Closing

```python
if close_count < open_count:
    backtrack(current_string + ")", open_count, close_count + 1)
```

  - This is the logic that enforces validity. We can never close a bracket if there isn't an open one waiting.
  - For example, if we have `((` (`open=2`, `close=0`), `0 < 2` is true, so we can add `)`.
  - If we have `()` (`open=1`, `close=1`), `1 < 1` is false, so we **cannot** add another `)`.

## Step-by-Step Execution Trace

Let's trace the algorithm for **`n = 2`** with extreme detail.
Target length: 4.

1.  **`backtrack("", 0, 0)`**
      - `0 < 2` (open)? Yes. -\> Call `backtrack("(", 1, 0)`
      - **`backtrack("(", 1, 0)`**
          - `1 < 2` (open)? Yes. -\> Call `backtrack("((", 2, 0)`
          - **`backtrack("((", 2, 0)`**
              - `2 < 2` (open)? No.
              - `0 < 2` (close)? Yes. -\> Call `backtrack("(()", 2, 1)`
              - **`backtrack("(()", 2, 1)`**
                  - `2 < 2` (open)? No.
                  - `1 < 2` (close)? Yes. -\> Call `backtrack("(())", 2, 2)`
                  - **`backtrack("(())", 2, 2)`**
                      - Len is 4. **Add `"(())"` to result**. Return.
                  - Function returns.
              - Function returns.
          - Function returns.
          - (Back in `backtrack("(", 1, 0)`)
          - `0 < 1` (close)? Yes. -\> Call `backtrack("()", 1, 1)`
          - **`backtrack("()", 1, 1)`**
              - `1 < 2` (open)? Yes. -\> Call `backtrack("()(", 2, 1)`
              - **`backtrack("()(", 2, 1)`**
                  - `2 < 2` (open)? No.
                  - `1 < 2` (close)? Yes. -\> Call `backtrack("()()", 2, 2)`
                  - **`backtrack("()()", 2, 2)`**
                      - Len is 4. **Add `"()()"` to result**. Return.
                  - Function returns.
              - Function returns.
              - (Back in `backtrack("()", 1, 1)`)
              - `1 < 1` (close)? No.
          - Function returns.
      - (Back in `backtrack("", 0, 0)`)
      - `0 < 0` (close)? No.
      - Function returns.

**Final Result:** `["(())", "()()"]`

## Performance Analysis

### Time Complexity: O(4^n / √n)

  - This is a complex mathematical derivation related to the **Catalan numbers**.
  - The number of valid parenthesis strings of length `2n` is the n-th Catalan number, which grows roughly as `4^n / (n * sqrt(n))`.
  - Since we generate exactly these valid strings and do constant work for each step, the complexity follows the sequence of Catalan numbers.

### Space Complexity: O(n)

  - The space complexity is determined by the recursion stack depth.
  - We recurse until we build a string of length `2n`. Therefore, the maximum depth of the recursion is `2n`, which simplifies to `O(n)`.
  - (This does not count the space required to store the output list).