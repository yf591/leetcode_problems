# 11\. Container With Most Water - Solution Explanation

## Problem Overview

You are given an array of integers `height`, where each integer `height[i]` represents the height of a vertical line at position `i`. The goal is to find two of these lines that, together with the x-axis, form a container that can hold the most water.

**Area Calculation:**
The amount of water a container can hold is determined by its area. The formula is:
`Area = width * height`

  - **Width**: The distance between the two lines (`right_index - left_index`).
  - **Height**: The height of the container is limited by the **shorter** of the two lines (`min(height[left], height[right])`).

**Example:**

```python
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The two lines at index 1 (height 8) and index 8 (height 7) form the container with the maximum area.
Width = 8 - 1 = 7
Height = min(8, 7) = 7
Area = 7 * 7 = 49.
```

## Key Insights

### The Inefficient Brute-Force Approach

A naive solution would be to check every single possible pair of lines. You could use two nested loops to calculate the area for all pairs and keep track of the maximum. However, this would have a time complexity of `O(n²)`, which is too slow for the problem's constraints.

### The Two-Pointer and Greedy Insight

The key to an efficient `O(n)` solution is the **two-pointer technique** combined with a **greedy** choice.

1.  **Start with Maximum Width**: The widest possible container is always formed by the two outermost lines. Let's start with a `left` pointer at index `0` and a `right` pointer at the last index.

2.  **The Greedy Choice**: We have a container. To find a potentially better one, we must move one of the pointers inward. Which one should we move?

      - As we move a pointer inward, the **width of our container will always decrease**.
      - Therefore, the **only way** to find a larger area is if the new container has a significantly greater **height**.
      - The current container's height is `min(height[left], height[right])`.
      - If we move the pointer of the *taller* line, the height of the new, narrower container will still be limited by the same *shorter* line. The width has decreased, and the height has not increased, so the area can only get smaller. This is a wasted move.
      - However, if we move the pointer of the **shorter** line, we are giving ourselves a chance to find a new, taller line. This new, taller line *might* be tall enough to compensate for the reduced width and create a larger area.

This greedy choice—**always move the shorter of the two pointers inward**—is the core of the algorithm. It allows us to intelligently discard possibilities and find the maximum area in a single pass.

## Solution Approach

This solution implements the efficient two-pointer approach. It starts with the widest container and greedily moves the pointers inward, updating the maximum area found along the way.

```python
from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        max_area = 0

        while left < right:
            # Calculate the area of the current container.
            width = right - left
            current_height = min(height[left], height[right])
            current_area = width * current_height
            
            # Update the maximum area found so far.
            max_area = max(max_area, current_area)
            
            # Make the greedy choice: move the pointer of the shorter line.
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
                
        return max_area
```

## Detailed Code Analysis

### Step 1: Pointer and Max Area Initialization

```python
left = 0
right = len(height) - 1
max_area = 0
```

  - We initialize our two pointers. `left` starts at the beginning of the array (index 0), and `right` starts at the very end. This ensures our first container is the widest possible.
  - `max_area` is initialized to `0`. This variable will store the best result we find during our traversal.

### Step 2: The Loop Condition

```python
while left < right:
```

  - The loop will continue as long as our two pointers have not met or crossed. The moment `left` is equal to or greater than `right`, it means we have considered all possible widths.

### Step 3: Area Calculation

```python
width = right - left
current_height = min(height[left], height[right])
current_area = width * current_height
```

  - Inside the loop, we first calculate the area of the container formed by the lines at the current `left` and `right` pointers. This is a direct translation of the area formula.

### Step 4: Tracking the Maximum

```python
max_area = max(max_area, current_area)
```

  - We compare the `current_area` with the `max_area` we've seen on all previous steps. If the current one is better, we update `max_area`.

### Step 5: The Greedy Move

```python
if height[left] < height[right]:
    left += 1
else:
    right -= 1
```

  - This is the implementation of our key insight.
  - If the line on the left is shorter, we increment `left`. We discard the shorter line in the hope of finding a taller one.
  - If the line on the right is shorter (or if they are equal), we decrement `right`.
  - This guarantees that in every single step, we are making the most optimal move to find a potentially larger area.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `height = [1, 8, 6, 2, 5, 4, 8, 3, 7]` with extreme detail.

| `left` | `right` | `height[left]` | `height[right]` | `min_height` | `width` | `current_area` | `max_area` | Action (Move Pointer) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0** | **8** | 1 | 7 | `min(1,7)=1` | 8 | `8*1=8` | **8** | Move `left` (since 1 \< 7) |
| **1** | **8** | 8 | 7 | `min(8,7)=7` | 7 | `7*7=49` | **49** | Move `right` (since 7 \< 8) |
| **1** | **7** | 8 | 3 | `min(8,3)=3` | 6 | `6*3=18` | 49 | Move `right` (since 3 \< 8) |
| **1** | **6** | 8 | 8 | `min(8,8)=8` | 5 | `5*8=40` | 49 | Move `right` (they are equal) |
| **1** | **5** | 8 | 4 | `min(8,4)=4` | 4 | `4*4=16` | 49 | Move `right` (since 4 \< 8) |
| **1** | **4** | 8 | 5 | `min(8,5)=5` | 3 | `3*5=15` | 49 | Move `right` (since 5 \< 8) |
| **1** | **3** | 8 | 2 | `min(8,2)=2` | 2 | `2*2=4` | 49 | Move `right` (since 2 \< 8) |
| **1** | **2** | 8 | 6 | `min(8,6)=6` | 1 | `1*6=6` | 49 | Move `right` (since 6 \< 8) |

  - At this point, `left` is `1` and `right` is `1`. The loop condition `while left < right` (`1 < 1`) is now **False**. The loop terminates.
  - The function returns the final `max_area`, which is **49**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of lines in the `height` array. The `left` and `right` pointers start at opposite ends and move towards each other. Each pointer will traverse the array at most once.

### Space Complexity: O(1)

  - The solution uses only a few variables to store the pointers and the maximum area. The space required is constant and does not grow with the size of the input.

## Key Learning Points

  - **Two-Pointer Technique**: This is a powerful pattern for problems on sorted or partially-ordered data where you need to find a pair of elements that satisfy a condition. Starting from the outside and moving inward is a common approach.
  - **Greedy Algorithms**: The logic of making the "best" local choice at each step (moving the shorter pointer) leads to the globally optimal solution. Understanding *why* the greedy choice is safe is the most important takeaway.
  - **Optimizing from Brute-Force**: This problem is a classic example of how to think about optimizing a slow `O(n²)` solution into a highly efficient `O(n)` one by eliminating possibilities intelligently.