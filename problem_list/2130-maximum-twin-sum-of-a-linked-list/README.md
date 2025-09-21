# 2130\. Maximum Twin Sum of a Linked List - Solution Explanation

## Problem Overview

You are given the `head` of a singly linked list with an **even** number of nodes. The task is to find the **maximum twin sum**.

**Twin Definition:**
A "twin" relationship pairs nodes symmetrically from the ends of the list.

  - The 1st node (index 0) is the twin of the last node (index `n-1`).
  - The 2nd node (index 1) is the twin of the 2nd-to-last node (index `n-2`).
  - ...and so on.

The **twin sum** is the sum of the values of a node and its twin. The goal is to find the largest of these sums.

**Examples:**

```python
Input: head = [5,4,2,1]
Output: 6
Explanation:
- Twin pair 1: Node 0 (value 5) and Node 3 (value 1). Sum = 6.
- Twin pair 2: Node 1 (value 4) and Node 2 (value 2). Sum = 6.
The maximum sum is 6.

Input: head = [4,2,2,3]
Output: 7
Explanation:
- Twin pair 1: Node 0 (4) and Node 3 (3). Sum = 7.
- Twin pair 2: Node 1 (2) and Node 2 (2). Sum = 4.
The maximum sum is 7.
```

## Key Insights

### The Challenge: Accessing Nodes in Reverse

The main difficulty with a singly linked list is that you can only traverse forward. To find a twin sum, you need to pair a node from the beginning of the list with a node from the end. An `O(1)` space solution requires a way to access the second half of the list in reverse order without creating a new copy.

### The Three-Step "In-Place" Strategy

The key insight is to break the problem down into a sequence of three fundamental linked list operations:

1.  **Find the Middle**: First, we need to find the starting point of the second half of the list. The most efficient way to do this is with the **"Tortoise and Hare" (slow and fast pointer)** algorithm.
2.  **Reverse the Second Half**: Once we have the second half, we can reverse it in-place. This makes the last node of the original list become the first node of our new, reversed second-half list.
3.  **Sum in Parallel**: After the reversal, we have two lists we can easily traverse: the original first half (starting from `head`) and the reversed second half. We can now iterate through them simultaneously, sum the pairs, and find the maximum.

## Solution Approach

This solution implements the three-step "Find Middle, Reverse, and Sum" strategy, which is highly efficient in both time and space.

```python
from typing import Optional

class Solution:
    def pairSum(self, head: Optional[ListNode]) -> int:
        
        # --- Step 1: Find the middle of the linked list ---
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        # 'slow' is now at the head of the second half of the list.
        
        # --- Step 2: Reverse the second half of the list ---
        prev = None
        current = slow
        while current:
            next_temp = current.next
            current.next = prev
            prev = current
            current = next_temp
        # 'prev' is now the new head of the reversed second half.
        
        # --- Step 3: Pair up nodes and find the max twin sum ---
        max_sum = 0
        first_half_head = head
        second_half_head = prev
        
        # Iterate through both halves simultaneously.
        while second_half_head:
            current_twin_sum = first_half_head.val + second_half_head.val
            max_sum = max(max_sum, current_twin_sum)
            
            # Move to the next pair.
            first_half_head = first_half_head.next
            second_half_head = second_half_head.next
            
        return max_sum
```

## Detailed Code Analysis

### Step 1: Find the Middle

```python
slow = head
fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
```

  - This is the classic "Tortoise and Hare" algorithm.
  - The `fast` pointer moves two steps for every one step of the `slow` pointer.
  - When the `fast` pointer reaches the end of the list, the `slow` pointer will be positioned exactly at the start of the second half.

### Step 2: Reverse the Second Half

```python
prev = None
current = slow
while current:
    next_temp = current.next
    current.next = prev
    prev = current
    current = next_temp
```

  - This is the standard iterative algorithm for reversing a linked list in-place.
  - We start the reversal at the `slow` pointer (the middle).
  - After the loop, the variable `prev` will be the new head of this now-reversed second half.

### Step 3: Sum the Pairs

```python
max_sum = 0
first_half_head = head
second_half_head = prev
while second_half_head:
    current_twin_sum = first_half_head.val + second_half_head.val
    max_sum = max(max_sum, current_twin_sum)
    first_half_head = first_half_head.next
    second_half_head = second_half_head.next
```

  - We set up two pointers, `first_half_head` starting at the original `head`, and `second_half_head` starting at `prev` (the head of our reversed section).
  - The `while` loop iterates through both halves in parallel. Since the list has an even length, both halves are the same size, so we can just loop until one of them ends.
  - In each step, we calculate the `current_twin_sum` and update our overall `max_sum`.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `head = [5, 4, 2, 1]` with extreme detail.

### **Phase 1: Finding the Middle**

| Iteration | `slow` Position (Value) | `fast` Position (Value) |
| :--- | :--- | :--- |
| **Start** | `Node(5)` | `Node(5)` |
| **1** | `slow` moves to `Node(4)` | `fast` moves to `Node(2)` |
| **2** | `slow` moves to `Node(2)` | `fast` moves to `None` |

  - The loop terminates. The head of the second half is `slow`, which is `Node(2)`.

### **Phase 2: Reversing the Second Half**

The sub-list to reverse is `2 -> 1 -> None`.

| Action | `prev` | `current` | `next_temp` | List State |
| :--- | :--- | :--- | :--- | :--- |
| **Start** | `None` | `Node(2)` | - | `2 -> 1 -> None` |
| **Loop 1** | | | | |
| `next_temp = current.next` | `None` | `Node(2)` | `Node(1)` | |
| `current.next = prev` | `None` | `Node(2)` | `Node(1)` | `2 -> None` (link to 1 is broken) |
| `prev = current` | `Node(2)`| `Node(2)` | `Node(1)` | |
| `current = next_temp` | `Node(2)`| `Node(1)` | `Node(1)` | |
| **Loop 2** | | | | |
| `next_temp = current.next` | `Node(2)`| `Node(1)` | `None` | |
| `current.next = prev` | `Node(2)`| `Node(1)` | `None` | `1 -> 2 -> None` (new link) |
| `prev = current` | `Node(1)`| `Node(1)` | `None` | |
| `current = next_temp` | `Node(1)`| `None` | `None` | |

  - The loop terminates. The head of the reversed second half is `prev`, which is `Node(1)`.

### **Phase 3: Summing the Pairs**

  - **Initial State**:
      - `first_half_head` points to `Node(5)` (the original head).
      - `second_half_head` points to `Node(1)` (the new head of the reversed half).
      - `max_sum = 0`.
  - **Loop 1**:
      - `current_twin_sum = first_half_head.val + second_half_head.val` -\> `5 + 1 = 6`.
      - `max_sum = max(0, 6) = 6`.
      - Advance pointers: `first_half_head` -\> `Node(4)`, `second_half_head` -\> `Node(2)`.
  - **Loop 2**:
      - `current_twin_sum = first_half_head.val + second_half_head.val` -\> `4 + 2 = 6`.
      - `max_sum = max(6, 6) = 6`.
      - Advance pointers: `first_half_head` -\> `Node(2)` (which is where the list was split), `second_half_head` -\> `None`.
  - The `while` loop terminates because `second_half_head` is now `None`.

### **Final Result**

  - The function returns `max_sum`, which is **6**.

## Performance Analysis

### Time Complexity: O(n)

  - The algorithm makes three passes over roughly half the list each time (`n/2` to find the middle, `n/2` to reverse, `n/2` to sum). The total time is `O(n/2 + n/2 + n/2)`, which simplifies to `O(n)`.

### Space Complexity: O(1)

  - All operations are done in-place by manipulating pointers. We only use a few extra variables, so the space required is constant.

## Key Learning Points

  - **Combining Algorithms**: This problem is a masterful example of how to solve a complex task by combining several fundamental linked list algorithms (finding the middle, reversing a list).
  - **The Versatility of the Tortoise and Hare Algorithm**: It's not just for cycle detection; it's the primary method for finding the midpoint of a linked list efficiently.
  - **In-Place Manipulation**: It reinforces the importance of careful pointer management to modify a linked list without using extra memory.