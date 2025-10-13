# 102\. Binary Tree Level Order Traversal - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree. The task is to return a **level order traversal** of its nodes' values.

**Level Order Traversal Definition:**
This means visiting the nodes level by level, from left to right.

  - First, visit the root (Level 0).
  - Then, visit all of the root's children (Level 1) from left to right.
  - Then, visit all of their children (Level 2) from left to right, and so on.
    The final output should be a list of lists, where each inner list contains the node values for one level.

**Example:**

```python
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]
```

## Key Insights

### The Right Algorithm: Breadth-First Search (BFS)

The problem's requirement to process nodes "level by level" is the exact definition of a **Breadth-First Search (BFS)** traversal. Unlike Depth-First Search (DFS), which explores as far down one path as possible, BFS explores the tree in concentric layers.

### The Right Data Structure: A Queue

BFS is implemented using a **queue**, which is a "First-In, First-Out" (FIFO) data structure.

  - We add nodes to the back of the queue (enqueue).
  - We process nodes from the front of the queue (dequeue).
    This ensures that we process all nodes at Level `N` before we start processing their children at Level `N+1`. In Python, the `collections.deque` object is the most efficient and standard way to implement a queue.

### The Level-by-Level Grouping Trick

How do we know when one level ends and the next begins? The key insight is to capture the size of the queue at the *start* of each level's processing. If the queue contains 2 nodes, we know those are the only 2 nodes on the current level. We can then run a loop exactly 2 times to process just those nodes, while their children get added to the queue for the *next* level.

## Solution Approach

This solution implements a classic BFS. It uses a `while` loop to iterate through the levels of the tree and a nested `for` loop to iterate through the nodes within each level.

```python
import collections
from typing import Optional, List

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        queue = collections.deque([root])

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(current_level)
            
        return result
```

## Detailed Code Analysis

### Step 1: Initialization

```python
if not root:
    return []
result = []
queue = collections.deque([root])
```

  - **Edge Case**: First, we handle the case of an empty tree. If the `root` is `None`, we return an empty list as required.
  - **`result = []`**: This is the list that will store our final answer (a list of lists).
  - **`queue = collections.deque([root])`**: We initialize our queue. We start by adding the `root` node, which is the only node on Level 0.

### Step 2: The Main (Level) Loop

```python
while queue:
```

  - This `while` loop is the main engine of the BFS. It continues to run as long as there are nodes in the queue, which means there are still levels to be processed. Each full iteration of this `while` loop processes **one entire level**.

### Step 3: The Level Processing Logic (Inside the `while` loop)

This is the most important part of the algorithm.

**Capturing the Level Size:**

```python
level_size = len(queue)
current_level = []
```

  - `level_size = len(queue)`: Before we start processing, we get the current number of items in the queue. This is the **exact** number of nodes on the current level. This is a critical step.
  - `current_level = []`: We create a temporary list to hold the values for just this level.

**The Inner (Node) Loop:**

```python
for _ in range(level_size):
    node = queue.popleft()
    current_level.append(node.val)
    if node.left:
        queue.append(node.left)
    if node.right:
        queue.append(node.right)
```

  - This `for` loop runs exactly `level_size` times.
  - `node = queue.popleft()`: We remove a node from the **front** of the queue (FIFO).
  - `current_level.append(node.val)`: We add its value to our temporary list for this level.
  - `if node.left: ...`, `if node.right: ...`: We add the node's children (if they exist) to the **back** of the queue. These children will be processed in the *next* iteration of the outer `while` loop.

**Finalizing the Level:**

```python
result.append(current_level)
```

  - After the inner `for` loop has finished, `current_level` contains all the values for that level in the correct left-to-right order. We append this list to our final `result`.

## Step-by-Step Execution Trace

Let's trace `root = [3, 9, 20, null, null, 15, 7]` with extreme detail.

### **Initial State:**

  - `result = []`
  - `queue = deque([Node(3)])`

-----

### **Level 0 (First `while` loop iteration)**

1.  **`while queue:`**: The queue is not empty.
2.  `level_size = len(queue)` is **1**. `current_level = []`.
3.  **Inner `for` loop runs 1 time**:
      - `node = queue.popleft()` -\> `Node(3)`. `queue` is now empty.
      - `current_level.append(3)`. `current_level` is `[3]`.
      - `Node(3).left` (Node 9) is added to the queue.
      - `Node(3).right` (Node 20) is added to the queue.
4.  Inner loop finishes. `queue` is now `deque([Node(9), Node(20)])`.
5.  `result.append(current_level)`.
6.  **`result` state**: `[[3]]`

-----

### **Level 1 (Second `while` loop iteration)**

1.  **`while queue:`**: The queue is not empty.
2.  `level_size = len(queue)` is **2**. `current_level = []`.
3.  **Inner `for` loop runs 2 times**:
      - **Loop 1**: `node = queue.popleft()` -\> `Node(9)`. `queue` is now `deque([Node(20)])`.
          - `current_level.append(9)`. `current_level` is `[9]`.
          - `Node(9)` has no children.
      - **Loop 2**: `node = queue.popleft()` -\> `Node(20)`. `queue` is now empty.
          - `current_level.append(20)`. `current_level` is `[9, 20]`.
          - `Node(20).left` (Node 15) is added to the queue.
          - `Node(20).right` (Node 7) is added to the queue.
4.  Inner loop finishes. `queue` is now `deque([Node(15), Node(7)])`.
5.  `result.append(current_level)`.
6.  **`result` state**: `[[3], [9, 20]]`

-----

### **Level 2 (Third `while` loop iteration)**

1.  **`while queue:`**: The queue is not empty.
2.  `level_size = len(queue)` is **2**. `current_level = []`.
3.  **Inner `for` loop runs 2 times**:
      - **Loop 1**: `node = queue.popleft()` -\> `Node(15)`. `current_level` is `[15]`. No children.
      - **Loop 2**: `node = queue.popleft()` -\> `Node(7)`. `current_level` is `[15, 7]`. No children.
4.  Inner loop finishes. `queue` is now `deque([])`.
5.  `result.append(current_level)`.
6.  **`result` state**: `[[3], [9, 20], [15, 7]]`

-----

### **End of Traversal**

  - The `while queue:` condition is now **False**. The loop terminates.
  - The function returns the final `result`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The algorithm enqueues and dequeues each node exactly once, performing constant-time work for each.

### Space Complexity: O(w)

  - Where `w` is the **maximum width** of the tree. This is the maximum number of nodes that can be in the `queue` at any one time. In the worst case (a full, complete binary tree), the last level can contain up to `(n+1)/2` nodes, making the space complexity `O(n)`.