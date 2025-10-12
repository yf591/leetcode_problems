# 173\. Binary Search Tree Iterator - Solution Explanation

## Problem Overview

The task is to implement a `BSTIterator` class that acts as an iterator over a **Binary Search Tree (BST)**. The iterator must return the nodes' values in **in-order** sequence.

**Class Methods:**

  - `__init__(self, root)`: Initializes the iterator with the root of the BST.
  - `next(self) -> int`: Moves to the next smallest number in the sequence and returns it.
  - `hasNext(self) -> bool`: Returns `True` if there is a next number in the sequence, and `False` otherwise.

**Key Constraints & Properties:**

  - **In-order Traversal**: For a BST, an in-order traversal (`Left -> Root -> Right`) visits the nodes in **ascending sorted order**.
  - **Iterator Behavior**: The `next()` and `hasNext()` calls must be efficient. We shouldn't do all the work at once. This implies a "lazy" or "controlled" traversal.
  - **Follow-up (The Real Goal)**: The optimal solution should have `O(1)` average time complexity for `next()` and `hasNext()`, and `O(h)` space complexity, where `h` is the height of the tree.

**Example:** For a tree `[7, 3, 15, null, null, 9, 20]`, the in-order sequence is `3, 7, 9, 15, 20`. The iterator should return these numbers in this order.

## Key Insights

### 1\. The Naive (but `O(n)` space) Approach

The simplest way to think about this is to perform a full in-order traversal during initialization, store all the node values in a list, and then use a pointer to iterate through that list.

  - `__init__`: Create a list `[3, 7, 9, 15, 20]`.
  - `next()`: Return the next item from the list.
  - `hasNext()`: Check if the pointer is past the end of the list.
    This works, but it's not optimal. It uses `O(n)` space for the list and does all the work upfront, which isn't the spirit of a true iterator.

### 2\. The Optimal Insight: Controlled Traversal with a Stack

The key to an efficient solution is to simulate the in-order traversal step-by-step, pausing after each `next()` call.

How is an in-order traversal typically implemented *iteratively*? With a **stack**. The stack keeps track of the path we've taken, allowing us to backtrack correctly. We can leverage this. The stack will hold the "state" of our paused traversal.

The standard iterative in-order algorithm is:

1.  Go as far left as you can from the current node, pushing every node you visit onto the stack.
2.  Once you can't go left anymore, **pop** a node from the stack. This is your next smallest element.
3.  After processing this node, move to its **right child** and repeat step 1 from there.

Our iterator can use this exact logic. The stack will hold the path to the next smallest node.

## Solution Approach

This solution uses a stack to simulate the in-order traversal in a controlled manner.

  - The `__init__` method will "prime" the stack by finding the path to the very first (smallest) element.
  - The `next()` method will pop an element, process its right subtree to set up the *next* call, and then return the value.
  - The `hasNext()` method simply checks if there's anything left on the stack to process.

<!-- end list -->

```python
from typing import Optional

class BSTIterator:
    def __init__(self, root: Optional[TreeNode]):
        # The stack will store the path to the next smallest node.
        self.stack = []
        # A helper function to push all left children of a node onto the stack.
        self._go_left(root)

    def _go_left(self, node: Optional[TreeNode]):
        """
        Traverses as far left as possible from the given node,
        pushing each node onto the stack along the way.
        """
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        """
        Returns the next smallest number in the BST.
        """
        # The node at the top of the stack is the next smallest element.
        node_to_return = self.stack.pop()
        
        # Before returning, we must prepare for the *next* call to next().
        # The next element in an in-order traversal is the smallest element
        # in the right subtree of the node we just popped.
        if node_to_return.right:
            self._go_left(node_to_return.right)
            
        return node_to_return.val

    def hasNext(self) -> bool:
        """
        Returns true if there is a next smallest number.
        """
        # If the stack is not empty, it means there are still nodes
        # to be processed in the in-order sequence.
        return len(self.stack) > 0
```

## Detailed Code Analysis

### `__init__(self, root)`

```python
self.stack = []
self._go_left(root)
```

  - We initialize an empty list to act as our `stack`.
  - We immediately call our helper `_go_left(root)`. This is the "priming" step. It finds the path to the smallest element in the entire tree by starting at the root and repeatedly moving left, pushing each node onto the stack. After this, the top of the stack holds the smallest node.

### `_go_left(self, node)`

```python
while node:
    self.stack.append(node)
    node = node.left
```

  - This helper is the core of finding the "next" part of a sequence. Given any starting `node`, it follows the `left` pointers down to the bottom, adding each node to the stack. This simulates the "Go Left" part of the `Left -> Root -> Right` in-order rule.

### `hasNext(self)`

```python
return len(self.stack) > 0
```

  - This is very simple. The in-order traversal is finished only when there are no more nodes to process. In our simulation, this means the stack is empty. So, if the stack has any elements, there is a `next` element.

### `next(self)`

This is the most important method.

```python
node_to_return = self.stack.pop()
```

  - This corresponds to the "Visit Root" part of the `Left -> Root -> Right` rule. The `_go_left` helper already took care of the `Left` part. The node at the top of the stack is the next node we need to process in our sorted sequence.

<!-- end list -->

```python
if node_to_return.right:
    self._go_left(node_to_return.right)
```

  - This corresponds to the "Go Right" part of the rule. After we've processed a node, the next smallest element must be the smallest node in its right subtree.
  - We take the `right` child of the node we just popped and call our `_go_left` helper on it. This sets up the stack perfectly for the *next* time `next()` is called.

<!-- end list -->

```python
return node_to_return.val
```

  - Finally, we return the value of the node we popped.

## Step-by-Step Execution Trace

Let's trace the algorithm with `root = [7, 3, 15, null, null, 9, 20]` with extreme detail.

### **1. `__init__(root)`**

  - `stack` is `[]`.
  - Call `_go_left(Node(7))`.
      - `stack.append(Node(7))`. Stack is `[Node(7)]`.
      - Move to `Node(7).left`, which is `Node(3)`.
      - `stack.append(Node(3))`. Stack is `[Node(7), Node(3)]`.
      - Move to `Node(3).left`, which is `None`. Loop ends.
  - **Initial State**: `stack` is `[Node(7), Node(3)]`.

-----

### **2. `next()` - First Call**

  - `hasNext()` would return `True` because the stack is not empty.
  - `node_to_return = stack.pop()` -\> `Node(3)`. Stack is now `[Node(7)]`.
  - Check `node_to_return.right` (`Node(3).right`). It is `None`. The `if` block is skipped.
  - **Returns `3`**.

-----

### **3. `next()` - Second Call**

  - `hasNext()` would return `True`.
  - `node_to_return = stack.pop()` -\> `Node(7)`. Stack is now `[]`.
  - Check `node_to_return.right` (`Node(7).right`). It is `Node(15)`. The `if` block runs.
  - Call `_go_left(Node(15))`.
      - `stack.append(Node(15))`. Stack is `[Node(15)]`.
      - Move to `Node(15).left`, which is `Node(9)`.
      - `stack.append(Node(9))`. Stack is `[Node(15), Node(9)]`.
      - Move to `Node(9).left`, which is `None`. Loop ends.
  - **Returns `7`**.
  - **State after call**: `stack` is `[Node(15), Node(9)]`.

-----

### **4. `hasNext()`**

  - Checks `len(stack) > 0`. `2 > 0` is true.
  - **Returns `True`**.

-----

### **5. `next()` - Third Call**

  - `hasNext()` would return `True`.
  - `node_to_return = stack.pop()` -\> `Node(9)`. Stack is now `[Node(15)]`.
  - Check `node_to_return.right` (`Node(9).right`). It is `None`. The `if` block is skipped.
  - **Returns `9`**.

... and so on. The process continues until the stack is empty.

## Performance Analysis

### Time Complexity: O(1) on average for `next()` and `hasNext()`

  - `hasNext()` is always a simple `O(1)` check on the stack's size.
  - `next()` is more complex. While the `_go_left` call can take `O(h)` time in the worst case (where `h` is the height of the tree), this work is not done on every call. Each node of the tree is pushed onto the stack exactly once and popped exactly once over the entire course of iterating through all `n` nodes.
  - Therefore, the total time spent over `n` calls to `next()` is `O(n)`. The **amortized** (or average) time complexity for each call is `O(n) / n = O(1)`.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. The maximum size of the stack at any given time is the length of the longest path of left children, which is the height of the tree. This is a significant improvement over the `O(n)` space of the naive "flattening" approach.