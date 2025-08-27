# 605\. Can Place Flowers - Solution Explanation

## Problem Overview

You are given a `flowerbed` represented by an array of `0`s (empty) and `1`s (planted). You are also given a number `n`, representing the number of new flowers you want to plant. The main rule is that **flowers cannot be planted in adjacent plots**. The task is to determine if it's possible to plant `n` new flowers without violating this rule.

**The Rule for Planting:**
You can plant a flower in a plot `i` only if:

1.  The plot `i` is empty (`flowerbed[i] == 0`).
2.  The plot to its left (`i-1`) is empty.
3.  The plot to its right (`i+1`) is empty.
    (The edges of the flowerbed are considered empty).

**Examples:**

```python
Input: flowerbed = [1,0,0,0,1], n = 1
Output: true
Explanation: You can plant one flower in the middle empty plot (at index 2).

Input: flowerbed = [1,0,0,0,1], n = 2
Output: false
Explanation: You can only plant one flower, so you cannot plant two.
```

## Key Insights

### The Greedy Strategy

The key insight for this problem is to use a **greedy** approach. To maximize the number of flowers we can plant, we should be "greedy" and plant a flower in the **earliest possible valid spot** we find as we scan the flowerbed from left to right.

Why does this work? Planting a flower at the first available spot `i` can only affect the ability to plant at `i+1`. But if we can plant at `i`, it means `i-1` and `i+1` were already empty, so we couldn't have planted at `i-1`, and we wouldn't be able to plant at `i+1` anyway. The greedy choice never prevents a better overall outcome.

## Solution Approach

This solution iterates through the flowerbed a single time. For each plot, it checks if it's possible to plant a flower there. If it is, we "plant" it (by changing the array value to 1) and decrement `n`.

```python
from typing import List

class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        # If we don't need to plant any flowers, we are already done.
        if n == 0:
            return True
            
        # We can iterate through the original flowerbed and modify it.
        for i in range(len(flowerbed)):
            # Condition 1: The current plot must be empty.
            if flowerbed[i] == 0:
                # Condition 2: The left plot must be empty.
                # This is true if we are at the very beginning (i == 0)
                # OR if the plot to the left (i - 1) is 0.
                is_left_empty = (i == 0) or (flowerbed[i - 1] == 0)
                
                # Condition 3: The right plot must be empty.
                # This is true if we are at the very end (i == len(flowerbed) - 1)
                # OR if the plot to the right (i + 1) is 0.
                is_right_empty = (i == len(flowerbed) - 1) or (flowerbed[i + 1] == 0)
                
                # If all three conditions are met, we can plant a flower.
                if is_left_empty and is_right_empty:
                    # Place the flower in the plot.
                    flowerbed[i] = 1
                    # Decrement the number of flowers we still need to plant.
                    n -= 1
                    # Optimization: If we've planted all required flowers, we can stop.
                    if n == 0:
                        return True
                        
        # If we finish the loop and n is not 0, it means we couldn't
        # plant all the flowers.
        return n == 0
```

## Detailed Code Analysis

### Step 1: Handle `n = 0`

```python
if n == 0:
    return True
```

  - This is an initial check. If the goal is to plant zero flowers, the task is trivially accomplished, so we can return `True` immediately.

### Step 2: The Loop

```python
for i in range(len(flowerbed)):
```

  - This starts our single scan through every plot in the flowerbed, from index `0` to the end.

### Step 3: The Three Conditions for Planting

```python
if flowerbed[i] == 0:
    is_left_empty = (i == 0) or (flowerbed[i - 1] == 0)
    is_right_empty = (i == len(flowerbed) - 1) or (flowerbed[i + 1] == 0)
    
    if is_left_empty and is_right_empty:
        # ... plant the flower
```

  - This is the core logic, broken down for maximum clarity.
  - `is_left_empty`: The `(i == 0)` part handles the edge case of the first plot. For any other plot, it checks `flowerbed[i - 1]`. The `or` ensures we don't get an `IndexError`.
  - `is_right_empty`: Similarly, `(i == len(flowerbed) - 1)` handles the last plot.
  - The final `if` statement combines all three rules: the current plot is empty, the left is empty, and the right is empty.

### Step 4: The Greedy Action

```python
flowerbed[i] = 1
n -= 1
```

  - If a spot is valid, we take the greedy action.
  - `flowerbed[i] = 1`: We modify the array in-place. This is crucial because it ensures that when our loop gets to the next plot (`i+1`), its check for `is_left_empty` will correctly fail, upholding the no-adjacent-flowers rule.
  - `n -= 1`: We decrement the number of flowers we still need to plant.

## Step-by-Step Execution Trace

### Example: `flowerbed = [1, 0, 0, 0, 1]`, `n = 1`

| `i` | `flowerbed[i]` | `left_empty`? | `right_empty`? | Can plant? | Action | `n` | `flowerbed` state |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | - | - | - | - | - | **1** | `[1,0,0,0,1]` |
| **0** | `1` | - | - | **No** (plot not empty) | - | 1 | `[1,0,0,0,1]` |
| **1** | `0` | `i==0` (F) or `fb[0]==0` (F) -\> **False** | - | **No** (left is not empty) | - | 1 | `[1,0,0,0,1]` |
| **2** | `0` | `i==0` (F) or `fb[1]==0` (T) -\> **True** | `i==4` (F) or `fb[3]==0` (T) -\> **True** | **Yes\!** | `fb[2]=1`, `n -= 1` | **0** | `[1,0,1,0,1]` |
| | | | | | `n == 0`? Yes. | **Return `True`** | |

The function exits early with `True` as soon as `n` becomes `0`.

## Performance Analysis

### Time Complexity: O(N)

  - Where `N` is the number of plots in the `flowerbed`. We iterate through the list only once.

### Space Complexity: O(1)

  - We modify the array in-place and use only a few variables (`n`, `i`, etc.). The extra space required is constant.

## Key Learning Points

  - **Greedy Algorithms**: This problem demonstrates that sometimes the simplest, most immediate "greedy" choice (planting in the first available spot) leads to the correct overall solution.
  - **Handling Edge Cases**: The logic for checking neighbors (`left_empty`, `right_empty`) shows a standard pattern for handling array edges (`i == 0`, `i == len - 1`) cleanly.
  - **In-Place Modification**: Modifying the input array as you process it is a powerful technique. Here, changing a `0` to a `1` correctly influences the calculation for the next step.