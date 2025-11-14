# 2462\. Total Cost to Hire K Workers - Solution Explanation

## Problem Overview

You need to hire exactly `k` workers, one at a time, for the minimum possible total cost. You are given the costs of all `n` workers in a list.

**The Hiring Rule:**
In each of the `k` hiring sessions, you have two "pools" of workers to choose from:

1.  The first `candidates` available workers.
2.  The last `candidates` available workers.

You must choose the worker with the **lowest cost** from these two pools combined.

**The Tie-Breaking Rule:**

  - If there is a tie for the lowest cost, you must choose the worker with the **smallest index**.

After a worker is hired, they are removed from the pool and can't be chosen again. If the two pools overlap (i.e., `2 * candidates >= n`), you simply choose from all available workers.

**Example:**

```python
Input: costs = [17,12,10,2,7,2,11,20,8], k = 3, candidates = 4
Output: 11
Explanation:
- Session 1:
  - Left pool (first 4): [17, 12, 10, 2]
  - Right pool (last 4): [7, 2, 11, 20, 8]  <- Wait, pools are [17,12,10,2] and [2,11,20,8]
  - Combined pool: {17, 12, 10, 2, 2, 11, 20, 8}
  - Lowest cost is 2. Two workers have this cost: index 3 and index 5.
  - We pick the one with the smaller index: worker at index 3 (cost 2).
  - Total Cost: 2.
  - Remaining workers: [17, 12, 10, 7, 2, 11, 20, 8]
- Session 2:
  - Left pool (first 4): [17, 12, 10, 7]
  - Right pool (last 4): [7, 2, 11, 20, 8]
  - Combined pool: {17, 12, 10, 7, 2, 11, 20, 8}
  - Lowest cost is 2 (at index 4 in the *new* list, which was index 5 in the original).
  - Total Cost: 2 + 2 = 4.
  - Remaining workers: [17, 12, 10, 7, 11, 20, 8]
- Session 3:
  - Left pool: [17, 12, 10, 7]
  - Right pool: [7, 11, 20, 8]
  - Combined pool: {17, 12, 10, 7, 11, 20, 8}
  - Lowest cost is 7 (at index 3).
  - Total Cost: 4 + 7 = 11.
```

## Deep Dive: What is a Heap? (Priority Queue) 🌳

Before the solution, let's understand our main tool.

  * **What is a Heap?**
    A **heap** is a specialized tree-based data structure that satisfies the "heap property." It's a way to store data that makes it *extremely fast* to find the item with the highest or lowest priority. This is why heaps are used to implement **priority queues**.

      - **Min-Heap**: The value of each parent node is **less than or equal to** the values of its children. This guarantees that the **smallest** element is always at the root.
      - **Max-Heap**: The value of each parent node is **greater than or equal to** the values of its children. The **largest** element is always at the root.

  * **Why use a heap here?**
    The problem is a *repeated search for the minimum value*. A heap allows us to find the minimum in `O(1)` time and add/remove elements in `O(log n)` time.

## Deep Dive: Python's `heapq` Module

Python's `heapq` module provides functions that operate on standard **lists** to make them behave like heaps. By default, `heapq` implements a **min-heap**.

  * **`heapq.heappush(heap_list, item)`**:

      - **Action:** Adds the `item` to the `heap_list`.
      - **Process:** It adds the item to the end of the list and then "sifts it up" to its correct position to maintain the heap property.
      - **Time:** `O(log n)`, where `n` is the size of the heap.

  * **`heapq.heappop(heap_list)`**:

      - **Action:** Removes and returns the **smallest** element from the `heap_list` (which is *always* at index `0`).
      - **Process:** It takes the smallest item, moves the last element to the top, and then "sifts it down" to restore the heap property.
      - **Time:** `O(log n)`.

## Key Insights

### 1\. The Inefficient (Naive) Approach

In each of the `k` sessions, we could build two lists for the left and right pools, find the minimum, and then *rebuild* the entire list of remaining workers. Finding the min takes `O(candidates)` time, but rebuilding the list/pools after removing a worker takes `O(n)` time. Total time would be `O(k * n)`, which is too slow.

### 2\. The Two-Heap (Priority Queue) Strategy

The problem *forces* us to choose from two distinct pools. This is a massive hint to use **two priority queues** (heaps).

  - One min-heap, `left_heap`, will store the `candidates` from the left pool.
  - Another min-heap, `right_heap`, will store the `candidates` from the right pool.

In each of the `k` sessions, we only need to compare the top elements of these two heaps (`left_heap[0]` and `right_heap[0]`). This gives us the best candidate from both pools in `O(1)` time.

### 3\. The Tie-Breaking Rule

The rule is "lowest cost, then smallest index." A min-heap in Python handles this *automatically* if we store **tuples**.

  - We will push `(cost, index)` tuples into the heaps.
  - When Python compares two tuples, like `(2, 3)` and `(2, 5)`, it first compares the costs. Since `2 == 2`, it moves to the next element and compares the indices. Since `3 < 5`, the heap will correctly identify `(2, 3)` as the "smaller" item.

### 4\. The "Refilling" Mechanism (Two Pointers)

We can't just load all workers into the heaps at once. We must maintain two "pools" of size `candidates`. We can use two pointers, `left_ptr` and `right_ptr`, to track the boundary between the "heaped" workers and the "available" workers in the middle of the array.

  - When we hire (pop) a worker from `left_heap`, we add the *next available* worker from the left side (at `left_ptr`) into the `left_heap`.
  - When we hire from `right_heap`, we add the next available worker from the right side (at `right_ptr`) into the `right_heap`.
  - This ensures our heaps always represent the correct pools.

## Solution Approach

This solution implements the two-heap, two-pointer strategy. It initializes two min-heaps with the first `candidates` from each side. Then, it loops `k` times, each time selecting the best worker by comparing the tops of the heaps, and then refilling the heap it selected from with the next available worker.

```python
import heapq
from typing import List

class Solution:
    def totalCost(self, costs: List[int], k: int, candidates: int) -> int:
        
        n = len(costs)
        total_cost = 0
        
        # Pointers for the next available worker to add to the heaps
        left_ptr = 0
        right_ptr = n - 1
        
        # Heaps store (cost, index) to handle tie-breaking
        left_heap = []
        right_heap = []

        # --- Step 1: Initialize the heaps with the first 'candidates' from each side ---
        
        # Fill the left heap
        for _ in range(candidates):
            if left_ptr <= right_ptr:
                heapq.heappush(left_heap, (costs[left_ptr], left_ptr))
                left_ptr += 1
        
        # Fill the right heap
        for _ in range(candidates):
            if left_ptr <= right_ptr:
                # We check left_ptr <= right_ptr *again* to handle overlap.
                # If 2*candidates > n, this check will fail and we'll
                # avoid adding the same worker to both heaps.
                heapq.heappush(right_heap, (costs[right_ptr], right_ptr))
                right_ptr -= 1

        # --- Step 2: Run the k hiring sessions ---
        for _ in range(k):
            # Check for cases where one of the heaps is empty
            if not right_heap:
                # Must hire from left
                cost, _ = heapq.heappop(left_heap)
                total_cost += cost
                # Refill from the left, if possible
                if left_ptr <= right_ptr:
                    heapq.heappush(left_heap, (costs[left_ptr], left_ptr))
                    left_ptr += 1
            elif not left_heap:
                # Must hire from right
                cost, _ = heapq.heappop(right_heap)
                total_cost += cost
                # Refill from the right, if possible
                if left_ptr <= right_ptr:
                    heapq.heappush(right_heap, (costs[right_ptr], right_ptr))
                    right_ptr -= 1
                    
            # Both heaps have candidates, so compare their top elements
            elif left_heap[0] <= right_heap[0]:
                # Left heap wins (lower cost, or same cost with lower index)
                cost, _ = heapq.heappop(left_heap)
                total_cost += cost
                
                # Refill the left heap from the middle
                if left_ptr <= right_ptr:
                    heapq.heappush(left_heap, (costs[left_ptr], left_ptr))
                    left_ptr += 1
            else:
                # Right heap wins
                cost, _ = heapq.heappop(right_heap)
                total_cost += cost
                
                # Refill the right heap from the middle
                if left_ptr <= right_ptr:
                    heapq.heappush(right_heap, (costs[right_ptr], right_ptr))
                    right_ptr -= 1
                    
        return total_cost
```

## Detailed Code Analysis

### Step 1: Initialization

```python
left_ptr = 0
right_ptr = n - 1
left_heap = []
right_heap = []
```

  - We set up our pointers to the start and end of the `costs` list, and initialize our two heaps.

### Step 2: Initial Heap Fill

```python
for _ in range(candidates):
    if left_ptr <= right_ptr:
        heapq.heappush(left_heap, (costs[left_ptr], left_ptr))
        left_ptr += 1
...
for _ in range(candidates):
    if left_ptr <= right_ptr:
        heapq.heappush(right_heap, (costs[right_ptr], right_ptr))
        right_ptr -= 1
```

  - This is the "priming" step. We fill the `left_heap` with the first `candidates` workers.
  - We then fill the `right_heap` with the last `candidates` workers.
  - The check `if left_ptr <= right_ptr` is **critical**. It handles the case where `2 * candidates > n` (the pools overlap). For example, if `costs = [1, 2, 3]` and `candidates = 2`, the left heap will take `(1,0)` and `(2,1)`. `left_ptr` will be 2. The right heap will try to take `(3,2)`. `left_ptr <= right_ptr` (`2 <= 2`) is true. It adds `(3,2)` and `right_ptr` becomes 1. The next iteration `left_ptr <= right_ptr` (`2 <= 1`) is false, so it correctly stops, having added all 3 workers to the heaps.

### Step 3: The `k` Hiring Sessions

```python
for _ in range(k):
```

  - This loop runs exactly `k` times, once for each worker we must hire.

### Step 4: The Selection Logic

```python
if not right_heap:
    # ... hire from left ...
elif not left_heap:
    # ... hire from right ...
elif left_heap[0] <= right_heap[0]:
    # ... hire from left ...
else:
    # ... hire from right ...
```

  - This `if/elif/else` block is the decision-making process for one session.
  - First, we check if either heap is empty. If `right_heap` is empty, we *must* hire from `left_heap`, and vice-versa.
  - If both heaps have workers, we compare their top elements: `left_heap[0]` and `right_heap[0]`. `[0]` accesses the root of the min-heap (the best candidate).
  - `left_heap[0] <= right_heap[0]`: This is the tie-breaker. Python's tuple comparison is lexicographical. It will compare `cost` first. If costs are equal, it will compare `index`. Since we want the *smallest* index, this `(cost, index)` tuple works perfectly.
  - We `heappop` the winner, add its `cost` to `total_cost`.

### Step 5: The Refill Logic

```python
if left_ptr <= right_ptr:
    heapq.heappush(left_heap, (costs[left_ptr], left_ptr))
    left_ptr += 1
```

  - This block is placed inside the `if` block that hired from the `left_heap`.
  - **`if left_ptr <= right_ptr:`**: We check if there are any workers left in the "middle" un-heaped section.
  - If so, we take the next available worker from the left side (`costs[left_ptr]`) and `heappush` them into the `left_heap`.
  - A similar block refills the `right_heap` if we hired from the right. This maintains the "rolling" `candidates` pools.

## Step-by-Step Execution Trace

Let's trace `costs = [17,12,10,2,7,2,11,20,8]`, `k = 3`, `candidates = 4`.

### **Initial State:**

  - `n = 9`, `k = 3`, `c = 4`, `total_cost = 0`
  - `left_ptr = 0`, `right_ptr = 8`
  - `left_heap = []`, `right_heap = []`

-----

### **Phase 1: Initial Heap Fill**

1.  **Fill `left_heap` (runs 4 times):**
      - `push(17, 0)`. `left_ptr = 1`.
      - `push(12, 1)`. `left_ptr = 2`.
      - `push(10, 2)`. `left_ptr = 3`.
      - `push(2, 3)`. `left_ptr = 4`.
      - `left_heap` is now `[(2, 3), (17, 0), (10, 2), (12, 1)]` (heap order)
2.  **Fill `right_heap` (runs 4 times):**
      - `left_ptr=4`, `right_ptr=8`. `4 <= 8` is True. `push(8, 8)`. `right_ptr = 7`.
      - `left_ptr=4`, `right_ptr=7`. `4 <= 7` is True. `push(20, 7)`. `right_ptr = 6`.
      - `left_ptr=4`, `right_ptr=6`. `4 <= 6` is True. `push(11, 6)`. `right_ptr = 5`.
      - `left_ptr=4`, `right_ptr=5`. `4 <= 5` is True. `push(2, 5)`. `right_ptr = 4`.
      - `right_heap` is now `[(2, 5), (20, 7), (11, 6), (8, 8)]` (heap order)

<!-- end list -->

  - **Pointers state**: `left_ptr = 4`, `right_ptr = 4`. The un-heaped middle is just `costs[4] = 7`.

-----

### **Phase 2: Hiring Sessions (Loop `k=3` times)**

**Session 1 (`k=1`):**

  - `left_heap[0]` is `(2, 3)`.
  - `right_heap[0]` is `(2, 5)`.
  - Check: `(2, 3) <= (2, 5)`? **True** (costs are equal, `3 < 5`).
  - Hire from `left_heap`: `cost, _ = heappop(left_heap)` -\> `cost = 2`.
  - `total_cost = 0 + 2 = 2`.
  - Refill `left_heap`: `left_ptr <= right_ptr` (`4 <= 4`) is True.
      - `heappush(left_heap, (costs[4], 4))` -\> `(7, 4)`.
      - `left_ptr` becomes `5`.

**Session 2 (`k=2`):**

  - `left_heap[0]` is now `(7, 4)`.
  - `right_heap[0]` is `(2, 5)`.
  - Check: `(7, 4) <= (2, 5)`? **False**.
  - Hire from `right_heap`: `cost, _ = heappop(right_heap)` -\> `cost = 2`.
  - `total_cost = 2 + 2 = 4`.
  - Refill `right_heap`: `left_ptr <= right_ptr` (`5 <= 4`) is **False**. No refill.

**Session 3 (`k=3`):**

  - `left_heap[0]` is `(7, 4)`.
  - `right_heap[0]` is now `(8, 8)`.
  - Check: `(7, 4) <= (8, 8)`? **True**.
  - Hire from `left_heap`: `cost, _ = heappop(left_heap)` -\> `cost = 7`.
  - `total_cost = 4 + 7 = 11`.
  - Refill `left_heap`: `left_ptr <= right_ptr` (`5 <= 4`) is **False**. No refill.

-----

### **End of Algorithm**

  - The `for _ in range(k)` loop finishes.
  - The function returns the final `total_cost`, which is **11**.

## Performance Analysis

### Time Complexity: O(k log(c) + c)

  - `n` = `len(costs)`, `k` = workers to hire, `c` = `candidates`.
  - **Initialization**: We must fill the two heaps. This involves `2 * c` `heappush` operations. Each push takes `O(log c)` time. Total: `O(c log c)`.
  - **Hiring Loop**: We loop `k` times.
      - Inside the loop, we do 1 `heappop` (`O(log c)`) and at most 1 `heappush` (`O(log c)`).
      - Total for the loop: `O(k * log c)`.
  - **Total Time**: `O(c log c + k log c) = O((c + k) * log c)`.
      - *(This is a simplification. A more precise analysis, considering the `n` elements are all processed, is `O(n log c + k log c)`, which simplifies to `O(n log c)` if `n > k`. But since `c` is the heap size, `O((k+c) log c)` is a common way to express it when `n` is large and we only perform `k` pulls).*
      - Let's stick to a simple, tight analysis: We perform `n` total pushes (initial fill + refills) and `k` total pops. The heap size is at most `2*c`. Total: `O(n log c + k log c) = O((n+k) * log c)`. Given `k <= n`, this is `O(n log c)`.
  - *Let's try again*:
      - `2*c` pushes for initial fill: `O(c log c)`.
      - `k` loops: Each loop has 1 pop (`O(log c)`) and *maybe* 1 push (`O(log c)`). Total: `O(k log c)`.
      - The total number of pushes can't exceed `n`. The number of pops is exactly `k`.
      - Total cost is `O(n * log(c))` (for all pushes) + `O(k * log(c))` (for all pops).
      - This simplifies to **`O((n+k) * log c)`**. Since `k <= n`, this is **`O(n log c)`**.

### Space Complexity: O(c)

  - `c = candidates`.
  - The two heaps, `left_heap` and `right_heap`, store the candidates.
  - The size of `left_heap` is at most `c`. The size of `right_heap` is at most `c`.
  - The total extra space is `O(c + c) = O(c)`.
  - (If `c > n/2`, the total heap size is bounded by `n`, so it's more precisely `O(min(n, c))`).