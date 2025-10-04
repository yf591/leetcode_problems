# 19\. Remove Nth Node From End of List - Solution Explanation

## Problem Overview

You are given the `head` of a singly linked list and an integer `n`. The task is to remove the **n-th node from the end** of the list and return the head of the modified list.

**Example:**

  - **Input:** `head = [1,2,3,4,5]`, `n = 2`
  - **Explanation**: The 2nd node from the end is the node with value `4`. Removing it results in the list `[1,2,3,5]`.
  - **Output:** `[1,2,3,5]`

## Key Insights

### The Challenge: Finding the "End"

The core difficulty is that in a singly linked list, you can only move forward. You don't know where the "end" is until you've traversed the entire list, which makes finding the "n-th from the end" tricky.

### The Two-Pass Approach (Simple but Inefficient)

A straightforward way to solve this is:

1.  **First Pass**: Traverse the entire list once just to count its total length, let's call it `L`.
2.  **Calculation**: The n-th node from the end is at index `L - n` from the beginning (0-indexed). To delete it, we need to stop at the node *before* it, which is at index `L - n - 1`.
3.  **Second Pass**: Traverse the list again from the head, stopping at the `(L - n - 1)`-th node to perform the deletion.
    This works, but it requires two full passes over the list. The follow-up question in many interviews is, "Can you do it in one pass?"

### The One-Pass Insight: The "Gap" Method

The key to a single-pass solution is the **two-pointer technique**. We can use a `slow` and a `fast` pointer to solve this efficiently.

1.  Imagine two pointers, `slow` and `fast`, both starting at the beginning.
2.  First, we move the `fast` pointer `n` steps ahead. Now there is a "gap" of `n` nodes between `slow` and `fast`.
3.  Next, we move **both pointers in tandem**, one step at a time, until the `fast` pointer reaches the very end of the list.
4.  Because we maintained a constant gap of `n` nodes, when `fast` is at the end, `slow` will be pointing exactly at the n-th node from the end (or the node just before it, depending on how we set up the gap).

To make deletion easy, it's best to have the `slow` pointer land on the node *before* the one we want to delete. We can achieve this by creating an initial gap of `n + 1`.

### The Dummy Node Trick

What if we need to remove the first node of the list (e.g., `head = [1,2,3]`, `n=3`)? The node to delete is the head, but there is no node *before* the head to modify. This edge case can make the code complicated. A very common and elegant solution is to create a `dummy` node that points to the original `head`. This ensures that every node in the list, including the original head, has a predecessor, simplifying the logic immensely.

## Solution Approach

This solution implements the efficient one-pass, two-pointer approach, using a `dummy` node to gracefully handle all edge cases.

```python
from typing import Optional

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # Create a dummy node that points to the head.
        dummy = ListNode(0, head)
        
        # Initialize two pointers, both starting at the dummy node.
        slow = dummy
        fast = dummy
        
        # 1. Advance the 'fast' pointer n + 1 steps ahead.
        for _ in range(n + 1):
            fast = fast.next
            
        # 2. Move both pointers in tandem until 'fast' reaches the end (None).
        while fast:
            slow = slow.next
            fast = fast.next
            
        # 3. 'slow' is now at the predecessor of the target node.
        #    Delete the target node by re-wiring the 'next' pointer.
        slow.next = slow.next.next
        
        # The dummy's 'next' will be the head of the modified list.
        return dummy.next
```

## Detailed Code Analysis

### Step 1: The Dummy Node

```python
dummy = ListNode(0, head)
slow = dummy
fast = dummy
```

  - We create a `dummy` node and link it to our list's `head`. The list is now conceptually `dummy -> head -> ...`.
  - We initialize **both** `slow` and `fast` pointers to this `dummy` node. This gives us a stable anchor point before the start of the actual list.

### Step 2: Creating the Gap

```python
for _ in range(n + 1):
    fast = fast.next
```

  - This loop's only job is to move the `fast` pointer ahead.
  - **Why `n + 1` steps?** This is the crucial detail. By moving it `n+1` steps, when `fast` eventually reaches the end of the list (`None`), `slow` will be positioned perfectly at the node **just before** the one we need to delete.
      - If we only moved `n` steps, `slow` would land directly on the node to be deleted, and we would have lost the reference to its predecessor.

### Step 3: Moving in Tandem

```python
while fast:
    slow = slow.next
    fast = fast.next
```

  - This loop starts after the initial gap has been created.
  - In each iteration, both `slow` and `fast` advance by one node. This maintains the constant gap between them.
  - The loop terminates when `fast` becomes `None`, meaning it has moved one step past the last node of the list.

### Step 4: The Deletion

```python
slow.next = slow.next.next
```

  - Because of our `n+1` gap, the `slow` pointer is now guaranteed to be the node immediately preceding the target node.
  - `slow.next` is the target node we want to remove.
  - `slow.next.next` is the node *after* the target node.
  - This line performs the deletion by "skipping over" the target node. The `slow` node's `next` pointer is re-wired to point directly to the node after the target, effectively removing the target from the list.

### Step 5: The Return

```python
return dummy.next
```

  - We return `dummy.next`, not `head`. This correctly handles the edge case where the original `head` itself was the node to be removed. In that case, `slow` would have remained at the `dummy` node, and `dummy.next` would have been correctly re-wired to the second node of the original list.

## Step-by-Step Execution Trace

Let's trace the algorithm with `head = [1,2,3,4,5]` and `n = 2` with extreme detail.

### **Initial State:**

  - The list is conceptually: `Dummy(0) -> 1 -> 2 -> 3 -> 4 -> 5 -> None`
  - `slow` points to `Dummy(0)`.
  - `fast` points to `Dummy(0)`.

-----

### **1. Creating the Gap (`n+1 = 3` steps)**

  - **Loop 1**: `fast` moves to `Node(1)`.
  - **Loop 2**: `fast` moves to `Node(2)`.
  - **Loop 3**: `fast` moves to `Node(3)`.

**State After Gap Creation:**

```
slow            fast
 |               |
 D -> 1 -> 2 -> 3 -> 4 -> 5 -> None
```

-----

### **2. Moving in Tandem**

  - The `while fast:` loop begins.

| Iteration | `fast` Position (at start) | Action | `slow` Position (at end) | `fast` Position (at end) |
| :--- | :--- | :--- | :--- | :--- |
| **1** | `Node(3)` | `slow`-\>`1`, `fast`-\>`4` | `Node(1)` | `Node(4)` |
| **2** | `Node(4)` | `slow`-\>`2`, `fast`-\>`5` | `Node(2)` | `Node(5)` |
| **3** | `Node(5)` | `slow`-\>`3`, `fast`-\>`None` | `Node(3)` | `None` |

  - The loop terminates because `fast` is now `None`.

**State Before Deletion:**

```
            slow
             |
 D -> 1 -> 2 -> 3 -> 4 -> 5 -> None
```

  - `slow` is at `Node(3)`. This is the node just before the target node (Node 4).

-----

### **3. The Deletion**

  - The code executes `slow.next = slow.next.next`.
  - `slow.next` is currently `Node(4)`.
  - `slow.next.next` is `Node(5)`.
  - The line becomes: `Node(3).next = Node(5)`.
  - The pointer from `3` now skips `4` and points directly to `5`. `Node(4)` is orphaned.

### **Final List State:**

```
 D -> 1 -> 2 -> 3 -> 5 -> None
```

### **4. Return Value**

  - The function returns `dummy.next`, which is `Node(1)`, the head of the final, correct list.

## Performance Analysis

### Time Complexity: O(L)

  - Where `L` is the number of nodes in the list. The algorithm traverses the list in a single pass.

### Space Complexity: O(1)

  - We only use a few extra pointers (`dummy`, `slow`, `fast`). The space required is constant and does not depend on the size of the list.