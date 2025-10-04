# 92\. Reverse Linked List II - Solution Explanation

## Problem Overview

You are given the `head` of a singly linked list and two 1-indexed integers, `left` and `right`. The task is to reverse the portion of the list from the `left`-th node to the `right`-th node and return the head of the modified list.

**Key Constraints:**

  - The reversal must be done **in-place** in a single pass.
  - `left` and `right` are 1-indexed positions.

**Example:**

  - **Input:** `head = [1,2,3,4,5]`, `left = 2`, `right = 4`
  - **Sublist to reverse:** `[2,3,4]`
  - **Reversed sublist:** `[4,3,2]`
  - **Final Output:** `[1,4,3,2,5]`

## Key Insights

### The Challenge of In-Place Reversal

The main challenge is to reverse a *segment* of the list while keeping the connections to the rest of the list intact. This requires carefully managing the "entry" and "exit" points of the sublist.

  - The node *before* the sublist (at position `left-1`) must be re-linked to the *new head* of the reversed sublist (the original `right`-th node).
  - The original start of the sublist (the `left`-th node) will become the *new tail* of the reversed sublist, and it must be re-linked to the node that was originally *after* the sublist.

### An Elegant Iterative Approach

Instead of a standard three-pointer reversal on a detached sublist, there is a more elegant, in-place solution. The core idea is to "pin" the node at the `left`-th position and then, one by one, move each subsequent node in the sublist to the very front of the sublist.

Think of it like moving cards in your hand. If you want to reverse `[2, 3, 4]`:

1.  Keep `2` as an anchor.
2.  Take `3` and move it to the front: `[3, 2, 4]`.
3.  Take `4` and move it to the front: `[4, 3, 2]`.

### The Dummy Node Trick

A common problem in linked list manipulations is handling edge cases, especially when the modification starts at the head of the list (`left = 1`). To simplify the code, we can create a `dummy` node that points to the original `head`. This ensures that every sublist, even one starting at the head, has a node `prev` before it, which makes the logic consistent for all cases.

## Solution Approach

This solution first advances a pointer `prev` to the node just before the reversal section begins. It then performs the reversal for the required number of steps by repeatedly moving the node after the `start` of the sublist to the position just after `prev`.

```python
from typing import Optional

class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        # Handle edge cases where no reversal is needed.
        if not head or left == right:
            return head
            
        # Use a dummy node to simplify handling the case where left=1.
        dummy = ListNode(0, head)
        # 'prev' will point to the node just before the reversal section.
        prev = dummy
        
        # 1. Move 'prev' to the (left - 1)-th node.
        for _ in range(left - 1):
            prev = prev.next
            
        # 2. Initialize pointers for the reversal.
        # 'start' is the first node of the sublist to be reversed (the anchor).
        start = prev.next
        # 'then' is the node that we will repeatedly move to the front.
        then = start.next
        
        # 3. Perform the reversal 'right - left' times.
        for _ in range(right - left):
            # The four-step pointer dance to move 'then'
            start.next = then.next
            then.next = prev.next
            prev.next = then
            # Reset 'then' for the next iteration.
            then = start.next
            
        return dummy.next
```

## Detailed Code Analysis

### Step 1: Finding the Predecessor Node

```python
dummy = ListNode(0, head)
prev = dummy
for _ in range(left - 1):
    prev = prev.next
```

  - We create a `dummy` node. Now `dummy.next` is our head.
  - We advance `prev` `left - 1` times. At the end of this loop, `prev` will be at the node right before our reversal section starts. For `left = 2`, it will move once and stop at `Node(1)`.

### Step 2: Setting up Reversal Pointers

```python
start = prev.next
then = start.next
```

  - `start`: This is the first node *inside* our reversal section (e.g., `Node(2)`). This node will be our "anchor." It will eventually become the tail of the reversed section.
  - `then`: This is the first node we are going to move (e.g., `Node(3)`).

### Step 3: The Reversal Loop and the "Pointer Dance"

```python
for _ in range(right - left):
    start.next = then.next
    then.next = prev.next
    prev.next = then
    then = start.next
```

  - This loop runs `right - left` times, which is the exact number of nodes we need to move.
  - Inside the loop is a four-step "dance" that moves the `then` node to become the new head of our sublist. Let's analyze one iteration in extreme detail.

**A Single Iteration of the "Dance":**

1.  **`start.next = then.next`**: The anchor `start` must skip over `then` to connect to the rest of the list. This detaches `then`.
2.  **`then.next = prev.next`**: `then` needs to point to the current head of the reversed section. `prev.next` is always pointing at that head.
3.  **`prev.next = then`**: `prev` must now connect to `then`, officially making `then` the new head of the reversed section.
4.  **`then = start.next`**: We reset `then` for the next iteration. `start.next` now points to the *new* next node that needs to be moved.

## Step-by-Step Execution Trace (Visualized)

Let's trace the algorithm with `head = [1,2,3,4,5]`, `left = 2`, `right = 4`.

### **Initial State:**

  - `prev` moves `left-1=1` time, stopping at `Node(1)`.
  - `start` is `prev.next` -\> `Node(2)`.
  - `then` is `start.next` -\> `Node(3)`.
  - The loop will run `right-left = 4-2 = 2` times.

**Initial Pointers:**

```
            start  then
              |      |
D -> 1(prev) -> 2 -> 3 -> 4 -> 5 -> None
```

-----

### **Reversal Loop - Iteration 1**

1.  **`start.next = then.next`**: `Node(2)` skips `Node(3)` and points to `Node(4)`.
      - `1(prev) -> 2(start) -> 4...`
      - `3(then)` is now detached, pointing to `4`.
2.  **`then.next = prev.next`**: `Node(3)` now points to what `prev` points to, which is `Node(2)`.
      - `3(then) -> 2(start)`
3.  **`prev.next = then`**: `Node(1)` now points to `Node(3)`.
      - `1(prev) -> 3(then)`
4.  **`then = start.next`**: Reset `then` for the next iteration. It becomes `start.next`, which is now `Node(4)`.

**State after Iteration 1:**

```
                   start  then
                     |      |
D -> 1(prev) -> 3 -> 2 -> 4 -> 5 -> None
```

-----

### **Reversal Loop - Iteration 2**

1.  **`start.next = then.next`**: `Node(2)` skips `Node(4)` and points to `Node(5)`.
      - `... 3 -> 2(start) -> 5...`
      - `4(then)` is now detached, pointing to `5`.
2.  **`then.next = prev.next`**: `Node(4)` now points to what `prev` points to, which is `Node(3)`.
      - `4(then) -> 3`
3.  **`prev.next = then`**: `Node(1)` now points to `Node(4)`.
      - `1(prev) -> 4(then)`
4.  **`then = start.next`**: Reset `then`. It becomes `start.next`, which is now `Node(5)`.

**State after Iteration 2:**

```
                          start  then
                            |      |
D -> 1(prev) -> 4 -> 3 -> 2 -> 5 -> None
```

-----

### **End of Loop**

  - The loop has run 2 times and finishes.

### **Final Result**

  - The function returns `dummy.next`, which is `Node(1)`.
  - The final, fully connected list is `1 -> 4 -> 3 -> 2 -> 5 -> None`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes. We traverse to the `left-1` position once (`O(left)`), and then the reversal loop runs `right - left` times with constant `O(1)` work inside. The total time is `O(n)`.

### Space Complexity: O(1)

  - The reversal is done entirely in-place. We only use a few extra pointers (`dummy`, `prev`, `start`, `then`), so the space is constant.