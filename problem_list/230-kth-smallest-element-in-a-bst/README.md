# 230\. Kth Smallest Element in a BST - Solution Explanation

## Problem Overview

You are given the `root` of a **Binary Search Tree (BST)** and an integer `k`. The task is to find the **k-th smallest value** (1-indexed) among all the node values in the tree.

**Key Definitions:**

  - **Binary Search Tree (BST)**: A tree where for any node, all values in its left subtree are smaller, and all values in its right subtree are larger.
  - **k-th Smallest**: The element that would be at index `k-1` if all the node values were sorted in ascending order.

**Example:**

```python
Input: root = [5,3,6,2,4,null,null,1], k = 3
Output: 3
Explanation:
The sorted values in the tree are [1, 2, 3, 4, 5, 6].
The 3rd smallest value is 3.
```

## Key Insights

### 1\. The Power of In-Order Traversal

The single most important property of a BST is that an **in-order traversal** (`Left -> Root -> Right`) visits the nodes in **ascending sorted order**. This is the key that unlocks the problem. The "k-th smallest element" is simply the k-th element you would encounter during an in-order traversal.

### 2\. The Inefficiency of a Full Traversal

A simple solution would be to perform a full in-order traversal (e.g., recursively), store all the node values in a list, and then return the element at index `k-1`.

  - **The Problem**: This is inefficient. It requires `O(n)` time and `O(n)` space to build the list, even if `k=1`. We are doing more work than necessary.

### 3\. The Optimal Insight: Controlled Iterative Traversal

The best solution is to perform the in-order traversal step-by-step and **stop as soon as we find our target**. An iterative approach using a **stack** is perfect for this. The stack allows us to "pause" our traversal down one path, process a node, and then "resume" the traversal in its right subtree.

## Solution Approach

This solution implements a classic iterative in-order traversal using a stack. It maintains a counter (`k`) and stops the traversal immediately after the k-th node is "visited."

```python
class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        current = root

        while current or stack:
            # Phase 1: Go all the way left.
            # This finds the path to the next smallest node.
            while current:
                stack.append(current)
                current = current.left
            
            # Phase 2: Visit the node.
            # 'current' is None here, so we pop from the stack. The popped
            # node is the next in the in-order sequence.
            current = stack.pop()
            
            k -= 1
            if k == 0:
                return current.val
            
            # Phase 3: Move to the right subtree.
            # The loop will then find the smallest element in this new subtree.
            current = current.right
```

## Detailed Code Analysis

### Step 1: Initialization

```python
stack = []
current = root
```

  - `stack`: An empty list that will function as our stack. It will store the "parent" nodes we need to return to after exploring a left branch.
  - `current`: A pointer that tracks the current node we are exploring. It starts at the `root`.

### Step 2: The Main Loop

```python
while current or stack:
```

  - This loop continues as long as there's a node to process (`current` is not `None`) OR there are nodes on our stack waiting to be processed. This condition correctly handles the entire traversal.

### Step 3: Phase 1 - Go Left

```python
while current:
    stack.append(current)
    current = current.left
```

  - This is the "dive down" part of the algorithm. As long as the `current` node is valid, we push it onto the stack (to save it for later) and then move to its left child. This loop repeats until we hit a `None` node, meaning we have found the leftmost (and thus smallest) unvisited node in the current subtree.

### Step 4: Phase 2 - Pop and Visit

```python
current = stack.pop()
k -= 1
if k == 0:
    return current.val
```

  - This code executes only after the "Go Left" loop has finished (i.e., `current` is `None`).
  - `current = stack.pop()`: We pop the most recently added node from the stack. This is the next node in our sorted, in-order sequence.
  - `k -= 1`: We "visit" this node by decrementing our counter `k`.
  - `if k == 0`: If our counter reaches zero, it means we have just visited the k-th smallest element. We have found our answer and can return its value immediately.

### Step 5: Phase 3 - Go Right

```python
current = current.right
```

  - After visiting a node, the in-order traversal rule says we must now process its right subtree. We update our `current` pointer to the popped node's right child.
  - The main `while` loop will then repeat. The first thing it will do is take this new `current` node and run the "Go Left" phase on it, correctly finding the smallest element in that right subtree.

## Step-by-Step Execution Trace

Let's trace the algorithm with `root = [3,1,4,null,2]` and `k = 1` with extreme detail.

**Tree Structure:**

```
      3
     / \
    1   4
     \
      2
```

### **Initial State:**

  - `stack = []`
  - `current = Node(3)`
  - `k = 1`

-----

### **Main Loop - Iteration 1**

1.  **Go Left**:
      - `current` is `Node(3)`. Push `Node(3)`. `current` becomes `Node(1)`. `stack` is `[Node(3)]`.
      - `current` is `Node(1)`. Push `Node(1)`. `current` becomes `None`. `stack` is `[Node(3), Node(1)]`.
      - `current` is `None`. The inner "Go Left" loop ends.
2.  **Pop and Visit**:
      - `current = stack.pop()` -\> `Node(1)`. `stack` is now `[Node(3)]`.
      - `k -= 1` -\> `k` becomes `0`.
      - `if k == 0:` is **True**.
3.  **Return**: The function returns `current.val`, which is **1**.

The algorithm correctly finds the 1st smallest element and stops without visiting the rest of the tree.

## Performance Analysis

### Time Complexity: O(H + k)

  - Where `H` is the height of the tree and `k` is the input parameter.
  - In the worst case, the algorithm traverses down to the deepest left leaf (`O(H)`) and then performs `k` pop operations. This is significantly better than the `O(n)` of a full traversal, especially when `k` is small.

### Space Complexity: O(H)

  - The space is determined by the maximum size of the `stack`. In the worst case (a skewed tree), the stack can hold up to `n` nodes, making it `O(n)`. In a balanced tree, the height `H` is `log n`, so the space is `O(log n)`.