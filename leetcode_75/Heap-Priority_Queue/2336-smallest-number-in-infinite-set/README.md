# 2336\. Smallest Number in Infinite Set - Solution Explanation

## Problem Overview

You are asked to implement a class, `SmallestInfiniteSet`, that simulates a set containing all positive integers (`1, 2, 3, ...`). This class must support two operations:

1.  **`popSmallest()`**: Removes and returns the smallest integer that is *currently* in the set.
2.  **`addBack(num)`**: Adds an integer `num` back into the set. This operation should only do something if `num` is *not* already present in the set.

**Example:**

```python
s = SmallestInfiniteSet()
s.addBack(2)       # Set is [1, 2, 3, ...]. 2 is already in. No change.
s.popSmallest()    # Returns 1. Set is now [2, 3, 4, ...].
s.popSmallest()    # Returns 2. Set is now [3, 4, 5, ...].
s.popSmallest()    # Returns 3. Set is now [4, 5, 6, ...].
s.addBack(1)       # 1 was not in the set. Set is now [1, 4, 5, 6, ...].
s.popSmallest()    # Returns 1 (the one we added back). Set is [4, 5, 6, ...].
s.popSmallest()    # Returns 4. Set is [5, 6, 7, ...].
```

## Deep Dive: What is a Heap? (Priority Queue) 🌳

Before the solution, let's understand our main tool.

  * **What is a Heap?**
    A **heap** is a specialized tree-based data structure that satisfies the "heap property." It's an efficient way to implement a **Priority Queue**, which is like a regular queue or stack, but the item you "pop" is always the one with the highest (or lowest) priority, regardless of when it was added.

  * **Min-Heap (The one we'll use):**

      - **Property**: The value of each parent node is **less than or equal to** the values of its children.
      - **Result**: This guarantees that the **smallest** element in the entire structure is always at the root (top) of the tree.

  * **Why use it here?**
    The `popSmallest()` method requires us to *repeatedly* find the smallest item. A min-heap gives us the smallest item in `O(1)` time (to peek) and `O(log n)` time (to remove).

## Deep Dive: Python's `heapq` Module

Python's `heapq` module provides functions that operate on standard Python **lists** to make them behave like heaps. By default, `heapq` implements a **min-heap**.

  * **`heapq.heappush(heap_list, item)`**:

      - **Action:** Adds the `item` to the `heap_list`.
      - **Process:** It adds the item to the end of the list and then "sifts it up" to its correct position to maintain the heap property.
      - **Time:** `O(log n)`, where `n` is the size of the heap.

  * **`heapq.heappop(heap_list)`**:

      - **Action:** Removes and returns the **smallest** element from the `heap_list` (which is *always* at index `0`).
      - **Process:** It takes the smallest item, moves the last element to the top, and then "sifts it down" to restore the heap property.
      - **Time:** `O(log n)`.

## Key Insights

### 1\. Simulating "Infinity"

We cannot store an infinite set of numbers. However, we know the set starts as `[1, 2, 3, 4, ...]`. We can simulate this "infinite" part with a single integer variable, let's call it `current_smallest_in_sequence`, which just tracks the next integer we would pop from the main sequence. It starts at `1`.

  - When we `popSmallest()`, we return `current_smallest_in_sequence` and then increment it. (e.g., return `1`, set counter to `2`).

### 2\. The Two-Pool Problem

The `addBack(num)` method creates a problem. Imagine we pop `1`, `2`, and `3`. Our `current_smallest_in_sequence` is now `4`. The "infinite" pool is `[4, 5, 6, ...]`. If the user then calls `addBack(1)`, our set is now:
`{1} U {4, 5, 6, ...}`
We now have *two* "pools" of numbers to draw from:

1.  A pool of "added back" numbers.
2.  The main "infinite" sequence.

When `popSmallest()` is called, we must return the smallest number from *either* of these two pools.

### 3\. The Hybrid Solution (Heap + Counter)

This two-pool problem leads to our beautiful solution:

  - **The Counter**: We use the integer `self.current_smallest` to manage the "infinite" pool.
  - **The Min-Heap**: We use a min-heap, `self.added_back_heap`, to manage the "added back" pool. A min-heap is perfect because it gives us the smallest added-back number in `O(1)` peek time.

Now, `popSmallest()` is simple: it just compares the top of the heap to the counter and returns the smaller of the two.

### 4\. Handling Duplicates

The `addBack(num)` method should do nothing if the number is already present. How do we check this?

  - If `num >= self.current_smallest`, the number is "already present" in the infinite sequence, so we can ignore it.
  - If `num` is *already in our heap*, we should also ignore it. The fastest way to check this is to use a companion **Hash Set** (`self.added_back_set`) to keep track of what's in the heap, allowing `O(1)` duplicate checks.

## Solution Approach

This solution implements the "Heap + Counter" hybrid. It uses `current_smallest` for the main sequence and a `heapq` (plus a `set` for duplicate-checking) to manage the numbers that have been added back.

```python
import heapq
from typing import List

class SmallestInfiniteSet:

    def __init__(self):
        # This counter represents the smallest number in the "infinite"
        # part of the set, i.e., numbers that have never been popped.
        self.current_smallest_in_sequence = 1
        
        # A min-heap to store any numbers that are popped and then added back.
        self.added_back_heap = []
        
        # A set to keep track of what's *in the heap* for fast O(1) duplicate checks.
        self.added_back_set = set()
        
    def popSmallest(self) -> int:
        
        smallest_val = 0
        
        # --- Decide which pool to pull from ---
        # We check if the heap is non-empty AND if its smallest element
        # is smaller than the next number in our "infinite" sequence.
        if self.added_back_heap and self.added_back_heap[0] < self.current_smallest_in_sequence:
            # Case 1: The smallest number is in the "added back" heap.
            smallest_val = heapq.heappop(self.added_back_heap)
            # We must remove it from our tracking set as well.
            self.added_back_set.remove(smallest_val)
        
        else:
            # Case 2: The smallest number is in the main sequence.
            smallest_val = self.current_smallest_in_sequence
            # "Pop" it by advancing the sequence counter.
            self.current_smallest_in_sequence += 1
            
        return smallest_val
        

    def addBack(self, num: int) -> None:
        # We only add the number back if it meets two conditions:
        
        # 1. It must be a number we've already popped (i.e., it's smaller
        #    than the next number in the main sequence).
        is_popped = (num < self.current_smallest_in_sequence)
        
        # 2. It must not *already* be in our "added back" heap.
        is_not_in_heap = (num not in self.added_back_set)
        
        if is_popped and is_not_in_heap:
            # If both are true, add it to the heap and the tracking set.
            heapq.heappush(self.added_back_heap, num)
            self.added_back_set.add(num)
```

## Step-by-Step Execution Trace

Let's trace the example `["addBack(2)", "popSmallest", "popSmallest", "popSmallest", "addBack(1)", "popSmallest", "popSmallest", "popSmallest"]` with extreme detail.

### **Initial State:**

  - `self.current_smallest_in_sequence = 1`
  - `self.added_back_heap = []`
  - `self.added_back_set = set()`

-----

### **Call 1: `addBack(2)`**

1.  Check `if num < self.current_smallest...` -\> `if 2 < 1`? **False**.
2.  (The number 2 is still "present" in the main sequence, so no change is made).
3.  **State**: `current_smallest=1`, `heap=[]`, `set={}`

-----

### **Call 2: `popSmallest()`**

1.  Check `if self.added_back_heap...`: The heap is empty.
2.  `else` block runs.
3.  `smallest = self.current_smallest_in_sequence` -\> `smallest = 1`.
4.  `self.current_smallest_in_sequence += 1` -\> `current_smallest_in_sequence = 2`.
5.  **Returns 1**.
6.  **State**: `current_smallest=2`, `heap=[]`, `set={}`

-----

### **Call 3: `popSmallest()`**

1.  Check `if self.added_back_heap...`: The heap is empty.
2.  `else` block runs.
3.  `smallest = self.current_smallest_in_sequence` -\> `smallest = 2`.
4.  `self.current_smallest_in_sequence += 1` -\> `current_smallest_in_sequence = 3`.
5.  **Returns 2**.
6.  **State**: `current_smallest=3`, `heap=[]`, `set={}`

-----

### **Call 4: `popSmallest()`**

1.  Check `if self.added_back_heap...`: The heap is empty.
2.  `else` block runs.
3.  `smallest = self.current_smallest_in_sequence` -\> `smallest = 3`.
4.  `self.current_smallest_in_sequence += 1` -\> `current_smallest_in_sequence = 4`.
5.  **Returns 3**.
6.  **State**: `current_smallest=4`, `heap=[]`, `set={}`

-----

### **Call 5: `addBack(1)`**

1.  Check `if num < self.current_smallest...` -\> `if 1 < 4`? **True**.
2.  Check `if num not in self.added_back_set` -\> `if 1 not in {}`? **True**.
3.  Both conditions are true.
4.  `heapq.heappush(self.added_back_heap, 1)`. `heap` is now `[1]`.
5.  `self.added_back_set.add(1)`. `set` is now `{1}`.
6.  **State**: `current_smallest=4`, `heap=[1]`, `set={1}`

-----

### **Call 6: `popSmallest()`**

1.  Check `if self.added_back_heap...`: `heap` is `[1]`.
2.  Check `if self.added_back_heap[0] < self.current_smallest_in_sequence` -\> `if 1 < 4`? **True**.
3.  `if` block runs.
4.  `smallest = heapq.heappop(self.added_back_heap)` -\> `smallest = 1`. `heap` is now `[]`.
5.  `self.added_back_set.remove(1)`. `set` is now `{}`.
6.  **Returns 1**.
7.  **State**: `current_smallest=4`, `heap=[]`, `set={}`

-----

### **Call 7: `popSmallest()`**

1.  Check `if self.added_back_heap...`: The heap is empty.
2.  `else` block runs.
3.  `smallest = self.current_smallest_in_sequence` -\> `smallest = 4`.
4.  `self.current_smallest_in_sequence += 1` -\> `current_smallest_in_sequence = 5`.
5.  **Returns 4**.
6.  **State**: `current_smallest=5`, `heap=[]`, `set={}`

-----

### **Call 8: `popSmallest()`**

1.  Check `if self.added_back_heap...`: The heap is empty.
2.  `else` block runs.
3.  `smallest = self.current_smallest_in_sequence` -\> `smallest = 5`.
4.  `self.current_smallest_in_sequence += 1` -\> `current_smallest_in_sequence = 6`.
5.  **Returns 5**.
6.  **State**: `current_smallest=6`, `heap=[]`, `set={}`

## Performance Analysis

Let `P` be the number of `popSmallest` calls and `A` be the number of `addBack` calls. Let `k` be the number of elements *in the heap*.

### Time Complexity

  - **`__init__()`**: `O(1)`.
  - **`popSmallest()`**: We compare two numbers (`O(1)`). In the worst case, we `heappop` from the `added_back_heap` and `remove` from the set. `heappop` is `O(log k)` and `set.remove` is `O(1)`. The time complexity is **`O(log k)`**.
  - **`addBack(num)`**: We check `if num < ...` (`O(1)`) and `if num not in ...` (`O(1)`). In the worst case, we `heappush` and `set.add`. `heappush` is `O(log k)`. The time complexity is **`O(log k)`**.

### Space Complexity: O(k)

  - Where `k` is the number of unique elements that are added back.
  - The space is dominated by `self.added_back_heap` and `self.added_back_set`, which both store at most `k` elements.
  - This is very efficient. In the worst case of `1000` calls, if every call is `addBack` with a unique number, the space would be `O(1000)`.