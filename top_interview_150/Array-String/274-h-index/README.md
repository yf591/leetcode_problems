# 274\. H-Index - Solution Explanation

## Problem Overview

Given an array of integers `citations`, where each number represents the citation count for a single paper, the task is to calculate the researcher's **h-index**.

**H-Index Definition:**
The h-index is a metric used to measure the productivity and impact of a researcher. It is defined as the **maximum value of `h`** such that the researcher has published at least `h` papers that have each been cited at least `h` times.

**Examples:**

```python
Input: citations = [3,0,6,1,5]
Output: 3
Explanation:
The researcher has 5 papers.
Let's sort them by citation count (high to low): [6, 5, 3, 1, 0]
- They have 1 paper with at least 1 citation.
- They have 2 papers with at least 2 citations.
- They have 3 papers with at least 3 citations ([6, 5, 3]).
- They do NOT have 4 papers with at least 4 citations (the 4th paper only has 1 citation).
The maximum h that satisfies the condition is 3.
```

## Key Insights

### Sorting Simplifies the Problem

The definition of the h-index compares a *count of papers* with a *citation threshold*. This can be tricky to check directly. The key insight is that if we **sort the citations in descending order**, the problem becomes much simpler.

Once sorted, we can iterate through the list. For any position `i` in the sorted list:

  - The number of papers we have looked at so far is `i + 1`.
  - The minimum number of citations among these papers is `citations[i]` (since the list is sorted from high to low).

This allows us to directly check the h-index condition (`h` papers with at least `h` citations) at each step.

## Solution Approach

This solution sorts the `citations` array in descending order. It then iterates through the sorted array to find the largest `h` that satisfies the h-index definition.

```python
from typing import List

class Solution:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)
        
        # Sort the citations in descending (high to low) order.
        citations.sort(reverse=True)
        
        h = 0
        # Iterate through the sorted list. The index 'i' gives us the count
        # of papers we are considering (i + 1).
        for i in range(n):
            # Number of papers considered so far = i + 1
            # Minimum citations among these papers = citations[i]
            
            # Check if we have (i + 1) papers with at least (i + 1) citations.
            # We only need to check the i-th paper, as it has the minimum citations
            # in the group of (i + 1) papers.
            if citations[i] >= i + 1:
                # If the condition is met, then (i + 1) is a possible h-index.
                h = i + 1
            else:
                # The moment the citation count is less than the number of papers,
                # we know that no larger h-index is possible, so we can stop.
                break
                
        return h
```

## Detailed Code Analysis

### Step 1: Sorting

```python
citations.sort(reverse=True)
```

  - This is the most important step. By sorting the citations from highest to lowest, we can process the papers in order of impact. This makes the subsequent check much easier.

### Step 2: Iteration and the Core Condition

```python
h = 0
for i in range(n):
    if citations[i] >= i + 1:
        h = i + 1
    else:
        break
```

  - We loop through the sorted list. The loop index `i` (0-based) is used to derive the count of papers `h` (which is 1-based, so `h = i + 1`).
  - The condition `citations[i] >= i + 1` is a direct translation of the h-index definition: "Do we have `h` papers (where `h` is `i+1`) that have at least `h` citations?". Because the list is sorted descending, we only need to check the `h`-th paper (`citations[i]`). If its citation count is at least `h`, then all the `h-1` papers before it must also have at least `h` citations.
  - If the condition is met, we update our candidate `h`.
  - If the condition fails, we `break` immediately. Since the citations are sorted descending, we know that no larger `h` could possibly satisfy the condition.

## Step-by-Step Execution Trace

### Example: `citations = [3, 0, 6, 1, 5]`

1.  **Initial State**: `h = 0`
2.  **Sort `citations`**: `[6, 5, 3, 1, 0]`

| `i` | `i + 1` (potential `h`) | `citations[i]` | `citations[i] >= i + 1`? | Action | `h` |
| :-- | :--- | :--- | :--- | :--- | :--- |
| **0** | 1 | 6 | `6 >= 1` -\> **True** | Update `h = 1` | **1** |
| **1** | 2 | 5 | `5 >= 2` -\> **True** | Update `h = 2` | **2** |
| **2** | 3 | 3 | `3 >= 3` -\> **True** | Update `h = 3` | **3** |
| **3** | 4 | 1 | `1 >= 4` -\> **False** | `break` loop | 3 |

  - The loop breaks when `i=3`. The last valid `h` recorded was `3`.
  - The function returns **3**.

## Performance Analysis

### Time Complexity: O(n log n)

  - The dominant operation is sorting the `citations` array, which typically takes `O(n log n)` time. The subsequent loop takes `O(n)` time.

### Space Complexity: O(1) or O(log n) to O(n)

  - This depends on the space complexity of the sorting algorithm used. Python's Timsort can use up to `O(n)` space in the worst case, but it's often much less. If we modify the array in-place, the extra space is minimal.

## Alternative Approaches Comparison

### Approach 1: Sorting (Our Solution)

  - ✅ Very intuitive and easy to understand once the concept is grasped.
  - ❌ `O(n log n)` time complexity might not be the absolute fastest.

### Approach 2: Counting Sort (More Efficient)

  - This approach avoids a comparison sort by using the constraints on the citation values.
  - **Logic**: Create an array of buckets (e.g., size `n+1`). Iterate through citations, incrementing the count for that number in the bucket array. Then, iterate backwards through the buckets, accumulating the paper count. The first time the accumulated paper count is greater than or equal to the bucket index (`h`), you've found the h-index.
  - ✅ **Time: O(n)**, **Space: O(n)**. Faster than the sorting approach for large `n`.
  - ❌ The logic is less direct and requires more space.

## Key Learning Points

  - Sorting is a powerful pre-processing step that can simplify many array-based problems.
  - The relationship between an element's value and its index in a sorted list can be exploited to create efficient algorithms.
  - Clearly understanding a problem's definition (like the h-index) is the most critical first step.