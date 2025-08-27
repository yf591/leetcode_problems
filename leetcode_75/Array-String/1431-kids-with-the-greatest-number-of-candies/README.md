# 1431\. Kids With the Greatest Number of Candies - Solution Explanation

## Problem Overview

You are given a list of integers `candies`, where each number represents the amount of candy a particular kid has. You are also given an integer `extraCandies`. The task is to determine, for each kid, if they would have the **greatest number of candies** among all the kids after receiving all the `extraCandies`.

**Key Definitions:**

  - **Greatest number of candies**: The highest candy count among all kids. Note that multiple kids can share this title.
  - **Return Value**: A list of booleans (`True` or `False`), where `result[i]` is `True` if the `i`-th kid can have the greatest number of candies, and `False` otherwise.

**Examples:**

```python
Input: candies = [2,3,5,1,3], extraCandies = 3
Output: [true,true,true,false,true] 
Explanation:
- The current maximum is 5 candies (held by Kid 3).
- Kid 1: 2 + 3 = 5. This is >= 5. -> True
- Kid 2: 3 + 3 = 6. This is >= 5. -> True
- Kid 3: 5 + 3 = 8. This is >= 5. -> True
- Kid 4: 1 + 3 = 4. This is < 5. -> False
- Kid 5: 3 + 3 = 6. This is >= 5. -> True
```

## Key Insights

### The Two-Pass Approach

The problem can be broken down into two simple, logical steps:

1.  **Find the Target**: First, we need a benchmark to compare against. The "greatest number of candies" is simply the maximum value currently in the `candies` array. We can find this in one pass.
2.  **Check Each Kid**: Once we have this maximum value, we can make a second pass through the `candies` array. For each kid, we perform the check: `(kid's current candies + extraCandies) >= maximum`.

This two-pass strategy is efficient because we avoid recalculating the maximum value inside our main loop.

## Solution Approach (Concise - List Comprehension)

This solution is very "Pythonic." It first finds the maximum value and then uses a single, expressive line of code called a list comprehension to build the final result array.

```python
from typing import List

class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        # Step 1: Find the maximum number of candies any kid currently has.
        max_candies = max(candies)
        
        # Step 2: Use a list comprehension to create the result list.
        # For each kid's candy_count, check if their new total would be the greatest.
        return [candy_count + extraCandies >= max_candies for candy_count in candies]
```

**Strategy:**

1.  **Find Max**: Use the built-in `max()` function to find the greatest value in the `candies` list.
2.  **Build Result**: Use a list comprehension to iterate through each `candy_count` in the `candies` list. For each one, evaluate the boolean expression `candy_count + extraCandies >= max_candies` and add the resulting `True` or `False` to the new list.

-----

## Alternative Solution (Explicit - For Loop)

This solution, which you wrote, is functionally identical to the one above but is more explicit and can be easier to read for beginners. It breaks the logic down into clear, sequential steps.

```python
from typing import List

class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        # Step 1: Find the maximum number of candies.
        max_candies = max(candies)

        # Step 2: Initialize an empty list to store the results.
        result_list = []
        
        # Step 3: Loop through each kid's candy count.
        for candy_count in candies:
            # Step 4: Perform the check and store the boolean result.
            result_bool = candy_count + extraCandies >= max_candies
            # Step 5: Append the result to our list.
            result_list.append(result_bool)

        # Step 6: Return the completed list.
        return result_list
```

## Detailed Code Analysis (For Loop Version)

### Step 1: Find Max

```python
max_candies = max(candies)
```

  - The `max()` function efficiently scans the `candies` list and returns the largest integer. This takes `O(n)` time.

### Step 2: Initialize Result List

```python
result_list = []
```

  - We create an empty list that we will populate with our boolean answers.

### Step 3: The Loop

```python
for candy_count in candies:
```

  - This starts our second pass through the array. The `for` loop will iterate through each element in `candies`, assigning it to the variable `candy_count`.

### Step 4 & 5: The Check and Append

```python
result_bool = candy_count + extraCandies >= max_candies
result_list.append(result_bool)
```

  - This is the core logic. For each `candy_count`:
      - We calculate the potential new total: `candy_count + extraCandies`.
      - We compare this total to our pre-calculated `max_candies`.
      - The expression `... >= max_candies` evaluates directly to a boolean value (`True` or `False`).
      - This boolean value is then appended to our `result_list`.

## Step-by-Step Execution Trace

### Example: `candies = [2, 3, 5, 1, 3]`, `extraCandies = 3`

1.  **Find Max**:

      * `max_candies = max([2, 3, 5, 1, 3])` which is **5**.

2.  **Initialize**:

      * `result_list = []`

3.  **The Loop**:

| `candy_count` | `candy_count + 3` | `... >= 5`? | `result_list` after append |
| :--- | :--- | :--- | :--- |
| **2** | 5 | `5 >= 5` -\> **True** | `[True]` |
| **3** | 6 | `6 >= 5` -\> **True** | `[True, True]` |
| **5** | 8 | `8 >= 5` -\> **True** | `[True, True, True]` |
| **1** | 4 | `4 >= 5` -\> **False**| `[True, True, True, False]` |
| **3** | 6 | `6 >= 5` -\> **True** | `[True, True, True, False, True]` |

4.  **Return**: The loop finishes. The function returns `[True, True, True, False, True]`.

## Performance Analysis (Both Solutions)

### Time Complexity: O(n)

  - Where `n` is the number of kids. The process involves two passes over the array: one to find the maximum (`O(n)`) and one to perform the checks (`O(n)`). The total time complexity is `O(n) + O(n)`, which simplifies to `O(n)`.

### Space Complexity: O(n)

  - We need to create a `result` list of length `n` to store the boolean answers. Therefore, the space required is proportional to the input size. (Note: This does not count the input storage itself).

## Key Learning Points

  - Breaking a problem down into simpler, sequential steps (find the max, then iterate and check) is a powerful strategy.
  - Pre-calculating a value (like `max_candies`) that will be used repeatedly in a loop is a common and important optimization.
  - Python's list comprehensions provide a concise syntax for building a new list based on an existing one, but a standard `for` loop is often more readable and is equally performant.