# 199\. Binary Tree Right Side View - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree. The task is to imagine you are standing on the **right side** of the tree and list the values of the nodes you can see, from top to bottom.

**The Goal in Simple Terms:**
For each "level" or "row" of the tree, find the value of the **rightmost node**.

**Examples:**

```python
Input: root = [1,2,3,null,5,null,4]
Output: [1,3,4]

# Tree Structure:
#      1   <-- Level 0, rightmost is 1
#     / \
#    2   3 <-- Level 1, rightmost is 3
#     \   \
#      5   4 <-- Level 2, rightmost is 4
```

## Key Insights

### Level-Order Traversal -\> Breadth-First Search (BFS)

The problem requires us to think about the tree in terms of its **levels**. This is a massive clue that the best algorithm to use is **Breadth-First Search (BFS)**. BFS is a traversal algorithm that explores a tree "layer by layer," visiting all nodes at the current depth before moving on to the next. This is exactly what we need.

### The "Peek at the End" Trick

When we use BFS with a queue, at the beginning of each step of our main loop, the queue will contain *all* the nodes for the current level and nothing else. Since we process the nodes on a level from left to right, the rightmost node is simply the **last element** in the queue at that moment.

This gives us a very simple strategy: for each level, we can just "peek" at the last node in the queue, record its value, and then process the entire level to set up the queue for the next level.

## Solution Approach

This solution implements the BFS algorithm using a queue (`collections.deque`). It processes the tree level by level. At the start of each level's processing, it records the value of the last node in the queue.

```python
import collections
from typing import Optional, List

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        # Handle the edge case of an empty tree.
        if not root:
            return []
            
        result = []
        # A deque (double-ended queue) is an efficient queue implementation in Python.
        queue = collections.deque([root])
        
        # Loop as long as there are levels to process.
        while queue:
            # The rightmost node is the last one in the queue at the start of a level.
            rightmost_node = queue[-1]
            result.append(rightmost_node.val)
            
            # Now, process all nodes on the current level to add their
            # children to the queue for the next level.
            level_size = len(queue)
            for _ in range(level_size):
                # Remove a node from the front of the queue.
                node = queue.popleft()
                
                # Add its children (if they exist) to the back of the queue.
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                    
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

  - **Edge Case**: We first handle the case of an empty tree.
  - **`result = []`**: This list will store our final answer.
  - **`queue = collections.deque([root])`**: We initialize our queue. `collections.deque` is used because adding to the right (`append`) and removing from the left (`popleft`) are both very fast `O(1)` operations. We start the queue with the `root` node, which represents Level 0.

### Step 2: The Main (Level-by-Level) Loop

```python
while queue:
```

  - This `while` loop continues as long as there are nodes in the queue, which means there are still levels to process. Each full iteration of this loop processes one entire level of the tree.

### Step 3: Finding the Rightmost Node

```python
rightmost_node = queue[-1]
result.append(rightmost_node.val)
```

  - This is the core insight. At the beginning of the `while` loop's iteration for a new level, the queue contains all nodes for that level.
  - `queue[-1]` is a convenient way to "peek" at the last element of a `deque` without removing it. This last element is guaranteed to be the rightmost node of the current level.
  - We append its value to our `result` list.

### Step 4: Processing the Current Level

```python
level_size = len(queue)
for _ in range(level_size):
    node = queue.popleft()
    if node.left:
        queue.append(node.left)
    if node.right:
        queue.append(node.right)
```

  - This is a standard pattern for level-order traversal.
  - `level_size = len(queue)`: We **must** store the size of the current level *before* the loop starts. If we used `len(queue)` directly in the loop, it would change as we add new children, leading to an incorrect traversal.
  - `for _ in range(level_size)`: This loop runs exactly enough times to process all nodes on the current level.
  - `node = queue.popleft()`: We remove nodes from the front of the queue (First-In, First-Out).
  - `queue.append(...)`: We add any existing children to the back of the queue. These will be processed in the next iteration of the outer `while` loop.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `root = [1, 2, 3, null, 5, null, 4]` with extreme detail.

### **Initial State:**

  - `result = []`
  - `queue = deque([Node(1)])`

-----

### **Level 0 (First `while` loop iteration)**

1.  **`queue` is not empty.**
2.  **Find Rightmost**: `queue[-1]` is `Node(1)`. `result.append(1)`.
      - `result` is now `[1]`.
3.  **Process Level**: `level_size = len(queue)` is `1`. The inner `for` loop will run once.
      - `node = queue.popleft()` -\> `Node(1)`.
      - `node.left` (Node 2) exists. `queue.append(Node(2))`.
      - `node.right` (Node 3) exists. `queue.append(Node(3))`.
4.  **End of Level**: `queue` is now `deque([Node(2), Node(3)])`.

-----

### **Level 1 (Second `while` loop iteration)**

1.  **`queue` is not empty.**
2.  **Find Rightmost**: `queue[-1]` is `Node(3)`. `result.append(3)`.
      - `result` is now `[1, 3]`.
3.  **Process Level**: `level_size = len(queue)` is `2`. The inner `for` loop will run twice.
      - **Loop 1**: `node = queue.popleft()` -\> `Node(2)`.
          - `node.left` is `None`.
          - `node.right` (Node 5) exists. `queue.append(Node(5))`.
      - **Loop 2**: `node = queue.popleft()` -\> `Node(3)`.
          - `node.left` is `None`.
          - `node.right` (Node 4) exists. `queue.append(Node(4))`.
4.  **End of Level**: `queue` is now `deque([Node(5), Node(4)])`.

-----

### **Level 2 (Third `while` loop iteration)**

1.  **`queue` is not empty.**
2.  **Find Rightmost**: `queue[-1]` is `Node(4)`. `result.append(4)`.
      - `result` is now `[1, 3, 4]`.
3.  **Process Level**: `level_size = len(queue)` is `2`. The inner `for` loop will run twice.
      - **Loop 1**: `node = queue.popleft()` -\> `Node(5)`. It has no children.
      - **Loop 2**: `node = queue.popleft()` -\> `Node(4)`. It has no children.
4.  **End of Level**: `queue` is now `deque([])`.

-----

### **End of Traversal**

  - The `while queue` condition is now **False**. The loop terminates.
  - The function returns the final `result`: **`[1, 3, 4]`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The algorithm enqueues and dequeues each node exactly once.

### Space Complexity: O(w)

  - Where `w` is the **maximum width** of the tree. This is the maximum number of nodes that can be in the `queue` at any one time. In the worst case (a full, complete binary tree), the last level can contain up to `n/2` nodes, making the space complexity `O(n)`.

## Key Learning Points

  - **BFS for Level-Order**: Breadth-First Search is the definitive algorithm for any problem that requires processing a tree level by level.
  - **Level Processing Pattern**: The pattern of `level_size = len(queue)` followed by a `for _ in range(level_size)` loop is the standard and robust way to process all nodes on a single level before moving to the next.
  - **`collections.deque`**: This is the ideal data structure for implementing a queue in Python, providing efficient `O(1)` appends and `poplefts`.