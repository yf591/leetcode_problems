# 1372\. Longest ZigZag Path in a Binary Tree - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree. The task is to find the length of the longest **"ZigZag" path** in the tree.

**ZigZag Path Definition:**
A zigzag path is formed by starting at any node, choosing a direction (left or right), and then alternating directions for each subsequent step.

  - If you move right, the next move must be left.
  - If you move left, the next move must be right.

**Length Definition:**
The length of a path is the number of edges, which is the number of nodes visited minus one. A single node has a path length of 0.

**Examples:**

```python
Input: root = [1,1,1,null,1,null,null,1,1,null,1]
Output: 4
Explanation: The longest path goes left, then right, then left, then right. It has 5 nodes, so its length is 4.

Input: root = [1]
Output: 0
Explanation: A single node has a path length of 0.
```

## Key Insights

### Path Exploration with State

This problem requires exploring paths in a tree. A **Depth-First Search (DFS)**, typically implemented with recursion, is a natural way to do this.

However, a simple traversal isn't enough. As we move from a parent to a child, we need to "remember" two key pieces of information to continue the zigzag:

1.  **Direction**: Which direction did we just travel to get to the current node (left or right)? This tells us which direction we must go next to continue the path.
2.  **Length**: What is the length of the current zigzag path we are on?

### Every Node is a Potential Starting Point

A zigzag path can start at *any* node. This means that at every node we visit, we have two choices:

1.  **Continue the current zigzag path**: Make a move in the opposite direction of the one we just took.
2.  **Start a new zigzag path**: Abandon the current path and start a new one of length 1 by moving in either direction.

Our recursive algorithm needs to explore both of these possibilities at every node.

## Solution Approach

This solution uses a recursive DFS helper function. This function traverses the tree and explores all possible zigzag paths. An instance variable, `self.max_len`, is used to keep track of the longest path found anywhere in the tree across all the recursive calls.

```python
from typing import Optional

class Solution:
    def longestZigZag(self, root: Optional[TreeNode]) -> int:
        # This variable will store the maximum length found across all recursive calls.
        self.max_len = 0

        def dfs(node: Optional[TreeNode], came_from_left: bool, length: int):
            # Base Case: If we have moved to a null node, the path ends.
            if not node:
                return

            # At every node, the current path length is a candidate for the maximum.
            self.max_len = max(self.max_len, length)

            # Determine the next moves based on the direction we came from.
            if came_from_left:
                # We came from the LEFT, so...
                # 1. To CONTINUE the zigzag, we must go RIGHT. Length increases by 1.
                dfs(node.right, False, length + 1)
                
                # 2. We can also START A NEW zigzag by going LEFT again. Length resets to 1.
                dfs(node.left, True, 1)
            else: # came from RIGHT
                # We came from the RIGHT, so...
                # 1. To CONTINUE the zigzag, we must go LEFT. Length increases by 1.
                dfs(node.left, True, length + 1)
                
                # 2. We can also START A NEW zigzag by going RIGHT again. Length resets to 1.
                dfs(node.right, False, 1)
        
        # Start the process. A path of length 0 starts at the root. From there,
        # we can initiate a move to the left or right, creating paths of length 1.
        if not root:
            return 0
            
        dfs(root.left, True, 1)
        dfs(root.right, False, 1)
        
        return self.max_len
```

## Detailed Code Analysis

### `dfs(node, came_from_left, length)` Helper Function

This is the core of the algorithm. It's designed to explore the tree with all the necessary context.

  - `node`: The current node we are visiting.
  - `came_from_left`: A boolean (`True`/`False`) that tells us the direction of the move that **led to** the current `node`.
  - `length`: The length of the zigzag path that ended at the current `node`.

**1. The Base Case and Max Update**

```python
if not node:
    return
self.max_len = max(self.max_len, length)
```

  - The recursion stops when it reaches a `None` node.
  - At the beginning of every valid call, we update our global `self.max_len`. The `length` passed into the function is the length of the path *ending at the parent*, so this is a valid path length. *Correction*: The `length` passed in is the length ending at the *current* node. The logic in the code is correct, let me adjust my explanation. The code `dfs(root.left, True, 1)` means "we are now at `root.left`, we came from its parent (the root) via a left move, and the path has length 1". This is correct. So, at the start of `dfs`, `length` is the length of a valid path.

**2. The Recursive Logic**

```python
if came_from_left:
    # ... continue RIGHT, start new LEFT
else: 
    # ... continue LEFT, start new RIGHT
```

  - This block makes two recursive calls, exploring the two choices we have at every node:
  - **Continuing the Path**: To continue the zigzag, we must move in the opposite direction. For example, if we `came_from_left`, we continue by calling `dfs` on `node.right`, flipping the direction flag to `False`, and incrementing the length (`length + 1`).
  - **Starting a New Path**: We can always start a new path. To do this, we move in the *same* direction again. For example, if we `came_from_left`, we can start a new path by calling `dfs` on `node.left`. This new path consists of a single move, so its `length` is reset to `1`.

### The Initial Calls

```python
dfs(root.left, True, 1)
dfs(root.right, False, 1)
```

  - The main `longestZigZag` function just needs to kick off the process.
  - A zigzag path can start by moving left from the root or right from the root. Both of these initial moves create a path of length `1`. We make both initial calls to explore all possibilities.

## Step-by-Step Execution Trace

Let's trace the algorithm with a simple example: `root = [1, 2, 3, 4, 5]`

**Tree Structure:**

```
      1
     / \
    2   3
   / \
  4   5
```

1.  **Initial Calls**:

      - `longestZigZag` calls `dfs(node=2, came_from_left=True, length=1)`.
      - It also calls `dfs(node=3, came_from_left=False, length=1)`.

2.  **Trace `dfs(node=2, came_from_left=True, length=1)`**:

      - `max_len` is updated: `max(0, 1) = 1`.
      - Since `came_from_left` is `True`, it makes two calls:
          - **Continue Zigzag**: `dfs(node=5, came_from_left=False, length=2)`
          - **Start New Path**: `dfs(node=4, came_from_left=True, length=1)`

3.  **Trace `dfs(node=5, came_from_left=False, length=2)`**:

      - `max_len` is updated: `max(1, 2) = 2`.
      - Node 5 is a leaf, its children are `None`. The recursive calls will be `dfs(None, ...)` which will just return.

4.  **Trace `dfs(node=4, came_from_left=True, length=1)`**:

      - `max_len` is updated: `max(2, 1) = 2`. (No change).
      - Node 4 is a leaf. Its recursive calls will just return.

5.  The entire exploration of the left subtree of the root is now complete. The current `max_len` is `2`.

6.  Now the initial call `dfs(node=3, came_from_left=False, length=1)` executes.

      - `max_len` is updated: `max(2, 1) = 2`. (No change).
      - Node 3 is a leaf. Its recursive calls will just return.

7.  **Final Result**: The process is complete. The function returns the final `max_len`, which is **2**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The DFS algorithm visits every node a constant number of times.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by the recursion call stack.
  - **Worst Case**: `O(n)` for a completely skewed tree.
  - **Best Case**: `O(log n)` for a completely balanced tree.