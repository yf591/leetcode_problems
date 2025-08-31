# 933\. Number of Recent Calls - Solution Explanation

## Problem Overview

The task is to implement a `RecentCounter` class that counts recent requests. It has one method: `ping(t)`.

  - When `ping(t)` is called, it registers a request at a specific time `t`.
  - It must then return the total number of requests that have occurred within the last 3000 milliseconds, inclusive. This means counting all requests with a timestamp in the range `[t - 3000, t]`.

**Key Constraint:**

  - Each call to `ping` will use a timestamp `t` that is strictly greater than the previous call. This is a crucial hint\!

**Example:**

```
ping(1);     // requests = [1], range is [-2999,1], return 1
ping(100);   // requests = [1, 100], range is [-2900,100], return 2
ping(3001);  // requests = [1, 100, 3001], range is [1,3001], return 3
ping(3002);  // requests = [1, 100, 3001, 3002], range is [2,3002], return 3
```

## Key Insights

### Sliding Window of Time

The problem is about a "sliding window" of time. As new pings arrive, the 3000ms window of interest slides forward.

### Discarding Old Data

The most important insight comes from the constraint that `t` is always increasing. This means that once a request timestamp is too old for the current window (i.e., less than `t - 3000`), it will **always** be too old for any future windows. We don't need to store these old timestamps forever; we can discard them.

### The Queue Data Structure

This "add to one end, remove from the other end" pattern is perfectly modeled by a **queue** data structure. A queue operates on a "First-In, First-Out" (FIFO) basis, which is exactly what we need:

  - New requests (`t`) are the "last in" and are added to the back.
  - Old, expired requests were the "first in" and are removed from the front.

In Python, the most efficient queue implementation is the `collections.deque` object.

## Solution Approach

The solution uses a `deque` (a queue) to store the timestamps of the requests. For each `ping`, it adds the new timestamp and removes any that have expired before returning the current size of the queue.

```python
import collections
from typing import List

class RecentCounter:
    def __init__(self):
        # We use a deque (double-ended queue) which is highly efficient
        # for adding to the right and removing from the left.
        self.requests = collections.deque()

    def ping(self, t: int) -> int:
        # Step 1: Add the new request's timestamp to the back of the queue.
        self.requests.append(t)
        
        # Step 2: Remove any old requests from the front of the queue that
        # are no longer in the valid time window [t - 3000, t].
        while self.requests[0] < t - 3000:
            self.requests.popleft()
            
        # Step 3: The size of the queue is now the number of recent requests.
        return len(self.requests)
```

## Deep Dive: Queue vs. List

This is a key concept for this problem. While you could use a standard Python `list`, a `deque` is much more efficient.

  * **List**: Think of a list like a **stack of books**. It's very easy and fast to add a book to the top (`append`) or remove a book from the top (`pop`). However, removing a book from the *bottom* is very slow. You have to lift up all the other books, take the bottom one, and then put them all back down. In Python, this means `list.pop(0)` is an `O(n)` operation because every other element has to be shifted.

  * **Queue (Deque)**: Think of a queue like a **line of people at a checkout**. New people join at the back (`append`), and the person at the front is served first (`popleft`). Both adding to the back and removing from the front are very fast, single operations. In Python, a `deque` is implemented as a doubly-linked list, which makes adding or removing from either end a highly efficient `O(1)` operation.

For this problem, since we are constantly removing old items from the front, using a `deque` is the optimal choice.

## Deep Dive: `popleft()` vs. `pop()`

These two methods determine how you remove items from a collection.

  * **`pop()`**: This method removes an item from the **right end** of the `deque` (or list). This is "Last-In, First-Out" (LIFO) behavior, which is used for implementing a **stack**.
    ```
    my_deque = deque([1, 2, 3])
    my_deque.pop()  # returns 3
    # my_deque is now deque([1, 2])
    ```
  * **`popleft()`**: This method, which is **only available on a `deque`**, removes an item from the **left end**. This is "First-In, First-Out" (FIFO) behavior, which is used for implementing a **queue**.
    ```
    my_deque = deque([1, 2, 3])
    my_deque.popleft()  # returns 1
    # my_deque is now deque([2, 3])
    ```

In our problem, we need to remove the *oldest* requests, which are at the left end of our deque, so we use `popleft()`.

## Step-by-Step Execution Trace

Let's trace the example: `ping(1)`, `ping(100)`, `ping(3001)`, `ping(3002)`

| `ping(t)` | `t - 3000` (Window Start) | `requests` (Before `append`) | `requests` (After `append`) | `while` Loop Action | `requests` (After `while`) | Return Value `len(requests)` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | - | `deque([])` | - | - | `deque([])` | - |
| **1** | -2999 | `deque([])` | `deque([1])` | `1 < -2999` is **False**. Loop does not run. | `deque([1])` | **1** |
| **100** | -2900 | `deque([1])` | `deque([1, 100])` | `1 < -2900` is **False**. Loop does not run. | `deque([1, 100])`| **2** |
| **3001**| 1 | `deque([1, 100])` | `deque([1, 100, 3001])` | `1 < 1` is **False**. Loop does not run. | `deque([1, 100, 3001])` | **3** |
| **3002**| 2 | `deque([1, 100, 3001])` | `deque([1, 100, 3001, 3002])`| **Check 1**: `1 < 2` is **True**. `popleft()`. `requests` becomes `deque([100, 3001, 3002])`.\<br\>**Check 2**: `100 < 2` is **False**. Loop ends. | `deque([100, 3001, 3002])` | **3** |

## Performance Analysis

### Time Complexity: Amortized O(1)

  - For each `ping` call, the `append` operation is `O(1)`. The `while` loop might run multiple times, but each timestamp is added to the deque exactly once and removed from the deque at most once over the entire series of calls. This means the total work is proportional to the total number of pings, so the **amortized** (or average) cost per `ping` is `O(1)`.

### Space Complexity: O(W)

  - Where `W` is the maximum number of requests that can fit in the 3000ms window. The space used by the deque is proportional to the number of items in the current time window.

## Key Learning Points

  - **Sliding Window**: This is a classic example of a sliding window problem, where you only care about a recent subset of data.
  - **Queues (`deque`)**: A queue is the ideal data structure for managing a sliding window where items are added at one end and removed from the other.
  - **Amortized Analysis**: Understanding that while a single operation might sometimes take longer, the average cost over many operations can be very low.