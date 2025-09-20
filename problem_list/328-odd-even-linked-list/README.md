# 328\. Odd Even Linked List - Solution Explanation

## Problem Overview

You are given the `head` of a singly linked list. The task is to reorder the list by grouping all the nodes with **odd indices** together, followed by all the nodes with **even indices**. The original relative order within the odd and even groups must be preserved.

**Key Definitions:**

  - **Odd/Even Indices**: This refers to the node's position, not its value. The first node is considered odd (position 1), the second is even (position 2), the third is odd, and so on.
  - **In-place**: The solution must modify the existing linked list without creating any new `ListNode` objects.
  - **Complexity**: The solution must have `O(1)` extra space complexity and `O(n)` time complexity.

**Examples:**

```python
Input: head = [1,2,3,4,5]
# Odd nodes: 1, 3, 5
# Even nodes: 2, 4
# Result: [1,3,5,2,4]

Input: head = [2,1,3,5,6,4,7]
# Odd nodes: 2, 3, 6, 7
# Even nodes: 1, 5, 4
# Result: [2,3,6,7,1,5,4]
```

## Key Insights

### In-Place Re-wiring

The strict `O(1)` space constraint is the biggest clue. It tells us that we cannot create new lists or nodes to store the result. The only way to solve this is to **re-wire the `next` pointers** of the existing nodes.

### Two Interwoven Lists

The most intuitive way to think about this is to see the original list as two separate lists that are interwoven.

  - An "odd list" starting at `head`.
  - An "even list" starting at `head.next`.

Our goal is to "un-weave" them into two distinct, continuous chains and then link the end of the odd chain to the start of the even chain.

### Tracking Heads and Tails

To manage these two chains as we build them, we need pointers.

  - We need to save the head of the even list (`even_head`) because it will be the starting point of the second half of our final list.
  - We need a pointer to the current tail of the odd list (`odd_tail`) so we know where to attach the next odd node.
  - We need a pointer to the current tail of the even list (`even_tail`) so we know where to attach the next even node.

## Solution Approach

This solution iterates through the list, using `odd_tail` and `even_tail` pointers to build the two chains in a single pass. After the list is fully partitioned, it connects the tail of the odd chain to the head of the even chain.

```python
from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Handle edge cases: A list with 0, 1, or 2 nodes is already sorted.
        if not head or not head.next or not head.next.next:
            return head
        
        # Pointers for the tail of the odd list and the head/tail of the even list.
        odd_tail = head
        even_head = head.next
        even_tail = head.next
        
        # Loop as long as there is a valid even node and an odd node after it.
        while even_tail and even_tail.next:
            # 1. Link the next odd node to the end of the odd chain.
            odd_tail.next = even_tail.next
            
            # 2. Move the odd_tail pointer forward to this new end.
            odd_tail = odd_tail.next
            
            # 3. Link the next even node to the end of the even chain.
            even_tail.next = odd_tail.next
            
            # 4. Move the even_tail pointer forward to this new end.
            even_tail = even_tail.next
            
        # 5. Connect the end of the odd list to the beginning of the even list.
        odd_tail.next = even_head
        
        return head
```

## Detailed Code Analysis

### Step 1: Initialization

```python
odd_tail = head
even_head = head.next
even_tail = head.next
```

  - `odd_tail`: This pointer starts at the first node, which is the beginning of our odd chain. We will extend the list from this point.
  - `even_head`: We **must** save a reference to the second node. This is the starting point of our even chain, and we will need it at the very end to connect the two lists.
  - `even_tail`: This pointer starts at the second node and will be used to build the even chain.

### Step 2: The Loop Condition

```python
while even_tail and even_tail.next:
```

  - This condition is crucial. It ensures that there are at least two more nodes in the list to process: an even node (`even_tail`) and the odd node that follows it (`even_tail.next`). If either of these is `None`, we have reached the end of the list and can stop the re-wiring process.

### Step 3: The "Pointer Weave" (Inside the loop)

This is the core of the algorithm, a four-step "dance" of pointers.

```python
# 1. Link the next odd node to the end of the odd chain.
odd_tail.next = even_tail.next
```

  - The next odd node is always the one right after the current even tail. This line detaches it from the even tail and links it to the current odd tail.

<!-- end list -->

```python
# 2. Move the odd_tail pointer forward to this new end.
odd_tail = odd_tail.next
```

  - We advance our `odd_tail` pointer to the node we just added, as it is now the new end of the odd chain.

<!-- end list -->

```python
# 3. Link the next even node to the end of the even chain.
even_tail.next = odd_tail.next
```

  - After the previous step, `odd_tail.next` points to the next available even node. This line links the current `even_tail` to it, skipping over the odd node we just moved.

<!-- end list -->

```python
# 4. Move the even_tail pointer forward to this new end.
even_tail = even_tail.next
```

  - We advance our `even_tail` pointer to the node we just added, as it is now the new end of the even chain.

### Step 4: The Final Connection

```python
odd_tail.next = even_head
```

  - After the loop finishes, the `odd_tail` is pointing to the very last node in the re-ordered odd chain. We set its `next` pointer to the `even_head` we saved at the beginning. This connects the two chains into one final list.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `head = [1, 2, 3, 4, 5]` with extreme detail.

### Initial State

  - `odd_tail` -\> `Node(1)`
  - `even_head` -\> `Node(2)`
  - `even_tail` -\> `Node(2)`
  - **List**: `1 -> 2 -> 3 -> 4 -> 5 -> None`

-----

### **Loop 1**

  - **Condition**: `even_tail` (2) and `even_tail.next` (3) are valid. The loop runs.

<!-- end list -->

1.  **`odd_tail.next = even_tail.next`**: `Node(1).next` is set to `Node(3)`.
      - *Odd chain is now `1 -> 3`.* The original link `1 -> 2` is broken.
2.  **`odd_tail = odd_tail.next`**: `odd_tail` moves forward to `Node(3)`.
3.  **`even_tail.next = odd_tail.next`**: `Node(2).next` is set to `Node(3).next`, which is `Node(4)`.
      - *Even chain is now `2 -> 4`.* The original link `2 -> 3` is broken.
4.  **`even_tail = even_tail.next`**: `even_tail` moves forward to `Node(4)`.

**State After Loop 1:**

  - `odd_tail` -\> `Node(3)`
  - `even_tail` -\> `Node(4)`
  - **Odd Chain**: `1 -> 3`
  - **Even Chain**: `2 -> 4`
  - **Links**: `...3 -> 4 -> 5...`

-----

### **Loop 2**

  - **Condition**: `even_tail` (4) and `even_tail.next` (5) are valid. The loop runs.

<!-- end list -->

1.  **`odd_tail.next = even_tail.next`**: `Node(3).next` is set to `Node(5)`.
      - *Odd chain is now `1 -> 3 -> 5`.* The link `3 -> 4` is broken.
2.  **`odd_tail = odd_tail.next`**: `odd_tail` moves forward to `Node(5)`.
3.  **`even_tail.next = odd_tail.next`**: `Node(4).next` is set to `Node(5).next`, which is `None`.
      - *Even chain is now `2 -> 4 -> None`.* The link `4 -> 5` is broken.
4.  **`even_tail = even_tail.next`**: `even_tail` moves forward to `None`.

**State After Loop 2:**

  - `odd_tail` -\> `Node(5)`
  - `even_tail` -\> `None`
  - **Odd Chain**: `1 -> 3 -> 5`
  - **Even Chain**: `2 -> 4 -> None`

-----

### **End of Loop**

  - **Condition**: `while even_tail` is now `False`. The loop terminates.

### **Final Connection**

  - The code executes `odd_tail.next = even_head`.
  - `Node(5).next` is set to point to `Node(2)` (which was saved as `even_head`).

### **Final Result**

  - The final, single list is now: `1 -> 3 -> 5 -> 2 -> 4 -> None`.
  - The function returns the original `head` (`Node(1)`).

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the list. We traverse the list with our pointers in a single pass.

### Space Complexity: O(1)

  - The reordering is done in-place. We only use a few extra pointers (`odd_tail`, `even_tail`, `even_head`). The space required is constant and does not grow with the size of the list.