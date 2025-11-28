# 373\. Find K Pairs with Smallest Sums - Solution Explanation

## Problem Overview

You are given two integer arrays `nums1` and `nums2` sorted in **non-decreasing order** and an integer `k`.
Your task is to find the `k` pairs `(u, v)` with the **smallest sums**, where `u` is from `nums1` and `v` is from `nums2`.

**Example:**

```python
Input: nums1 = [1, 7, 11], nums2 = [2, 4, 6], k = 3
Output: [[1, 2], [1, 4], [1, 6]]
Explanation: 
Possible sums: 
1+2=3, 1+4=5, 1+6=7, 
7+2=9, 7+4=11, 7+6=13... 
The three smallest are 3, 5, and 7.
```

## Deep Dive: What is a Heap? 🌳

A **Heap** is a specialized tree-based data structure that satisfies the **Heap Property**. It is the standard way to implement a **Priority Queue**.

### 1\. The Concept

Imagine a task list where you don't do things in the order you wrote them down. Instead, you always do the **most urgent** task first. A heap is a data structure designed to give you that "most urgent" item instantly.

### 2\. Types of Heaps

  * **Min-Heap**: The parent is always **smaller** (or equal) than its children.
      * **Result**: The root (top) is always the **minimum** element in the entire dataset.
      * **Use Case**: Finding the smallest sum (like in this problem\!).
  * **Max-Heap**: The parent is always **larger** (or equal) than its children.
      * **Result**: The root (top) is always the **maximum** element.

### 3\. Efficiency

Heaps are incredibly fast for specific operations:

  * **Find Minimum**: **O(1)** (Instant lookup at the top).
  * **Add Item (Push)**: **O(log N)** (Very fast).
  * **Remove Minimum (Pop)**: **O(log N)** (Very fast).

*Contrast this with a Sorted Array: Finding min is O(1), but adding a new item while keeping it sorted is O(N), which is much slower.*

### 4\. Python's `heapq`

Python uses the `heapq` module to turn standard lists into Min-Heaps.

  * `heapq.heappush(list, item)`: Adds item to heap, maintaining order.
  * `heapq.heappop(list)`: Removes and returns the smallest item.

[Image of binary search tree algorithm]

*(Note: While the image above shows a BST, a Heap is structurally similar as a binary tree but with different ordering rules, specifically designed for O(1) access to the root).*

## Key Insights for This Problem

### 1\. The Implicit Matrix

Since `nums1` and `nums2` are sorted, we can visualize the pairs as a matrix (grid) of sums:

  * Rows represent elements from `nums1`.
  * Columns represent elements from `nums2`.

| Sums | `2` (col 0) | `4` (col 1) | `6` (col 2) |
| :--- | :--- | :--- | :--- |
| **`1` (row 0)** | **3** | 5 | 7 |
| **`7` (row 1)** | 9 | 11 | 13 |
| **`11` (row 2)** | 13 | 15 | 17 |

Notice a pattern?

  * Every row is sorted increasing to the right.
  * Every column is sorted increasing downwards.
    The smallest elements are clustered in the **top-left**.

### 2\. The "Frontier" Strategy

We don't need to calculate *every* sum (which would be huge, $N \times M$). We only need to explore the **frontier** of smallest sums.

1.  **Initialization**: Start by picking the first element of every row (the first column). These are the smallest possible candidates for each row. Put them in a Min-Heap.
2.  **Selection**: The top of the heap is guaranteed to be the current smallest sum overall. Pop it\!
3.  **Expansion**: If we picked the pair at `(row, col)`, the next smallest pair *from that specific row* is `(row, col + 1)`. We push that into the heap.

## Solution Approach

```python
import heapq
from typing import List

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        # Min-heap to store tuples: (sum, index_i, index_j)
        min_heap = []
        result = []
        
        # Step 1: Initialize the heap with the first element of each row.
        # We only need min(k, len(nums1)) rows because the k-th smallest pair 
        # cannot possibly come from a row index > k.
        for i in range(min(k, len(nums1))):
            current_sum = nums1[i] + nums2[0]
            # We store indices i and j to track where we are in the matrix.
            heapq.heappush(min_heap, (current_sum, i, 0))
            
        # Step 2: Extract the smallest pairs one by one.
        while k > 0 and min_heap:
            # Pop the pair with the smallest sum
            current_sum, i, j = heapq.heappop(min_heap)
            result.append([nums1[i], nums2[j]])
            
            # Step 3: Push the next pair from the same row into the heap.
            # If we just used (i, j), the next candidate in this row is (i, j+1).
            if j + 1 < len(nums2):
                next_sum = nums1[i] + nums2[j + 1]
                heapq.heappush(min_heap, (next_sum, i, j + 1))
                
            k -= 1
            
        return result
```

## Detailed Code Analysis

### Step 1: Initialization

```python
for i in range(min(k, len(nums1))):
    heapq.heappush(min_heap, (nums1[i] + nums2[0], i, 0))
```

  * We treat the problem as merging $K$ sorted lists.
  * We take the first element of `nums1` paired with the first element of `nums2`.
  * We take the *second* element of `nums1` paired with the first element of `nums2`, and so on.
  * This fills our heap with the "leaders" of each row.
  * **Optimization**: We limit the range to `min(k, len(nums1))`. Why? Because if we are looking for the top 3 pairs, we definitely don't need to look at the 100th element of `nums1` yet. It's too big.

### Step 2: The Pop and Push Loop

```python
while k > 0 and min_heap:
    current_sum, i, j = heapq.heappop(min_heap)
    result.append([nums1[i], nums2[j]])
```

  * `heapq.heappop`: This magically gives us the pair with the absolute smallest sum among all candidates currently in the heap.
  * We add the actual numbers `[nums1[i], nums2[j]]` to our result list.

### Step 3: The Expansion (Next Candidate)

```python
if j + 1 < len(nums2):
    next_sum = nums1[i] + nums2[j + 1]
    heapq.heappush(min_heap, (next_sum, i, j + 1))
```

  * Since we just used the pair at indices `(i, j)`, we need to replenish the heap with the next candidate from that specific row.
  * The next candidate is `(i, j+1)`.
  * We calculate its sum and push it onto the heap. The heap automatically sorts it into the correct position.

## Step-by-Step Execution Trace

Let's trace `nums1 = [1, 7, 11]`, `nums2 = [2, 4, 6]`, `k = 3`.

**Initial State:**

  * `min_heap = []`
  * `result = []`

**Step 1: Initialization (First Column)**

  * `i=0`: Push `(1+2, 0, 0)` -\> `(3, 0, 0)`
  * `i=1`: Push `(7+2, 1, 0)` -\> `(9, 1, 0)`
  * `i=2`: Push `(11+2, 2, 0)` -\> `(13, 2, 0)`
  * **Heap State:** `[(3, 0, 0), (9, 1, 0), (13, 2, 0)]` (sorted by sum)

**Step 2: Iteration 1 (`k=3`)**

  * **Pop**: `(3, 0, 0)`. Sum is 3. Indices are `(0, 0)`.
  * **Add to Result**: `[1, 2]`. `result = [[1, 2]]`.
  * **Push Next**: Next in row 0 is `j=1`. Sum `nums1[0] + nums2[1]` = `1 + 4 = 5`.
  * **Push**: `(5, 0, 1)`.
  * **Heap State:** `[(5, 0, 1), (9, 1, 0), (13, 2, 0)]`.

**Step 3: Iteration 2 (`k=2`)**

  * **Pop**: `(5, 0, 1)`. Sum is 5. Indices `(0, 1)`.
  * **Add to Result**: `[1, 4]`. `result = [[1, 2], [1, 4]]`.
  * **Push Next**: Next in row 0 is `j=2`. Sum `nums1[0] + nums2[2]` = `1 + 6 = 7`.
  * **Push**: `(7, 0, 2)`.
  * **Heap State:** `[(7, 0, 2), (9, 1, 0), (13, 2, 0)]`.

**Step 4: Iteration 3 (`k=1`)**

  * **Pop**: `(7, 0, 2)`. Sum is 7. Indices `(0, 2)`.
  * **Add to Result**: `[1, 6]`. `result = [[1, 2], [1, 4], [1, 6]]`.
  * **Push Next**: Next in row 0 is `j=3`. `3 < len(nums2)` is False. No push.
  * **Heap State:** `[(9, 1, 0), (13, 2, 0)]`.

**Termination:** `k` becomes 0. Return `result`.

## Performance Analysis

### Time Complexity: O(k \* log k)

  * **Initialization**: We push up to `k` elements (actually `min(k, n)`) onto the heap. This takes `O(k)`.
  * **Loop**: We run the loop `k` times.
      * In each iteration, we perform one `heappop` and one `heappush`.
      * Heap operations take logarithmic time relative to the size of the heap. The heap size never exceeds `k`. So, each operation is `O(log k)`.
  * **Total**: `O(k log k)`.

### Space Complexity: O(k)

  * The heap stores at most `k` (or `min(k, len(nums1))`) elements at any time.
  * We don't store the full $N \times M$ matrix, making this very memory efficient.