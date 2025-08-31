# 206\. Reverse Linked List - Solution Explanation

## Problem Overview

Given the `head` of a singly linked list, the task is to reverse the list and return the new head.

**Reversal Definition:**
The process involves re-wiring the pointers of the list so that each node points to its previous node instead of its next node. The last node of the original list will become the first node (the new head) of the reversed list.

**Example:**

  - **Input:** `1 -> 2 -> 3 -> None`
  - **Output:** `3 -> 2 -> 1 -> None`

## Key Insights

### Pointer Re-wiring

The core of this problem is not about changing the nodes' values, but about changing their `next` pointers. For any given node in the list, its `next` pointer must be changed to point to the node that came *before* it.

### The "Lost Link" Problem

The main challenge is that a linked list is a one-way street. As you stand on a node, you only know what's in front of you (`node.next`).

  - Imagine you are at `Node 2` in the list `1 -> 2 -> 3`.
  - You want to make `2.next` point to `1`.
  - But the moment you do that, you have lost your only connection to `Node 3`\!

To solve this, we must save a reference to the next node *before* we reverse the pointer. This requires keeping track of three nodes as we iterate: the **previous**, the **current**, and the **next**.

## Solution Approach

This solution iterates through the linked list one node at a time, performing a "three-step pointer dance" to reverse the links without losing the rest of the list.

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # We need two main pointers:
        # prev_node starts as None, because the original head will be the new tail.
        prev_node = None
        # current_node starts at the beginning of the list.
        current_node = head
        
        # We loop as long as there is a node to process.
        while current_node:
            # --- The Pointer Dance ---
            # 1. Save the next node before we break the link.
            next_temp = current_node.next
            
            # 2. Reverse the pointer of the current node.
            current_node.next = prev_node
            
            # 3. Move our pointers one step forward for the next iteration.
            prev_node = current_node
            current_node = next_temp
            
        # When the loop ends, current_node is None, and prev_node is the new head.
        return prev_node
```

## Detailed Code Analysis

### Step 1: Initialization

```python
prev_node = None
current_node = head
```

  - We initialize `current_node` to `head`, which is our starting point for the traversal.
  - We initialize `prev_node` to `None`. This is critical. After we reverse the first node, it will become the new *tail* of the list, and the tail must point to `None`.

### Step 2: The Loop

```python
while current_node:
```

  - The loop will continue as long as `current_node` is a valid node. It will stop once `current_node` becomes `None`, which happens after we have processed the last node in the original list.

### Step 3: The "Pointer Dance" (Inside the loop)

This is the core logic, a sequence of four operations that must happen in a specific order.

```python
# 1. Save the next node.
next_temp = current_node.next
```

  - This is the most important step. We create a temporary variable `next_temp` to hold the rest of the list. We're about to break the `current_node.next` link, so we need to save this path forward.

<!-- end list -->

```python
# 2. Reverse the current pointer.
current_node.next = prev_node
```

  - Here, we do the actual reversal. The current node's `next` pointer is re-wired to point backward to the `prev_node`.

<!-- end list -->

```python
# 3. Move the 'prev_node' pointer forward.
prev_node = current_node
```

  - For the *next* iteration of the loop, the node we just processed will be the "previous" node. So, we update `prev_node` to point to where `current_node` is.

<!-- end list -->

```python
# 4. Move the 'current_node' pointer forward.
current_node = next_temp
```

  - We move our `current_node` to the next node in the original list, which we safely stored in `next_temp`.

## Step-by-Step Execution Trace (Visualized)

Let's trace this with extreme detail for the input `[1, 2, 3]`.

### Initial State

The list is `1 -> 2 -> 3 -> None`.
Our pointers are:

  - `prev_node`: `None`
  - `current_node`: `Node(1)`

<!-- end list -->

```
prev_node      current_node
   |                |
(None)           Node(1) -> Node(2) -> Node(3) -> None
```

-----

### Loop 1

**1. `next_temp = current_node.next`**

  - We save the rest of the list starting from Node(2).

<!-- end list -->

```
prev_node      current_node    next_temp
   |                |               |
(None)           Node(1) ->      Node(2) -> Node(3) -> None
```

**2. `current_node.next = prev_node`**

  - We reverse the pointer. Node(1) now points to `None`. The link to Node(2) is broken.

<!-- end list -->

```
prev_node      current_node    next_temp
   |                |               |
(None) <- Node(1) (None)         Node(2) -> Node(3) -> None
```

**3. `prev_node = current_node`**

  - We slide our `prev_node` pointer forward.

<!-- end list -->

```
             prev_node
             current_node    next_temp
                  |               |
(None) <-      Node(1)         Node(2) -> Node(3) -> None
```

**4. `current_node = next_temp`**

  - We slide our `current_node` pointer forward using our saved link. The first iteration is complete.

<!-- end list -->

```
           prev_node       current_node
                |               |
(None) <-      Node(1)         Node(2) -> Node(3) -> None
```

-----

### Loop 2

**1. `next_temp = current_node.next`**

  - Save the rest of the list starting from Node(3).

<!-- end list -->

```
           prev_node       current_node    next_temp
                |               |               |
(None) <-      Node(1)         Node(2) ->      Node(3) -> None
```

**2. `current_node.next = prev_node`**

  - Reverse the pointer. Node(2) now points to Node(1).

<!-- end list -->

```
           prev_node       current_node    next_temp
                |               |               |
(None) <-      Node(1) <-      Node(2)         Node(3) -> None
```

**3. `prev_node = current_node`**

  - Slide `prev_node` forward.

<!-- end list -->

```
                       prev_node
                       current_node    next_temp
                            |               |
(None) <-      Node(1) <-      Node(2)         Node(3) -> None
```

**4. `current_node = next_temp`**

  - Slide `current_node` forward. The second iteration is complete.

<!-- end list -->

```
                               prev_node       current_node
                                    |               |
(None) <-      Node(1) <-      Node(2)         Node(3) -> None
```

-----

### Loop 3

**1. `next_temp = current_node.next`**

  - Save the rest of the list, which is now `None`.

<!-- end list -->

```
                               prev_node       current_node    next_temp
                                    |               |               |
(None) <-      Node(1) <-      Node(2)         Node(3) ->      (None)
```

**2. `current_node.next = prev_node`**

  - Reverse the pointer. Node(3) now points to Node(2).

<!-- end list -->

```
                               prev_node       current_node    next_temp
                                    |               |               |
(None) <-      Node(1) <-      Node(2) <-      Node(3)         (None)
```

**3. `prev_node = current_node`**

  - Slide `prev_node` forward. It now points to `Node(3)`, which is the new head.

<!-- end list -->

```
                                               prev_node
                                               current_node    next_temp
                                                    |               |
(None) <-      Node(1) <-      Node(2) <-      Node(3)         (None)
```

**4. `current_node = next_temp`**

  - Slide `current_node` forward. It now becomes `None`.

<!-- end list -->

```
                                               prev_node           current_node
                                                    |                   |
(None) <-      Node(1) <-      Node(2) <-      Node(3)             (None)
```

-----

### End of Loop

  - The `while current_node:` condition is now false, because `current_node` is `None`. The loop terminates.

### Final Step

```python
return prev_node
```

  - The function returns `prev_node`, which is pointing to `Node(3)`, the correct new head of our reversed list.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the list. We iterate through the list exactly once.

### Space Complexity: O(1)

  - We only use a few pointers (`prev_node`, `current_node`, `next_temp`). The space required is constant and does not grow with the size of the list.