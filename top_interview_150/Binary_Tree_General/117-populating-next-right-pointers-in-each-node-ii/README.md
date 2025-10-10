# 117\. Populating Next Right Pointers in Each Node II - Solution Explanation

## Problem Overview

You are given a binary tree with a special `next` pointer in each node. Initially, all `next` pointers are `NULL`. The task is to populate each `next` pointer so that it points to the node immediately to its right on the same level. If a node is the rightmost on its level, its `next` pointer should remain `NULL`.

**The Crucial Detail:**

  - Unlike its sibling problem (No. 116), this tree is **not a perfect binary tree**. It can have gaps, making the solution more complex.
  - The "follow-up" asks for a solution using only **constant (`O(1)`) extra space**.

**Example:**

  - **Input Tree:**
    ```
          1
         / \
        2   3
       / \   \
      4   5   7
    ```
  - **Output Tree (after connecting `next` pointers):**
    ```
          1 -> NULL
         / \
        2 -> 3 -> NULL
       / \   \
      4 -> 5 -> 7 -> NULL
    ```

## Key Insights

### 1\. The Obvious (but Space-Inefficient) BFS Approach

The problem requires processing the tree **level by level**. This immediately suggests a **Breadth-First Search (BFS)** using a **queue**.

1.  Put the root in a queue.
2.  In a loop, process all nodes for the current level.
3.  For each node you dequeue, set its `next` pointer to the node that is now at the front of the queue.
4.  Add the children of all nodes from the current level to the queue for the next level.

This works perfectly, but it requires a queue that can grow to the maximum width of the tree. In the worst case, this is `O(n)` space, which violates the constant space constraint.

### 2\. The `O(1)` Space Insight: "The Level Above is a Linked List"

The key to a constant space solution is to realize that once you have successfully populated the `next` pointers for a given level, that entire level becomes a **singly linked list** that you can traverse from left to right.

This means we can use the completed Level `N` as a "track" to move across and build the `next` pointer connections for the level below it, Level `N+1`, without needing a queue.

## Solution Approach

This beautiful solution uses a nested loop structure. The outer loop moves from one level down to the next. The inner loop moves across the current level (using the `next` pointers we've already set) to build the connections for the level below.

We use a `dummy` head and a `tail` pointer to construct the linked list for the child level.

```python
class Solution:
    def connect(self, root: 'Node') -> 'Node':
        if not root:
            return None
        
        # 'level_start' is the first node of the level we are currently traversing.
        level_start = root
        
        # This outer loop moves us from one level down to the next.
        while level_start:
            # 'dummy_head' is a placeholder for the start of the *next* level.
            # 'tail' is our "builder" pointer for the next level's connections.
            dummy_head = Node(0)
            tail = dummy_head
            
            # 'current' traverses the current level using the .next pointers.
            current = level_start
            
            # This inner loop processes all nodes on the current level.
            while current:
                # If the current node has a left child, link it.
                if current.left:
                    tail.next = current.left
                    tail = tail.next
                
                # If the current node has a right child, link it.
                if current.right:
                    tail.next = current.right
                    tail = tail.next
                    
                # Move to the next node on the *same* level using the .next pointer.
                current = current.next
            
            # Move to the start of the next level that we just built.
            level_start = dummy_head.next
            
        return root
```

## Detailed Code Analysis

### Step 1: Initialization

```python
level_start = root
```

  - We initialize a pointer `level_start` to the `root`. This pointer will always mark the beginning (the leftmost node) of the level we are about to process.

### Step 2: The Outer Loop

```python
while level_start:
```

  - This loop continues as long as there are more levels in the tree to process. When `level_start` becomes `None`, it means we have processed the children of the last level of nodes, and our work is done.

### Step 3: Setting Up for the Next Level

```python
dummy_head = Node(0)
tail = dummy_head
current = level_start
```

  - Inside the outer loop, we reset our "builder" tools for the child level.
  - `dummy_head`: This is a temporary placeholder. It's the "scaffolding" we'll attach the first child node to. This avoids messy `if` checks for "is this the first child on this level?".
  - `tail`: This is our "pen." It will always point to the last node in the `next` chain we are currently constructing for the level below. We start it at the `dummy_head`.
  - `current`: This is our "reader." It starts at the beginning of the *current* level and will traverse it from left to right.

### Step 4: The Inner Loop (Building the Child Level)

```python
while current:
    if current.left:
        tail.next = current.left
        tail = tail.next
    if current.right:
        tail.next = current.right
        tail = tail.next
    current = current.next
```

  - This loop iterates across the current level using the `next` pointers we set in the *previous* iteration of the outer loop.
  - **`if current.left:`**: We check if the node we're on has a left child.
      - `tail.next = current.left`: If it does, we link our `tail` to this child. This is the core connection step.
      - `tail = tail.next`: We then advance our `tail` pointer to be this new child, as it's now the end of our growing child-level chain.
  - **`if current.right:`**: We do the exact same thing for the right child.
  - **`current = current.next`**: This moves our "reader" to the next node on the *current* level, allowing us to process its children.

### Step 5: Moving to the Next Level

```python
level_start = dummy_head.next
```

  - After the inner `while` loop has finished, we have visited every node on the current level.
  - The `dummy_head.next` now points to the very first child we linked, which is the start of the next level.
  - We update `level_start` to this new node, preparing for the next iteration of the outer `while` loop.

## Step-by-Step Execution Trace

Let's trace the algorithm with `root = [1,2,3,4,5,null,7]` with extreme detail.

### **Initial State:**

  - `level_start` -\> `Node(1)`

-----

### **Outer Loop - Pass 1 (Processing Level 0, Building Level 1)**

  - **Setup**:
      - `dummy_head` is created. `tail` -\> `dummy_head`.
      - `current` -\> `level_start` -\> `Node(1)`.
  - **Inner Loop (while `current`):**
    1.  **`current` is `Node(1)`**:
          - `current.left` (Node 2) exists. `tail.next = Node(2)`. Now `dummy -> 2`. `tail` moves to `Node(2)`.
          - `current.right` (Node 3) exists. `tail.next = Node(3)`. Now `dummy -> 2 -> 3`. `tail` moves to `Node(3)`.
          - `current = current.next` (which is `None` for Node 1).
    2.  **`current` is `None`**: Inner loop terminates.
  - **Move to Next Level**: `level_start = dummy_head.next` -\> `level_start` is now `Node(2)`.
  - **State after Pass 1**: The `next` pointers for Level 1 are set: `2 -> 3 -> NULL`.

-----

### **Outer Loop - Pass 2 (Processing Level 1, Building Level 2)**

  - **Setup**:
      - A new `dummy_head` is created. `tail` -\> `dummy_head`.
      - `current` -\> `level_start` -\> `Node(2)`.
  - **Inner Loop (while `current`):**
    1.  **`current` is `Node(2)`**:
          - `current.left` (Node 4) exists. `tail.next = Node(4)`. Now `dummy -> 4`. `tail` moves to `Node(4)`.
          - `current.right` (Node 5) exists. `tail.next = Node(5)`. Now `dummy -> 4 -> 5`. `tail` moves to `Node(5)`.
          - `current = current.next` -\> `current` is now `Node(3)`.
    2.  **`current` is `Node(3)`**:
          - `current.left` is `None`.
          - `current.right` (Node 7) exists. `tail.next = Node(7)`. Now `dummy -> 4 -> 5 -> 7`. `tail` moves to `Node(7)`.
          - `current = current.next` -\> `current` is now `None`.
    3.  **`current` is `None`**: Inner loop terminates.
  - **Move to Next Level**: `level_start = dummy_head.next` -\> `level_start` is now `Node(4)`.
  - **State after Pass 2**: The `next` pointers for Level 2 are set: `4 -> 5 -> 7 -> NULL`.

-----

### **Outer Loop - Pass 3 (Processing Level 2, Building Level 3)**

  - **Setup**:
      - New `dummy_head` and `tail`.
      - `current` -\> `level_start` -\> `Node(4)`.
  - **Inner Loop (while `current`):**
      - The loop runs for `Node(4)`, `Node(5)`, and `Node(7)`. None of them have children. The `if` conditions are never met. The `tail` pointer never moves from `dummy_head`.
  - **Move to Next Level**: `level_start = dummy_head.next`. Since `tail` never moved, `dummy_head.next` is still `None`. `level_start` becomes `None`.

-----

### **End of Algorithm**

  - The outer `while level_start:` condition is now **False**. The entire process terminates.
  - The function returns the original `root`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. Each node is visited exactly once by the `current` pointer in the inner loop.

### Space Complexity: O(1)

  - This is the main advantage of this approach. We only use a few pointers (`level_start`, `current`, `dummy_head`, `tail`). The space required is constant and does not depend on the size of the tree. This is a huge improvement over the `O(n)` space required by a queue-based BFS.