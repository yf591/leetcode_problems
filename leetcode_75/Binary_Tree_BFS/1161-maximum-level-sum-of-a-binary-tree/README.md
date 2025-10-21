# 1161\. Maximum Level Sum of a Binary Tree - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree. The levels are numbered starting from **1** (root is level 1, its children are level 2, etc.). The task is to find the **level number** that has the **maximum sum** of node values. If multiple levels have the same maximum sum, you should return the **smallest** (earliest) level number.

**Examples:**

```python
Input: root = [1,7,0,7,-8,null,null]
Output: 2
Explanation:
Level 1 sum = 1
Level 2 sum = 7 + 0 = 7
Level 3 sum = 7 + -8 = -1
The maximum sum is 7, which occurs at level 2.

Input: root = [989,null,10250,98693,-89388,null,null,null,-32127]
Output: 2
```

## Key Insights

### Level-by-Level Processing -\> Breadth-First Search (BFS)

The problem explicitly asks us to calculate sums **level by level**. This is a direct signal that the most appropriate algorithm is **Breadth-First Search (BFS)**. BFS naturally explores a tree layer by layer, visiting all nodes at the current depth before moving on to the next deeper level.

### Tracking the Maximum Sum and Level

While performing the BFS, we need to:

1.  Calculate the sum of node values for each level as we process it.
2.  Keep track of the largest sum we have encountered *so far* (`max_sum`).
3.  Keep track of the level number (`result_level`) where that `max_sum` was found.
4.  Remember the rule: if a new level's sum equals the current `max_sum`, we *do not* update `result_level` because we need the *smallest* level number. We only update `result_level` when we find a *strictly greater* sum.

## Solution Approach

This solution implements a standard BFS using a queue (`collections.deque`). It iterates through the tree level by level. In each iteration, it calculates the sum of the nodes on the current level and compares it with the maximum sum found so far, updating the result level if a new maximum is found.

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
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        # Although constraints say >= 1 node, handle empty tree just in case.
        if not root:
            return 0 
            
        # Initialize variables to track the best result found so far.
        max_sum = float('-inf') # Start with negative infinity
        result_level = 0        # Stores the level number of the max_sum
        current_level_number = 1 # Tracks the current level (1-indexed)
        
        # Initialize the queue for BFS
        queue = collections.deque([root])
        
        # Loop as long as there are levels to process.
        while queue:
            level_size = len(queue)
            current_level_sum = 0
            
            # Process all nodes on the current level.
            for _ in range(level_size):
                node = queue.popleft()
                current_level_sum += node.val
                
                # Add children for the next level.
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            # Check if this level's sum is the new maximum.
            if current_level_sum > max_sum:
                max_sum = current_level_sum
                result_level = current_level_number
                
            # Move to the next level number for the next iteration.
            current_level_number += 1
            
        return result_level
```

## Detailed Code Analysis

### Step 1: Initialization

```python
max_sum = float('-inf')
result_level = 0
current_level_number = 1
queue = collections.deque([root])
```

  - **`max_sum = float('-inf')`**: We initialize `max_sum` to negative infinity. This ensures that the sum of the very first level (the root) will always be greater and will correctly set our initial `max_sum` and `result_level`.
  - **`result_level = 0`**: Will store the level number (1-indexed) corresponding to `max_sum`.
  - **`current_level_number = 1`**: Tracks the level we are currently processing, starting from 1 as per the problem description.
  - **`queue = collections.deque([root])`**: Standard BFS queue initialization with the root node.

### Step 2: The Main (Level) Loop

```python
while queue:
```

  - This loop continues as long as there are nodes in the queue, meaning there are still levels to process. Each iteration processes one full level.

### Step 3: Level Processing (Inside the `while` loop)

```python
level_size = len(queue)
current_level_sum = 0
for _ in range(level_size):
    node = queue.popleft()
    current_level_sum += node.val
    if node.left:
        queue.append(node.left)
    if node.right:
        queue.append(node.right)
```

  - **`level_size = len(queue)`**: Captures the number of nodes on the *current* level before we start processing it.
  - **`current_level_sum = 0`**: Initializes the sum for this specific level.
  - **`for _ in range(level_size):`**: This inner loop iterates exactly `level_size` times.
      - `node = queue.popleft()`: Removes a node from the front.
      - `current_level_sum += node.val`: Accumulates the sum for the level.
      - `if node.left/right: queue.append(...)`: Adds children to the queue for the *next* level's processing.

### Step 4: Updating the Maximum

```python
if current_level_sum > max_sum:
    max_sum = current_level_sum
    result_level = current_level_number
```

  - This check happens *after* processing all nodes on a level and calculating `current_level_sum`.
  - We compare `current_level_sum` with the best `max_sum` found so far.
  - **Crucially, we use `>` (strictly greater than).** If the sums are equal, we do *not* update `result_level`, ensuring we keep the *smallest* level number in case of ties.
  - If the current level's sum is indeed greater, we update `max_sum` and store the `current_level_number` in `result_level`.

### Step 5: Advancing the Level Counter

```python
current_level_number += 1
```

  - We increment the level counter to prepare for the next iteration of the `while` loop.

### Step 6: Return Value

```python
return result_level
```

  - After the `while` loop finishes (the queue is empty), `result_level` holds the smallest level number that had the maximum sum.

## Step-by-Step Execution Trace

Let's trace the algorithm with `root = [1, 7, 0, 7, -8, null, null]` with extreme detail.

### **Initial State:**

  - `max_sum = -inf`
  - `result_level = 0`
  - `current_level_number = 1`
  - `queue = deque([Node(1)])`

-----

### **Level 1 (First `while` loop iteration)**

1.  `queue` is not empty.
2.  `level_size = 1`. `current_level_sum = 0`.
3.  Inner loop runs once:
      - `node = Node(1)` dequeued. `current_level_sum` becomes `1`.
      - `Node(1).left` (Node 7) enqueued.
      - `Node(1).right` (Node 0) enqueued.
4.  `queue` is now `deque([Node(7), Node(0)])`.
5.  Check max: `current_level_sum` (1) \> `max_sum` (-inf)? **Yes**.
      - `max_sum` becomes `1`.
      - `result_level` becomes `current_level_number` (1).
6.  Increment level: `current_level_number` becomes `2`.
    **State:** `max_sum = 1`, `result_level = 1`, `current_level = 2`

-----

### **Level 2 (Second `while` loop iteration)**

1.  `queue` is not empty.
2.  `level_size = 2`. `current_level_sum = 0`.
3.  Inner loop runs twice:
      - `node = Node(7)` dequeued. `current_level_sum` becomes `7`.
          - `Node(7).left` (Node 7) enqueued.
          - `Node(7).right` (Node -8) enqueued.
      - `node = Node(0)` dequeued. `current_level_sum` becomes `7 + 0 = 7`.
          - `Node(0)` has no children.
4.  `queue` is now `deque([Node(7), Node(-8)])`.
5.  Check max: `current_level_sum` (7) \> `max_sum` (1)? **Yes**.
      - `max_sum` becomes `7`.
      - `result_level` becomes `current_level_number` (2).
6.  Increment level: `current_level_number` becomes `3`.
    **State:** `max_sum = 7`, `result_level = 2`, `current_level = 3`

-----

### **Level 3 (Third `while` loop iteration)**

1.  `queue` is not empty.
2.  `level_size = 2`. `current_level_sum = 0`.
3.  Inner loop runs twice:
      - `node = Node(7)` dequeued. `current_level_sum` becomes `7`. No children.
      - `node = Node(-8)` dequeued. `current_level_sum` becomes `7 + (-8) = -1`. No children.
4.  `queue` is now empty `deque([])`.
5.  Check max: `current_level_sum` (-1) \> `max_sum` (7)? **No**.
6.  Increment level: `current_level_number` becomes `4`.
    **State:** `max_sum = 7`, `result_level = 2`, `current_level = 4`

-----

### **End of Traversal**

  - The `while queue:` condition is now **False**. The loop terminates.
  - The function returns the final `result_level`, which is **2**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The BFS algorithm visits each node exactly once.

### Space Complexity: O(w)

  - Where `w` is the **maximum width** of the tree. This is the maximum number of nodes that can be in the `queue` at any one time. In the worst case (a full, complete binary tree), the last level can contain up to `(n+1)/2` nodes, making the space complexity `O(n)`.