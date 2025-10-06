# 61\. Rotate List - Solution Explanation

## Problem Overview

You are given the `head` of a singly linked list and an integer `k`. The task is to **rotate the list to the right** by `k` places. This means the last `k` nodes of the list move to the beginning, and the rest of the nodes follow.

**Examples:**

```python
Input: head = [1,2,3,4,5], k = 2
Output: [4,5,1,2,3]
Explanation:
- Rotate 1 step: [5,1,2,3,4]
- Rotate 2 steps: [4,5,1,2,3]

Input: head = [0,1,2], k = 4
Output: [2,0,1]
Explanation: Rotating a list of length 3 by 4 steps is the same as rotating it by 1 step.
```

## Key Insights

### 1\. The `k` Can Be Huge

The constraint `0 <= k <= 2 * 10^9` is a massive hint. A naive approach of rotating the list one step at a time, `k` times, would be far too slow.

The key insight is that rotating a list of length `L` by `L` steps results in the original list. Therefore, we only care about the remainder of `k` divided by `L`. The effective number of rotations is `k % L`. This reduces the problem to a manageable number of rotations.

### 2\. The "Circular List" Trick

The second key insight is how to perform the rotation in a single pass. A rotation can be thought of as:

1.  Finding the last node.
2.  Connecting the last node's `next` pointer back to the original `head`, forming a **circle**.
3.  Finding the new "tail" of the list.
4.  "Cutting" the list at this new tail by setting its `next` pointer to `None`.

The node immediately after the new tail becomes the new head of the list. This "make it a circle and cut it" approach is very efficient.

## Solution Approach

This solution implements the "circular list" strategy. It first traverses the list to find its length and tail. Then, it forms a circle, calculates the position of the new tail, and breaks the circle at the correct spot to form the new, rotated list.

```python
from typing import Optional

class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # Step 1: Handle edge cases.
        if not head or not head.next or k == 0:
            return head
            
        # Step 2: Find the length and the tail of the list.
        length = 1
        tail = head
        while tail.next:
            tail = tail.next
            length += 1
            
        # Step 3: Calculate the effective rotation and form a circle.
        k = k % length
        if k == 0:
            return head # If k is a multiple of length, no rotation is needed.
        tail.next = head
        
        # Step 4: Find the new tail of the list.
        # The new tail is at position (length - k - 1) from the start.
        steps_to_new_tail = length - k - 1
        new_tail = head
        for _ in range(steps_to_new_tail):
            new_tail = new_tail.next
            
        # Step 5: Find the new head and break the circle.
        new_head = new_tail.next
        new_tail.next = None
        
        return new_head
```

## Detailed Code Analysis

### Step 1: Edge Cases

```python
if not head or not head.next or k == 0:
    return head
```

  - `not head`: If the list is empty, there's nothing to rotate.
  - `not head.next`: If the list has only one node, rotating it does nothing.
  - `k == 0`: If we don't need to rotate, we can return immediately.

### Step 2: Find Length and Tail

```python
length = 1
tail = head
while tail.next:
    tail = tail.next
    length += 1
```

  - This is a standard single pass to find the end of the list.
  - We start `length` at `1` (for the head node).
  - The loop continues until `tail.next` is `None`, which means `tail` is the last node.
  - When this loop finishes, `length` holds the total number of nodes, and `tail` points to the last node.

### Step 3: Handle `k` and Form the Circle

```python
k = k % length
if k == 0:
    return head
tail.next = head
```

  - `k = k % length`: This is the crucial step to handle large `k` values. It calculates the effective number of rotations.
  - `if k == 0:`: If the effective `k` is 0 (meaning the original `k` was a multiple of the list length), no rotation is needed. We can return the original `head`.
  - `tail.next = head`: This is the "magic" step. We connect the `next` pointer of the original last node (`tail`) to the original first node (`head`), forming a closed loop or circle.

### Step 4: Find the New Tail

```python
steps_to_new_tail = length - k - 1
new_tail = head
for _ in range(steps_to_new_tail):
    new_tail = new_tail.next
```

  - **The Logic**: If we rotate right by `k` spots, the `k`-th node from the original end becomes the new head. The node just before it becomes the new tail. The position of this new tail is `length - k` nodes from the start (1-indexed), which means it's at index `length - k - 1` (0-indexed).
  - `steps_to_new_tail = length - k - 1`: We calculate the number of steps we need to take from the start to reach the node that will become the new tail.
  - The `for` loop simply advances a pointer, `new_tail`, from the `head` for the required number of steps.

### Step 5: Cut the Circle and Return

```python
new_head = new_tail.next
new_tail.next = None
return new_head
```

  - `new_head = new_tail.next`: The node immediately after our `new_tail` is the start of the rotated part, so it becomes the `new_head`.
  - `new_tail.next = None`: This is the "cut." We break the circular link by setting the `next` pointer of our `new_tail` to `None`, which correctly terminates the list.
  - `return new_head`: We return the new head of our correctly rotated list.

## Step-by-Step Execution Trace

Let's trace `head = [1,2,3,4,5]` and `k = 2` with extreme detail.

### **Phase 1: Find Length and Tail**

  - Start: `length = 1`, `tail` -\> Node(1).
  - Loop 1: `tail` -\> Node(2), `length` -\> 2.
  - Loop 2: `tail` -\> Node(3), `length` -\> 3.
  - Loop 3: `tail` -\> Node(4), `length` -\> 4.
  - Loop 4: `tail` -\> Node(5), `length` -\> 5.
  - Loop ends. **`length = 5`**, **`tail` is `Node(5)`**.

### **Phase 2: Handle `k` and Form Circle**

  - `k = k % length` -\> `k = 2 % 5` -\> `k` is still `2`.
  - `k` is not 0.
  - `tail.next = head`: `Node(5).next` is set to point to `Node(1)`.
  - **List is now a circle**: `1 -> 2 -> 3 -> 4 -> 5 -> 1 ...`

### **Phase 3: Find New Tail**

  - `steps_to_new_tail = length - k - 1` -\> `5 - 2 - 1` = **2**.
  - We need to move 2 steps from the head.
  - Start: `new_tail` -\> `Node(1)`.
  - Loop 1: `new_tail` -\> `Node(2)`.
  - Loop 2: `new_tail` -\> `Node(3)`.
  - Loop ends. **`new_tail` is `Node(3)`**.

### **Phase 4: Cut and Finalize**

  - `new_head = new_tail.next`: `new_head` becomes `Node(3).next`, which is **`Node(4)`**.
  - `new_tail.next = None`: `Node(3).next` is set to **`None`**. This breaks the circle.
  - The link `3 -> 4` is now `3 -> None`.
  - The list starting from `new_head` is `4 -> 5 -> 1 -> 2 -> 3 -> None`.

### **Final Result**

  - The function returns `new_head`, which points to `Node(4)`.
  - The final list is `[4, 5, 1, 2, 3]`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the list. The algorithm consists of two main traversals of the list (one to find the length, one to find the new tail), both of which are linear. The total time is `O(n) + O(n) = O(n)`.

### Space Complexity: O(1)

  - All operations are done by re-wiring pointers in-place. We only use a few extra variables (`tail`, `new_tail`, etc.), so the space required is constant.