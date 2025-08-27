# 1768\. Merge Strings Alternately - Solution Explanation

## Problem Overview

You are given two strings, `word1` and `word2`. The goal is to merge them into a single new string by adding their letters in alternating order, starting with `word1`. If one string runs out of letters before the other, the remaining letters from the longer string should be appended to the end.

**Examples:**

```python
# Example 1: Same length
Input: word1 = "abc", word2 = "pqr"
Output: "apbqcr"
# a from word1, p from word2, b from word1, q from word2, ...

# Example 2: word2 is longer
Input: word1 = "ab", word2 = "pqrs"
Output: "apbqrs"
# a, p, b, q ... then append the rest of word2, which is "rs"

# Example 3: word1 is longer
Input: word1 = "abcd", word2 = "pq"
Output: "apbqcd"
# a, p, b, q ... then append the rest of word1, which is "cd"
```

## Key Insights

### Building a New String Efficiently

The task is to construct a new string. In Python, repeatedly adding to a string in a loop with the `+` operator can be inefficient because it creates a new string in memory with every operation. A much more efficient pattern is to append the characters to a **list** and then, at the very end, use the `"".join()` method to combine them into a single string.

### Handling Different Lengths

The main challenge is that the two strings can have different lengths. The merging process needs to continue until all characters from the **longer** string have been used. This means our loop must run a number of times equal to the length of the longer string. Inside the loop, we must be careful to only access characters from a string if our current index is still within its bounds.

## Solution Approach

This solution iterates a number of times equal to the length of the longer string. In each iteration, it conditionally appends a character from `word1` (if available) and a character from `word2` (if available) to a result list.

```python
from typing import List

class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        # A list to build our result string efficiently.
        result = []
        m, n = len(word1), len(word2)
        
        # We need to loop as many times as the length of the longer string.
        for i in range(max(m, n)):
            # If our index 'i' is still a valid index for word1,
            # append its character.
            if i < m:
                result.append(word1[i])
            
            # If our index 'i' is still a valid index for word2,
            # append its character.
            if i < n:
                result.append(word2[i])
                
        # Join all the characters in the list to form the final string.
        return "".join(result)
```

**Strategy:**

1.  **Initialize**: Create an empty list `result` to store the characters for the new string.
2.  **Loop**: Iterate with an index `i` from `0` up to the length of the longer string (`max(m, n)`).
3.  **Conditional Append**: Inside the loop, use an `if` statement to check if `i` is a valid index for `word1` before appending `word1[i]`. Do the same for `word2`.
4.  **Join**: After the loop has finished, combine the list of characters in `result` into the final string.

## Detailed Code Analysis

### Step 1: Initialization

```python
result = []
m, n = len(word1), len(word2)
```

  - We create an empty list `result`. This is our workspace for building the final string.
  - We store the lengths of `word1` and `word2` in `m` and `n` for easy access.

### Step 2: The Loop

```python
for i in range(max(m, n)):
```

  - This is the control structure for the entire process.
  - `max(m, n)` ensures the loop runs enough times to process every character from both strings, even if one is much longer than the other.
  - The variable `i` will take on values `0, 1, 2, ...` up to one less than the length of the longer string.

### Step 3: Conditional Appending

```python
if i < m:
    result.append(word1[i])
```

  - This is a crucial **boundary check**.
  - Python strings are 0-indexed. A string of length `m` has valid indices from `0` to `m-1`.
  - The condition `i < m` checks if the current loop index `i` is a valid index for `word1`. If it is, we can safely access `word1[i]` and append it to our `result`. If `i` is `m` or greater, this condition will be false, and we will skip the append, avoiding an `IndexError`.

<!-- end list -->

```python
if i < n:
    result.append(word2[i])
```

  - This performs the exact same boundary check for `word2`.

### Step 4: Final String Creation

```python
return "".join(result)
```

  - After the loop, `result` is a list of characters in the correct merged order.
  - `"".join(result)` is an efficient Python method that concatenates all the strings in the `result` list into a single new string, with an empty string (`""`) as the separator.

## Step-by-Step Execution Trace

### Example: `word1 = "ab"`, `word2 = "pqrs"`

1.  **Initialization**:

      * `result = []`
      * `m = 2`, `n = 4`
      * The loop will run for `i` in `range(max(2, 4))`, which is `range(4)`. So, `i` will be `0, 1, 2, 3`.

2.  **The Loop**:

| `i` | `i < m`? (i \< 2) | Action for `word1` | `i < n`? (i \< 4) | Action for `word2` | `result` state after loop |
| :-- | :--- | :--- | :--- | :--- | :--- |
| **0** | `0 < 2` -\> True | `result.append('a')` | `0 < 4` -\> True | `result.append('p')` | `['a', 'p']` |
| **1** | `1 < 2` -\> True | `result.append('b')` | `1 < 4` -\> True | `result.append('q')` | `['a', 'p', 'b', 'q']` |
| **2** | `2 < 2` -\> **False** | (nothing) | `2 < 4` -\> True | `result.append('r')` | `['a', 'p', 'b', 'q', 'r']` |
| **3** | `3 < 2` -\> **False** | (nothing) | `3 < 4` -\> True | `result.append('s')` | `['a', 'p', 'b', 'q', 'r', 's']`|

3.  **Final Step**:
      * The loop finishes.
      * `return "".join(['a', 'p', 'b', 'q', 'r', 's'])`
      * The final output is **`"apbqrs"`**.

## Performance Analysis

### Time Complexity: O(L)

  - Where `L` is the length of the **longer** string (`L = max(m, n)`). The loop runs `L` times, and the operations inside are constant time.

### Space Complexity: O(m + n)

  - The `result` list stores every character from both input strings. The space required is proportional to the total length of the input strings.

## Key Learning Points

  - How to iterate through sequences of different lengths within a single loop by using the `max` length.
  - The critical importance of boundary checks (`if i < length`) to prevent `IndexError` when dealing with sequences of varying sizes.
  - The standard Python pattern of building a list of characters and using `"".join()` at the end for efficient string construction.