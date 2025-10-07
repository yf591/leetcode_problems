# 86\. Partition List - Solution Explanation

## Problem Overview

You are given the `head` of a singly linked list and a value `x`. The task is to reorder the list so that all nodes with values **less than `x`** appear before all nodes with values **greater than or equal to `x`**.

**The Crucial Constraint:**

  - You must **preserve the original relative order** of the nodes within each of the two partitions.

**Examples:**

```python
Input: head = [1,4,3,2,5,2], x = 3
Output: [1,2,2,4,3,5]
Explanation:
- Nodes less than 3 are: 1, 2, 2. Their original order is preserved.
- Nodes greater or equal to 3 are: 4, 3, 5. Their original order is preserved.
- The final list combines these two groups.
```

## Key Insights

### The "Preserve Order" Challenge

The requirement to preserve the original relative order is the most important clue. It suggests that trying to swap nodes in-place within the original list would be extremely complicated and difficult to get right. For example, moving a `2` from the end of the list to the front would involve many complex pointer changes.

### The "Two New Lists" Strategy

A much simpler and cleaner insight is to **build two new, separate lists** as we traverse the original list once.

1.  **A "less than" list**: This list will hold all the nodes with values `< x`.
2.  **A "greater or equal" list**: This list will hold all the nodes with values `>= x`.

As we iterate through the original list, we can detach each node and append it to the tail of the appropriate new list. This naturally preserves the relative order within each group. After we've processed all the nodes, we can simply connect the tail of the "less than" list to the head of the "greater or equal" list to form our final result.

### The "Dummy Head" Trick

When building a new linked list, the code to handle adding the very first node is often different from adding subsequent nodes. To make the code uniform and avoid special `if` checks, we can use a **dummy head** for each of our two new lists. These are placeholder nodes that we will discard at the end. We'll also need **tail pointers** for each list so that we can append new nodes in constant `O(1)` time.

## Solution Approach

This solution implements the "Two New Lists" strategy. It iterates through the original linked list a single time. For each node, it decides which of the two new lists it belongs to and appends it. Finally, it stitches the two lists together.

```python
from typing import Optional

class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        # Step 1: Initialize dummy heads for the two new lists.
        less_head = ListNode()
        greater_head = ListNode()
        
        # Step 2: Initialize tail pointers for building the new lists.
        less_tail = less_head
        greater_tail = greater_head
        
        # Step 3: Traverse the original list with a 'current' pointer.
        current = head
        
        while current:
            # Step 4: Decide which list the current node belongs to.
            if current.val < x:
                # Append it to the 'less' list.
                less_tail.next = current
                less_tail = less_tail.next
            else:
                # Append it to the 'greater or equal' list.
                greater_tail.next = current
                greater_tail = greater_tail.next
            
            # Move to the next node in the original list.
            current = current.next
            
        # Step 5: Terminate the 'greater or equal' list. This is crucial.
        greater_tail.next = None
        
        # Step 6: Connect the 'less' list to the 'greater or equal' list.
        less_tail.next = greater_head.next
        
        # Step 7: The head of our final list is the node after our 'less_head' dummy.
        return less_head.next
```

## Detailed Code Analysis

### Step 1 & 2: Initialization

```python
less_head = ListNode()
greater_head = ListNode()
less_tail = less_head
greater_tail = greater_head
```

  - We create two placeholder nodes, `less_head` and `greater_head`. These will never be part of our final result, but they provide a fixed starting point.
  - We also create two tail pointers, `less_tail` and `greater_tail`, and initialize them to point to their respective dummy heads. These pointers will always point to the last node in each of the lists we are building.

### Step 3 & 4: The Traversal and Partitioning Loop

```python
current = head
while current:
    if current.val < x:
        less_tail.next = current
        less_tail = less_tail.next
    else:
        greater_tail.next = current
        greater_tail = greater_tail.next
    current = current.next
```

  - This is the main loop where we process the original list.
  - For each `current` node:
      - We check its value against `x`.
      - **If `< x`**: We link the end of our "less" list to the `current` node (`less_tail.next = current`) and then update our `less_tail` to be this new node (`less_tail = less_tail.next`).
      - **If `>= x`**: We do the exact same thing for the "greater" list.
  - At the end of each iteration, we advance `current`. It's important to note that we are re-wiring the `next` pointers of the original nodes as we go.

### Step 5: Terminating the Second List

```python
greater_tail.next = None
```

  - This is an **extremely important step**. After the loop, `greater_tail` points to the last node in the "greater or equal" group. This node's original `next` pointer could be pointing to a node that we moved to the "less" list earlier. If we don't sever this link by setting it to `None`, we could create a cycle in our final linked list. This line ensures our final combined list is properly terminated.

### Step 6: Stitching the Lists Together

```python
less_tail.next = greater_head.next
```

  - `less_tail` is currently the last node of the entire "less than" group.
  - `greater_head` is our dummy node for the second list. The *actual* start of the second list is `greater_head.next`.
  - This line connects the end of the first list to the start of the second list, creating our final, partitioned sequence.

### Step 7: Returning the Result

```python
return less_head.next
```

  - `less_head` is our dummy node for the first list. The actual start of our final result is `less_head.next`. We return this.

## Step-by-Step Execution Trace

Let's trace the algorithm with `head = [1, 4, 3, 2, 5, 2]` and `x = 3` with extreme detail.

### **Initial State:**

  - `less_head` -\> `DummyL`
  - `greater_head` -\> `DummyG`
  - `less_tail` -\> `DummyL`
  - `greater_tail` -\> `DummyG`
  - `current` -\> `Node(1)`

| `current` Node | `current.val < 3`?| Action | `less` list state | `greater` list state |
| :--- | :--- | :--- | :--- | :--- |
| **Node(1)** | True | Append to `less` list. `less_tail` moves to `Node(1)`. | `DummyL -> 1` | `DummyG` |
| **Node(4)** | False | Append to `greater` list. `greater_tail` moves to `Node(4)`.| `DummyL -> 1` | `DummyG -> 4` |
| **Node(3)** | False | Append to `greater` list. `greater_tail` moves to `Node(3)`.| `DummyL -> 1` | `DummyG -> 4 -> 3` |
| **Node(2)** | True | Append to `less` list. `less_tail` moves to `Node(2)`. | `DummyL -> 1 -> 2`| `DummyG -> 4 -> 3` |
| **Node(5)** | False | Append to `greater` list. `greater_tail` moves to `Node(5)`.| `DummyL -> 1 -> 2`| `DummyG -> 4 -> 3 -> 5` |
| **Node(2)** | True | Append to `less` list. `less_tail` moves to the second `Node(2)`. | `DummyL -> 1 -> 2 -> 2` | `DummyG -> 4 -> 3 -> 5`|

  - The `while` loop finishes. `current` is now `None`.

### **Final Connection Steps:**

1.  **`greater_tail.next = None`**:

      - `greater_tail` is at `Node(5)`. Its `next` pointer is set to `None`.
      - The `greater` list is now properly terminated: `4 -> 3 -> 5 -> None`.

2.  **`less_tail.next = greater_head.next`**:

      - `less_tail` is at the second `Node(2)`.
      - `greater_head.next` is `Node(4)`.
      - The `next` pointer of the second `Node(2)` is set to `Node(4)`.
      - The two lists are now stitched together.

3.  **`return less_head.next`**:

      - The function returns the node after `DummyL`, which is the first `Node(1)`.

### **Final List Structure:**

`1 -> 2 -> 2 -> 4 -> 3 -> 5 -> None`

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the list. The algorithm iterates through the original list exactly once.

### Space Complexity: O(1)

  - This is a key advantage. We are not creating new copies of the nodes; we are simply re-wiring the `next` pointers of the existing nodes. We only use a few extra pointers (`dummy` nodes, `tail` pointers, `current`), so the extra space is constant.