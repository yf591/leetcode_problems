# 141\. Linked List Cycle - Solution Explanation

## Problem Overview

Determine if a singly linked list contains a **cycle**.

**Cycle Definition:**
A cycle exists if, by following the `next` pointers, you can revisit a node you have already seen.
In other words, the list "loops" back to an earlier node instead of ending at `None`.

**Examples:**

```python
Input: head = [3,2,0,-4], pos = 1
Output: True
Explanation: The last node (-4) points back to the node at index 1 (value 2), forming a cycle.

Input: head = [1,2], pos = 0
Output: True
Explanation: The last node (2) points back to the first node (1), forming a cycle.

Input: head = [1], pos = -1
Output: False
Explanation: The list ends at None, so there is no cycle.
```

## Key Insights

### Floyd's Tortoise and Hare Algorithm (Two-Pointer Technique)

```python
# Use two pointers:
# - slow: moves one step at a time
# - fast: moves two steps at a time

# If there is a cycle, fast will eventually "lap" slow and they will meet.
# If there is no cycle, fast will reach the end of the list (None).
```

### Why the Loop Condition is Crucial

```python
# The loop condition:
while fast and fast.next:
    # ensures that fast and fast.next are valid nodes
    # prevents errors when accessing fast.next.next

# If you use 'while slow and fast.next:', you risk accessing fast.next when fast is None,
# which would cause a runtime error.
```

## Solution Approach

Our solution uses **Floyd's Cycle Detection Algorithm** for optimal time and space efficiency:

```python
def hasCycle(self, head: Optional[ListNode]) -> bool:
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False
```

**Strategy:**

1.  **Pointer Initialization**: Both pointers start at the head.
2.  **Traversal**: Slow moves one step, fast moves two steps.
3.  **Cycle Detection**: If slow and fast meet, a cycle exists.
4.  **Termination**: If fast reaches the end (`None`), no cycle exists.

## Detailed Code Analysis

### Step 1: Pointer Initialization

```python
slow = head
fast = head
```

  - Both pointers start at the beginning of the list.

### Step 2: Safe Traversal with Loop Condition

```python
while fast and fast.next:
```

  - Ensures both `fast` and `fast.next` are not `None`.
  - Prevents errors when moving `fast` two steps ahead.

### Step 3: Pointer Movement

```python
slow = slow.next
fast = fast.next.next
```

  - `slow` advances by one node.
  - `fast` advances by two nodes.

### Step 4: Cycle Detection

```python
if slow == fast:
    return True
```

  - If the pointers meet, a cycle is present.

### Step 5: End of List Check

```python
return False
```

  - If the loop exits, `fast` reached the end, so no cycle exists.

## Step-by-Step Execution Trace

### Example: head = [3,2,0,-4], pos = 1

#### List Structure

```
3 -> 2 -> 0 -> -4
     ^         |
     |_________|
```

  - `-4` points back to `2`, forming a cycle.

#### Execution Steps

| Iteration | `slow` Position (Value) | `fast` Position (Value) | `slow == fast`? |
| :--- | :--- | :--- | :--- |
| **Start** | `head` (3) | `head` (3) | No |
| **1** | `slow.next` (2) | `fast.next.next` (0) | No |
| **2** | `slow.next` (0) | `fast.next.next` (-4 -\> 2) | No |
| **3** | `slow.next` (-4) | `fast.next.next` (0 -\> -4) | **Yes** |

  - In the 3rd iteration, `slow` and `fast` meet at the node with value `-4`, confirming a cycle. The function returns `True`.

### Example: head = [1], pos = -1

  - **Start**: `slow` is at node 1, `fast` is at node 1.
  - **Loop Check**: The condition `while fast and fast.next` is checked. `fast` is valid, but `fast.next` is `None`. The condition is **false**.
  - The loop never runs. The function proceeds to the end and returns `False`.

## Edge Cases Analysis

### Case 1: Empty List

```python
head = None
# Both slow and fast are None; loop never runs.
# Output: False
```

### Case 2: Single Node, No Cycle

```python
head = [1], pos = -1
# slow = fast = head
# fast.next is None; loop never runs.
# Output: False
```

### Case 3: Single Node, Cycle to Itself

```python
head = [1], pos = 0
# slow = fast = head
# fast.next = head (cycle)
# In the first iteration, slow moves to head.next (itself) and fast moves to head.next.next (itself).
# They meet after one loop, and the function returns True.
# Output: True
```

### Case 4: Multiple Nodes, No Cycle

```python
head = [1,2,3,4], pos = -1
# fast will eventually become None or fast.next will become None. The loop will terminate.
# Output: False
```

## Performance Analysis

### Time Complexity: O(n)

  - Each pointer traverses at most the length of the list.

### Space Complexity: O(1)

  - Only two pointers are used; no extra space required.

## Alternative Approaches Comparison

### Approach 1: Hash Set

```python
def hasCycle(self, head: Optional[ListNode]) -> bool:
    visited = set()
    node = head
    while node:
        if node in visited:
            return True
        visited.add(node)
        node = node.next
    return False
```

  - ✅ Simple to understand
  - ❌ Uses O(n) extra space

### Approach 2: Floyd's Algorithm (Our Solution)

  - ✅ O(1) space
  - ✅ O(n) time
  - ✅ Efficient and elegant

## Why the Loop Condition Matters

  - `while fast and fast.next:` ensures you never access `fast.next` when `fast` is `None`.
  - `while slow and fast.next:` is incorrect because if `fast` is `None`, `fast.next` will cause an error.

## Key Learning Points

  - **Two-pointer technique** is powerful for cycle detection.
  - **Loop condition safety** is crucial to avoid runtime errors.
  - **Space-efficient algorithms** are preferred for linked list problems.

## Common Pitfalls Avoided

  - Accessing `fast.next` when `fast` is `None` (runtime error).
  - Forgetting to check both `fast` and `fast.next` in the loop condition.
  - Using extra space unnecessarily.

## Real-World Applications

  - Detecting infinite loops in data structures.
  - Validating linked list integrity in memory management.
  - Cycle detection in graphs and network routing.

-----

This solution demonstrates the elegance and efficiency of Floyd's Cycle Detection algorithm, with careful attention to pointer safety.