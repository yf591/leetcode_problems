# 2095\. Delete the Middle Node of a Linked List - Solution Explanation

## Problem Overview

You are given the `head` of a singly linked list. The task is to find the **middle node** of the list, delete it, and return the head of the modified list.

**Middle Node Definition:**
For a linked list with `n` nodes, the middle node is the one at index `⌊n / 2⌋` (using 0-based indexing).

  - For `n = 7` (e.g., `[1,2,3,4,5,6,7]`), the middle index is `⌊7/2⌋ = 3`. This is the 4th node.
  - For `n = 6` (e.g., `[1,2,3,4,5,6]`), the middle index is `⌊6/2⌋ = 3`. This is also the 4th node.

**Examples:**

```python
Input: head = [1,3,4,7,1,2,6]
# n = 7. Middle index is 3. The node with value 7 is deleted.
Output: [1,3,4,1,2,6]

Input: head = [1,2,3,4]
# n = 4. Middle index is 2. The node with value 3 is deleted.
Output: [1,2,4]
```

## Key Insights

### The Challenge: Finding the Middle in One Pass

A simple way to solve this would be to first go through the entire list just to count the number of nodes, `n`. Then, you could calculate the middle index and start a second pass from the head to find and delete that node. However, this is inefficient as it requires two passes.

The key insight for a more optimal solution is to use the **"Tortoise and Hare" (slow and fast pointer)** algorithm. This clever technique allows us to find the middle of the list in a **single pass**.

### The Logic of Deletion

To delete a node from a singly linked list, you can't just access the node itself. You need a pointer to the node that comes **just before it**. Let's call this the `prev` node. The deletion is performed by "skipping over" the middle node: `prev.next = middle_node.next`.

Therefore, our algorithm must not only find the middle node but also keep track of its predecessor.

## Solution Approach

This solution uses the "Tortoise and Hare" algorithm. We use a `fast` pointer that moves two steps at a time and a `slow` pointer that moves one step. By the time the `fast` pointer reaches the end, the `slow` pointer will be at the middle. We also maintain a `prev` pointer that always lags one step behind `slow`.

```python
from typing import Optional

class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Edge Case: If the list has 0 or 1 nodes, deleting the middle
        # results in an empty list.
        if not head or not head.next:
            return None
        
        # Initialize three pointers.
        # 'prev' will track the node just before 'slow'.
        prev = None
        # 'slow' and 'fast' start at the head.
        slow = head
        fast = head
        
        # Loop until the 'fast' pointer reaches the end of the list.
        while fast and fast.next:
            # First, update prev to be where slow is now.
            prev = slow
            # Then, advance slow and fast.
            slow = slow.next
            fast = fast.next.next
            
        # At this point, 'slow' is the middle node and 'prev' is the one before it.
        # We delete the middle node by linking 'prev' to the node after 'slow'.
        prev.next = slow.next
        
        return head
```

## Detailed Code Analysis

### Step 1: The Edge Case

```python
if not head or not head.next:
    return None
```

  - This handles lists of size 0 or 1.
  - If `head` is `None` (size 0), `not head` is true.
  - If `head` has one node (size 1), `head.next` is `None`, so `not head.next` is true.
  - In both cases, deleting the "middle" node leaves an empty list, so we correctly return `None`.

### Step 2: Pointer Initialization

```python
prev = None
slow = head
fast = head
```

  - We initialize all our pointers. `slow` and `fast` start together at the beginning. `prev` starts at `None`, as there is no node before the head.

### Step 3: The Main Loop (The "Race")

```python
while fast and fast.next:
    prev = slow
    slow = slow.next
    fast = fast.next.next
```

  - **`while fast and fast.next:`**: This loop condition is crucial. It ensures that it's always safe to advance the `fast` pointer two steps (`fast.next.next`). If `fast` becomes `None` (for odd-length lists) or `fast.next` becomes `None` (for even-length lists), the loop terminates.
  - **`prev = slow`**: Before `slow` moves, we update `prev` to point to the current location of `slow`. This ensures `prev` always lags one step behind.
  - **`slow = slow.next`**: The "tortoise" moves one step forward.
  - **`fast = fast.next.next`**: The "hare" moves two steps forward.

### Step 4: The Deletion

```python
prev.next = slow.next
```

  - When the loop finishes, `slow` is pointing at the middle node we want to delete.
  - `prev` is pointing at the node right before it.
  - This line performs the deletion by "re-wiring" the link. `prev`'s `next` pointer is changed to skip over `slow` and point directly to whatever `slow` was pointing at. The `slow` node is now effectively orphaned from the list.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `head = [1, 3, 4, 7, 1, 2, 6]` with extreme detail.

### Initial State

```
prev         slow / fast
 |              |
None         [1] -> [3] -> [4] -> [7] -> [1] -> [2] -> [6] -> None
```

-----

### **Loop 1**

1.  **`prev = slow`**: `prev` now points to `Node(1)`.
2.  **`slow = slow.next`**: `slow` now points to `Node(3)`.
3.  **`fast = fast.next.next`**: `fast` moves two steps to `Node(4)`.
    **State after Loop 1:**

<!-- end list -->

```
       prev   slow         fast
        |      |            |
None   [1] -> [3] -> [4] -> [7] -> [1] -> [2] -> [6] -> None
```

-----

### **Loop 2**

1.  **`prev = slow`**: `prev` now points to `Node(3)`.
2.  **`slow = slow.next`**: `slow` now points to `Node(4)`.
3.  **`fast = fast.next.next`**: `fast` moves two steps to `Node(1)`.
    **State after Loop 2:**

<!-- end list -->

```
              prev   slow                     fast
               |      |                        |
None   [1] -> [3] -> [4] -> [7] -> [1] -> [2] -> [6] -> None
```

-----

### **Loop 3**

1.  **`prev = slow`**: `prev` now points to `Node(4)`.
2.  **`slow = slow.next`**: `slow` now points to `Node(7)`. **This is the middle node.**
3.  **`fast = fast.next.next`**: `fast` moves two steps to `Node(6)`.
    **State after Loop 3:**

<!-- end list -->

```
                     prev   slow                           fast
                      |      |                              |
None   [1] -> [3] -> [4] -> [7] -> [1] -> [2] -> [6] -> None
```

-----

### **End of Loop**

  - The `while fast and fast.next:` condition is checked. `fast` is `Node(6)`, but `fast.next` is `None`. The condition is false, and the loop terminates.

### **Final Deletion Step**

  - At this point:
      - `prev` is pointing to `Node(4)`.
      - `slow` is pointing to `Node(7)`.
  - The code executes `prev.next = slow.next`.
  - `slow.next` is `Node(1)`.
  - So, `Node(4).next` is set to `Node(1)`.
  - **The link now looks like this:** `... [4] -> [1] ...`, effectively skipping over and deleting `Node(7)`.

The final list is `[1, 3, 4, 1, 2, 6]`. The function returns the original `head`, which still points to `Node(1)`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes. The slow and fast pointers traverse the list a single time.

### Space Complexity: O(1)

  - We only use three pointers (`prev`, `slow`, `fast`). The space required is constant and does not grow with the size of the list.