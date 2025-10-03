# 138\. Copy List with Random Pointer - Solution Explanation

## Problem Overview

You are given a special kind of linked list where each node has two pointers:

1.  A standard `next` pointer, which points to the next node in the sequence.
2.  A `random` pointer, which can point to **any** node in the list (or to `null`).

The task is to create a **deep copy** of this entire list. A deep copy means creating a completely new set of nodes that are separate from the original, but which perfectly replicate the structure and values of the original list, including both the `next` and `random` pointers.

**Example:**
If `Node X` points to `Node Y` with its `random` pointer in the original list, then the new copy of `X` must point to the new copy of `Y` with its `random` pointer.

## Key Insights

### The "Chicken and Egg" Dilemma

Copying a simple linked list (with only `next` pointers) is easy. You traverse the original list and create a new node for each one you see.

The challenge here is the `random` pointer. Imagine you are copying the list node by node. You're at an original `Node A` and create its copy, `Node A'`. `Node A`'s `random` pointer points to some `Node Z` later in the list. To set `Node A'.random`, you need to point it to `Node Z'`, but `Node Z'` **hasn't been created yet\!** How can you get a reference to a node that doesn't exist?

### Solution 1: The Hash Map (O(n) Space)

A straightforward way to solve this is with a hash map and two passes.

1.  **First Pass (Create Nodes)**: Go through the original list. For each `original_node`, create its `new_node` copy and store the mapping in a hash map: `map[original_node] = new_node`.
2.  **Second Pass (Assign Pointers)**: Go through the list again. For each `original_node`, you can now set the pointers for its `new_node`:
      - `new_node.next = map[original_node.next]`
      - `new_node.random = map[original_node.random]`
        This works perfectly, but it requires `O(n)` extra space for the hash map.

### Solution 2: The Interweaving Trick (O(1) Space)

The most clever and space-efficient solution avoids a hash map by modifying the list structure itself to store the mapping. This is the **interweaving** method you described.

1.  **Pass 1: Interweave**: Weave the copied nodes into the original list. For every original node, create its copy and place it immediately after the original. The list `A -> B` becomes `A -> A' -> B -> B'`.
2.  **Pass 2: Assign Random Pointers**: Now, for any `original_node`, its copy is always `original_node.next`. This gives us a way to find copies. For an original node `A`, we can set its copy's random pointer (`A'.random`) by looking at the original's random target (`A.random`) and finding *its* copy, which is simply `A.random.next`.
3.  **Pass 3: Separate the Lists**: "Unzip" the interwoven list to restore the original list and extract the new, fully-formed copied list.

## Solution Approach (The O(1) Space Interweaving Method)

This solution implements the elegant three-pass strategy.

```python
class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return None

        # --- Pass 1: Create a copy of each node and interweave them ---
        current = head
        while current:
            new_node = Node(current.val)
            new_node.next = current.next
            current.next = new_node
            current = new_node.next

        # --- Pass 2: Set the random pointers for the copied nodes ---
        current = head
        while current:
            if current.random:
                current.next.random = current.random.next
            current = current.next.next

        # --- Pass 3: Separate the original and copied lists ---
        dummy_head = Node(0)
        new_list_tail = dummy_head
        current = head
        
        while current:
            # Save the pointer to the next original node
            next_original = current.next.next
            
            # Extract the copied node
            copied_node = current.next
            new_list_tail.next = copied_node
            new_list_tail = new_list_tail.next
            
            # Restore the original list's next pointer
            current.next = next_original
            
            # Move to the next original node
            current = next_original
            
        return dummy_head.next
```

## Detailed Code Analysis

### Pass 1: Interweaving the Nodes

```python
current = head
while current:
    new_node = Node(current.val)
    new_node.next = current.next
    current.next = new_node
    current = new_node.next
```

  - This loop iterates through the original nodes. For each `current` node:
    1.  A `new_node` is created with the same value.
    2.  `new_node.next = current.next`: The new node is linked to the rest of the original list.
    3.  `current.next = new_node`: The original node is linked to its new copy.
    4.  `current = new_node.next`: `current` is advanced to the *next original* node to continue the process.

### Pass 2: Assigning Random Pointers

```python
current = head
while current:
    if current.random:
        current.next.random = current.random.next
    current = current.next.next
```

  - This loop also iterates through the original nodes, but it jumps two steps at a time (`current.next.next`) to do so.
  - `if current.random:`: We only do something if the original node has a random pointer.
  - **`current.next.random = current.random.next`**: This is the core magic. Let's break it down:
      - `current`: The original node (e.g., `A`).
      - `current.next`: The copy of that node (e.g., `A'`). So we are setting `A'.random`.
      - `current.random`: The original random target (e.g., `Z`).
      - `current.random.next`: The copy of that random target (e.g., `Z'`).
      - The line effectively says: **`A_copy.random = Z_copy`**.

### Pass 3: Separating the Lists

```python
dummy_head = Node(0)
new_list_tail = dummy_head
current = head
while current:
    next_original = current.next.next
    copied_node = current.next
    new_list_tail.next = copied_node
    new_list_tail = new_list_tail.next
    current.next = next_original
    current = next_original
```

  - This is the "unzipping" process. We use a `dummy_head` to make handling the start of the new list easier.
  - For each `current` original node:
    1.  We extract the `copied_node` (`current.next`).
    2.  We restore the `current` node's original `next` pointer.
    3.  We append the `copied_node` to our new list.
    4.  We advance `current` to the next original node.

## Step-by-Step Execution Trace

Let's trace with a simple list `A -> B`, where `A.random -> B` and `B.random -> A`.

### **Initial State:**

```
  A <-----.
  |         \
  '--> B ---'
  ^    |
  '----'
```

### **Pass 1: Interweave**

1.  **At A**: Create `A'`. Link `A -> A'`. Link `A' -> B`. `current` becomes `B`.
2.  **At B**: Create `B'`. Link `B -> B'`. Link `B' -> None`. `current` becomes `None`.
    **State After Pass 1:** The list is now `A -> A' -> B -> B'`.

### **Pass 2: Assign Random Pointers**

1.  **At A**:
      - `A.random` is `B`.
      - Set `A'.random` (`A.next.random`) to `A.random.next` (`B.next`).
      - `A'.random` is now correctly set to `B'`.
2.  **At B**:
      - `B.random` is `A`.
      - Set `B'.random` (`B.next.random`) to `B.random.next` (`A.next`).
      - `B'.random` is now correctly set to `A'`.

**State After Pass 2:** Both `A'.random` and `B'.random` are correctly set. The list is still interwoven.

### **Pass 3: Separate**

1.  **At A**:
      - Extract `A'`. Link `dummy_head -> A'`.
      - Restore `A.next` to point to `B`.
      - Advance `current` to `B`.
2.  **At B**:
      - Extract `B'`. Link `A' -> B'`.
      - Restore `B.next` to point to `None`.
      - Advance `current` to `None`.

**Final State:**

  - **Original List**: `A -> B -> None` (fully restored).
  - **Copied List**: `A' -> B' -> None` (fully extracted and correct).
  - The function returns `dummy_head.next`, which is `A'`.

## Performance Analysis

### Time Complexity: O(n)

  - The algorithm consists of three separate passes over the list. Each pass is `O(n)`. The total time complexity is `O(n) + O(n) + O(n) = O(n)`.

### Space Complexity: O(1)

  - This is the main advantage of this method. The modification is done in-place. We only use a few extra pointers. The space required is constant.