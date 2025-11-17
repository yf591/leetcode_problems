# 215\. Kth Largest Element in an Array - Solution Explanation

## Problem Overview

You are given an array of integers `nums` and an integer `k`. The task is to find the **k-th largest** element in the array. This means finding the element that would be at the k-th position if the array were sorted in descending order.

**Important Note:** It's the k-th largest overall, *not* the k-th distinct element. Duplicates are counted.

**Examples:**

```python
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
Explanation: If sorted descending: [6, 5, 4, 3, 2, 1]. The 2nd largest is 5.

Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
Explanation: If sorted descending: [6, 5, 5, 4, 3, 3, 2, 2, 1]. The 4th largest is 4.
```

## Key Insights

### 1\. The Obvious (but less optimal) Approach: Sorting

The simplest way to conceptualize the problem is to:

1.  Sort the `nums` array in descending order.
2.  Return the element at index `k-1`.

This works perfectly, but the time complexity is dominated by the sort, which is typically **`O(n log n)`**. The problem often implies or asks for a more efficient solution, especially if `k` is much smaller than `n`.

### 2\. The Efficient Insight: Using a Heap (Priority Queue)

How can we find the k-th largest element *without* fully sorting the entire array? We can use a data structure that efficiently keeps track of the "top k" elements seen so far. A **min-heap** of size `k` is perfect for this.

**The Strategy:**

1.  Imagine we have a min-heap that will store the `k` largest numbers encountered.
2.  Iterate through the input array `nums`.
3.  For each `num`:
    a.  Add it to the min-heap.
    b.  If the heap's size is now *greater than* `k`, it means we have `k+1` elements. Since it's a *min*-heap, the smallest of these `k+1` elements is at the root. This smallest element cannot possibly be the k-th largest overall (it's at best the (k+1)-th largest), so we can safely remove it.
4.  After processing all numbers in `nums`, the min-heap will contain exactly the `k` largest elements from the original array.
5.  The element at the root of the min-heap (the smallest element *within the heap*) is precisely the k-th largest element overall.

This approach has a time complexity of **`O(n log k)`**, which is better than `O(n log n)` when `k` is significantly smaller than `n`.

## Deep Dive: Heaps

  * **What is a Heap?** 🌳
    A heap is a specialized tree-based data structure that satisfies the **heap property**. It's commonly used to implement **priority queues**. While it's a tree conceptually, it's usually implemented efficiently using an array or list.

      - **Heap Property**: The rule that defines the relationship between parent and child nodes. There are two main types:
        1.  **Min-Heap**: The value of each parent node is **less than or equal to** the values of its children. This means the **smallest** element is always at the root.
        2.  **Max-Heap**: The value of each parent node is **greater than or equal to** the values of its children. The **largest** element is always at the root.

  * **What is a Min-Heap (used in this solution)?**
    As mentioned, in a min-heap, the smallest element is always at the top. When you add or remove elements, the heap structure is rearranged (using operations often called "sift-up" or "sift-down") to maintain this property. This rearrangement is very efficient, typically taking `O(log m)` time, where `m` is the number of elements currently in the heap.

## Deep Dive: Python's `heapq` Module

Python doesn't have a built-in heap *class*, but it provides the `heapq` module, which contains functions that operate on standard Python **lists** to make them behave like heaps. By default, `heapq` implements a **min-heap**.

  * **`heapq.heappush(heap_list, item)`**:

      - Adds `item` to the `heap_list`.
      - It then rearranges the list (internally, using sift-up) to ensure the min-heap property is maintained.
      - Time complexity: `O(log m)`.

    <!-- end list -->

    ```python
    import heapq
    my_heap = [1, 5, 3]
    heapq.heapify(my_heap) # Optional, turns list into heap faster: O(m)
    heapq.heappush(my_heap, 2)
    # my_heap might now be [1, 2, 3, 5] (order isn't fully sorted, just heap property)
    ```

  * **`heapq.heappop(heap_list)`**:

      - Removes and returns the **smallest** element from the `heap_list` (which is always at index 0).
      - It then rearranges the remaining elements (internally, using sift-down) to restore the min-heap property.
      - Time complexity: `O(log m)`.

    <!-- end list -->

    ```python
    smallest = heapq.heappop(my_heap) # smallest is 1
    # my_heap might now be [2, 5, 3]
    ```

## Solution Approach (Min-Heap)

This solution iterates through the input numbers, maintaining a min-heap of size `k`. When the heap size exceeds `k`, the smallest element is removed. At the end, the root of the heap is the k-th largest element.

```python
import heapq
from typing import List

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # Step 1: Initialize an empty list to serve as our min-heap.
        min_heap = []
        
        # Step 2: Iterate through each number in the input array.
        for num in nums:
            # Step 2a: Add the current number to the heap.
            heapq.heappush(min_heap, num)
            
            # Step 2b: If the heap size exceeds k...
            if len(min_heap) > k:
                # ...remove the smallest element (the root of the min-heap).
                heapq.heappop(min_heap)
                
        # Step 3: After processing all numbers, the heap contains the k largest elements.
        # The root of the min-heap (min_heap[0]) is the smallest among them,
        # which is the k-th largest element overall.
        return min_heap[0]
```

## Detailed Code Analysis

### Step 1: Initialization

```python
min_heap = []
```

  - We create an empty list. The `heapq` functions will operate directly on this list to maintain the min-heap property.

### Step 2: Iteration and Heap Maintenance

```python
for num in nums:
    heapq.heappush(min_heap, num)
    if len(min_heap) > k:
        heapq.heappop(min_heap)
```

  - **`for num in nums:`**: This loop iterates through every number in the input array.
  - **`heapq.heappush(min_heap, num)`**: We add the current `num` to our heap. The `heapq` module ensures the list remains a valid min-heap after the addition. This takes `O(log size_of_heap)` time, where the size is at most `k`. So, it's `O(log k)`.
  - **`if len(min_heap) > k:`**: We check if adding the new number made our heap too large.
  - **`heapq.heappop(min_heap)`**: If the heap is too large, this removes the smallest element currently in the heap. This also takes `O(log k)` time.
  - This `if` condition ensures our heap never stores more than `k` elements.

### Step 3: Returning the Result

```python
return min_heap[0]
```

  - After the loop finishes, `min_heap` contains the `k` largest numbers from the original `nums` array, structured as a min-heap.
  - In a min-heap, the smallest element is always at the root, which is index `0` when using a list.
  - This smallest element *within the top k elements* is precisely the k-th largest element overall. Accessing `min_heap[0]` is an `O(1)` operation.

## Step-by-Step Execution Trace

Let's trace `nums = [3, 2, 1, 5, 6, 4]`, `k = 2` with extreme detail.

| `num` | Action (`heappush`) | `min_heap` State | `len > k`? (`len > 2`) | Action (`heappop`) | `min_heap` (end) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | - | `[]` | - | - | `[]` |
| **3** | `push(3)` | `[3]` | False | - | `[3]` |
| **2** | `push(2)` | `[2, 3]` | False | - | `[2, 3]` |
| **1** | `push(1)` | `[1, 3, 2]` | True (len=3) | `pop()` -\> removes 1 | `[2, 3]` |
| **5** | `push(5)` | `[2, 3, 5]` | True (len=3) | `pop()` -\> removes 2 | `[3, 5]` |
| **6** | `push(6)` | `[3, 5, 6]` | True (len=3) | `pop()` -\> removes 3 | `[5, 6]` |
| **4** | `push(4)` | `[4, 6, 5]` | True (len=3) | `pop()` -\> removes 4 | `[5, 6]` |

  - The `for` loop finishes.
  - The function returns `min_heap[0]`, which is **5**.

## Performance Analysis

### Time Complexity: O(n log k)

  - Where `n` is the number of elements in `nums` and `k` is the input parameter.
  - The loop runs `n` times.
  - Inside the loop, `heappush` takes `O(log k)` time (since the heap size is limited to `k`).
  - `heappop` also takes `O(log k)` time.
  - The total time complexity is `n * O(log k) = O(n log k)`.

### Space Complexity: O(k)

  - The space is dominated by the `min_heap`, which stores at most `k` elements.

## Alternative Approaches Comparison

### Approach 1: Sorting

  - Time: `O(n log n)`
  - Space: `O(1)` (if sorted in-place) or `O(n)` (otherwise, depends on sort implementation)
  - Simpler code, but less efficient if `k` is much smaller than `n`.

### Approach 2: Min-Heap (Our Solution)

  - Time: `O(n log k)`
  - Space: `O(k)`
  - Generally more efficient than sorting when `k` is small.

### Approach 3: Quickselect (Partition-based selection)

  - Time: **`O(n)` on average**, `O(n²)` in the worst case.
  - Space: `O(1)` (in-place partitioning).
  - The theoretically fastest approach on average, but more complex to implement correctly and has a poor worst-case performance. Often used in specific library implementations.