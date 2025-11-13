# 2542\. Maximum Subsequence Score - Solution Explanation

## Problem Overview

You are given two arrays, `nums1` and `nums2`, of the same length, and an integer `k`. The goal is to find the **maximum possible score** you can get by choosing a **subsequence** of `k` indices.

**Score Calculation:**
The score for a chosen set of `k` indices is calculated as:
`Score = (Sum of nums1 elements) * (Minimum of corresponding nums2 elements)`

**Example:**

```python
Input: nums1 = [1,3,3,2], nums2 = [2,1,3,4], k = 3
Output: 12
Explanation:
Let's choose the indices {0, 2, 3}.
- Sum from nums1: nums1[0] + nums1[2] + nums1[3] = 1 + 3 + 2 = 6
- Minimum from nums2: min(nums2[0], nums2[2], nums2[3]) = min(2, 3, 4) = 2
- Score = 6 * 2 = 12.
This is the highest possible score.
```

-----

## Deep Dive: Key Python Functions Used

Before the solution, let's understand the core tools.

### 1\. `zip(list1, list2, ...)`

  - **What is it?** `zip` is a built-in Python function that "zips" together multiple lists (or any iterables) into a single list of tuples.
  - **How it works:** It takes the 1st element from each list and pairs them, then the 2nd from each, and so on, until the *shortest* list runs out.
  - **Example:**
    ```python
    list_a = [1, 2, 3]
    list_b = ['a', 'b', 'c']
    zipped = zip(list_a, list_b)
    # zipped is an iterator, so we convert it to a list
    print(list(zipped)) 
    # Output: [(1, 'a'), (2, 'b'), (3, 'c')]
    ```
  - **Why use it here?** It's the perfect tool to link `nums1[i]` and `nums2[i]` together. We can create a single list of pairs: `[(nums1[0], nums2[0]), (nums1[1], nums2[1]), ...]`.

### 2\. What is a Heap? (Priority Queue) 🌳

  - **What is it?** A heap is a specialized tree-based data structure that satisfies the "heap property." It's a way to store data that makes it *extremely fast* to find the item with the highest (or lowest) priority.
  - **Analogy:** Think of a hospital's emergency room. It's a "priority queue." Patients are not treated in the order they arrive (like a normal queue); they are treated based on the *severity* of their condition. A heap data structure does this for numbers.
  - **Min-Heap (used in this solution):** The parent node is *always smaller* than its children. This guarantees that the **smallest element in the heap is always at the root (top)**.
  - **Max-Heap:** The parent node is *always larger* than its children. The **largest** element is always at the root.

### 3\. What is Python's `heapq` module?

  - `heapq` is Python's built-in module for heap operations. It does not create a new data structure; it provides functions that cleverly use a regular **Python list** to *behave* like a heap. By default, `heapq` implements a **min-heap**.

  - **`heapq.heappush(heap_list, item)`**:

      - **Action:** Adds the `item` to the `heap_list`.
      - **Magic:** It then rearranges the list (an `O(log n)` operation) to ensure the min-heap property is maintained (i.e., the smallest element is still at `heap_list[0]`).

  - **`heapq.heappop(heap_list)`**:

      - **Action:** Removes and returns the **smallest** element from the `heap_list` (which is *always* `heap_list[0]`).
      - **Magic:** It then rearranges the remaining elements (an `O(log n)` operation) to restore the min-heap property.

-----

## Key Insights for This Problem

### 1\. The Core Conflict

We want to maximize `Score = Sum * Min`.

  - To get a big `Sum`, we want to pick the `k` largest values from `nums1`.
  - To get a big `Min`, we want to pick `k` values from `nums2` that are all large.
    The challenge is that the `nums1` and `nums2` values are tied together by their index. A large `nums1` value might have a tiny `nums2` value, and vice versa.

### 2\. The "Fix one variable" Insight

This problem is hard to solve if we try to optimize both `Sum` and `Min` at the same time. The key insight is to **fix one variable**. Let's try to iterate through all possible values for the `Min` part of the equation.

If we decide that `nums2[i]` will be the **minimum** for our group of `k`, it means we can *only* choose from the set of indices `j` where `nums2[j] >= nums2[i]`. From this eligible group, we would then (greedily) pick the `k` elements with the **largest `nums1` values** to maximize the `Sum`.

### 3\. The Greedy "Sort by `nums2`" Strategy

Iterating through every possible `nums2[i]` as the minimum is still slow. We can be much more clever.

1.  First, let's `zip` `nums1` and `nums2` together into a list of pairs: `[(1,2), (3,1), (3,3), (2,4)]`.
2.  Now, let's **sort this list of pairs based on the `nums2` value, in descending order**.
    `[(2,4), (3,3), (1,2), (3,1)]`
3.  **Why?** This is the magic. We can now iterate through this sorted list. As we iterate, the `nums2` value of the *current* pair we are looking at is **guaranteed to be the minimum** of all the `nums2` values we have seen in our group so far.

**Example of this logic:**

  - We process `(2,4)`.
  - We process `(3,3)`. The group is `{(2,4), (3,3)}`. The `Min` is now `3`.
  - We process `(1,2)`. The group is `{(2,4), (3,3), (1,2)}`. The `Min` is now `2`.

This turns the problem into: "As I iterate through the pairs, what are the `k` largest `nums1` values I have seen so far?"

### 4\. The "Top K" Problem and Min-Heaps

How do we efficiently maintain a list of the "Top `k`" largest `nums1` values? This is a classic problem solved by a **min-heap of size `k`**.

  - We will maintain a min-heap that stores the `k` largest `nums1` values we've encountered.
  - When a new `nums1` value arrives, we push it onto the heap.
  - If the heap's size is now `k+1`, we `pop` the smallest item (the root) to bring it back to size `k`.
  - This ensures the heap *always* contains the `k` largest elements.

## Solution Approach

This solution combines all these insights. It zips, sorts by `nums2` (descending), and then iterates through the pairs, using a min-heap of size `k` to track the largest `nums1` values.

```python
import heapq
from typing import List

class Solution:
    def maxScore(self, nums1: List[int], nums2: List[int], k: int) -> int:
        
        # --- Step 1: Combine nums1 and nums2 into a list of pairs ---
        # [(1,2), (3,1), (3,3), (2,4)]
        pairs = list(zip(nums1, nums2))
        
        # --- Step 2: Sort the pairs based on nums2 in descending order ---
        # We sort by the second element (x[1]) of the pair.
        # [(2,4), (3,3), (1,2), (3,1)]
        pairs.sort(key=lambda x: x[1], reverse=True)
        
        # --- Step 3: Initialize the min-heap and state variables ---
        # This heap will store the 'k' largest nums1 values we've seen.
        min_heap = []
        # 'current_sum' tracks the sum of the elements *in the heap*.
        current_sum = 0
        max_score = 0
        
        # --- Step 4: Iterate through the sorted pairs ---
        for n1, n2 in pairs:
            # Add the current nums1 value to our sum and heap.
            current_sum += n1
            heapq.heappush(min_heap, n1)
            
            # If the heap is too large (has k+1 elements)...
            if len(min_heap) > k:
                # ...remove the smallest element from the heap and the sum.
                smallest_n1 = heapq.heappop(min_heap)
                current_sum -= smallest_n1
                
            # If the heap has exactly k elements, we have a valid
            # subsequence of size k, so we can calculate a potential score.
            if len(min_heap) == k:
                # current_sum = Sum of the k largest nums1 values in this group
                # n2 = The minimum of the k corresponding nums2 values (due to sorting)
                score = current_sum * n2
                max_score = max(max_score, score)
                
        # After the loop, max_score holds the best score found.
        return max_score
```

## Step-by-Step Execution Trace

Let's trace `nums1 = [1,3,3,2]`, `nums2 = [2,1,3,4]`, `k = 3` with extreme detail.

### **Initial State:**

  - `pairs = [(1,2), (3,1), (3,3), (2,4)]`
  - **`sorted_pairs` = `[(2,4), (3,3), (1,2), (3,1)]`** (Sorted by `nums2` descending)
  - `min_heap = []`
  - `current_sum = 0`
  - `max_score = 0`

-----

### **Loop (Iterating through `sorted_pairs`)**

**Loop 1: `(n1, n2) = (2, 4)`**

1.  `current_sum += 2` -\> `current_sum = 2`.
2.  `heappush(min_heap, 2)`. `min_heap = [2]`.
3.  `len(min_heap) > 3`? No (1 \> 3 is False).
4.  `len(min_heap) == 3`? No (1 == 3 is False).

<!-- end list -->

  - `max_score` remains `0`.

**Loop 2: `(n1, n2) = (3, 3)`**

1.  `current_sum += 3` -\> `current_sum = 5`.
2.  `heappush(min_heap, 3)`. `min_heap = [2, 3]`.
3.  `len(min_heap) > 3`? No (2 \> 3 is False).
4.  `len(min_heap) == 3`? No (2 == 3 is False).

<!-- end list -->

  - `max_score` remains `0`.

**Loop 3: `(n1, n2) = (1, 2)`**

1.  `current_sum += 1` -\> `current_sum = 6`.
2.  `heappush(min_heap, 1)`. `min_heap = [1, 3, 2]`.
3.  `len(min_heap) > 3`? No (3 \> 3 is False).
4.  `len(min_heap) == 3`? **Yes**.
      - Calculate `score = current_sum * n2` -\> `6 * 2 = 12`.
      - `max_score = max(0, 12) = 12`.

<!-- end list -->

  - `max_score` is now `12`.

**Loop 4: `(n1, n2) = (3, 1)`**

1.  `current_sum += 3` -\> `current_sum = 9`.
2.  `heappush(min_heap, 3)`. `min_heap = [1, 3, 2, 3]`.
3.  `len(min_heap) > 3`? **Yes** (4 \> 3 is True).
      - `smallest_n1 = heappop(min_heap)` -\> `smallest_n1 = 1`.
      - `current_sum -= 1` -\> `current_sum = 8`.
      - `min_heap` is now `[2, 3, 3]`.
4.  `len(min_heap) == 3`? **Yes**.
      - Calculate `score = current_sum * n2` -\> `8 * 1 = 8`.
      - `max_score = max(12, 8) = 12`.

<!-- end list -->

  - `max_score` remains `12`.

-----

### **End of Algorithm**

  - The `for` loop finishes.
  - The function returns the final `max_score`, which is **12**.

## Performance Analysis

### Time Complexity: O(n log n)

  - `n = len(nums1)`.
  - `zip()` takes `O(n)` time.
  - `sort()` takes `O(n log n)` time (this is the dominant step).
  - The `for` loop runs `n` times.
  - Inside the loop, `heappush` and `heappop` take `O(log k)` time.
  - Total time = `O(n log n) + O(n log k)`. Since `k <= n`, `log k <= log n`. The complexity is dominated by the sort, so it is **`O(n log n)`**.

### Space Complexity: O(n)

  - The `pairs` list requires `O(n)` space to store all the zipped tuples.
  - The `min_heap` requires `O(k)` space.
  - Total space = `O(n + k)`, which simplifies to **`O(n)`** since `k <= n`.