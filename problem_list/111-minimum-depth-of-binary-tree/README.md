# 111\. Minimum Depth of Binary Tree - Solution Explanation

## Problem Overview

Given the `root` of a binary tree, the task is to find its **minimum depth**.

**Minimum Depth Definition:**
The minimum depth is the number of nodes along the **shortest path** from the root node down to the **nearest leaf node**.

**Key Definitions:**

  - **Path**: A sequence of nodes from the root downwards.
  - **Leaf Node**: A node that has no children (both its `left` and `right` pointers are `None`).

**Examples:**

```python
Input: root = [3,9,20,null,null,15,7]
Output: 2
Explanation: The root is 3. Its left child is 9, which is a leaf.
The path 3 -> 9 has 2 nodes, which is the shortest path to any leaf.

Input: root = [2,null,3,null,4,null,5,null,6]
Output: 5
Explanation: This is a skewed tree. The only leaf is node 6.
The path is 2 -> 3 -> 4 -> 5 -> 6, which has 5 nodes.
```

## Key Insights

### Shortest Path Implies Breadth-First Search (BFS)

The phrase **"minimum depth"** or **"shortest path"** is a major clue. When you need to find the shortest path in a graph where every step has the same "cost" (like moving one level down in a tree), the ideal algorithm is **Breadth-First Search (BFS)**.

### Level-by-Level Exploration

BFS works by exploring the tree in layers, or "levels." It starts at the root (Level 0), then visits all of the root's children (Level 1), then all of their children (Level 2), and so on. Because of this systematic, outward-expanding search, the **first time BFS encounters a leaf node, it is guaranteed to be the nearest one**, and its depth will be the minimum depth of the tree.

## Solution Approach

This solution implements the BFS algorithm using a queue. The queue will store not just the nodes to visit, but also their current depth, allowing us to immediately return the depth when we find the first leaf.

```python
import collections
from typing import Optional

class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        # Base case: If the tree is empty, its depth is 0.
        if not root:
            return 0
        
        # Initialize a queue for BFS. We store tuples of (node, depth).
        # The root node starts at depth 1.
        queue = collections.deque([(root, 1)])
        
        # Continue as long as there are nodes to process.
        while queue:
            # Get the next node and its depth from the front of the queue.
            node, depth = queue.popleft()
            
            # Check if this node is a leaf (it has no children).
            if not node.left and not node.right:
                # Since BFS finds the shallowest leaf first, we can
                # immediately return its depth as the answer.
                return depth
            
            # If it's not a leaf, add its existing children to the back of the queue.
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))
```

## Detailed Code Analysis

### Step 1: The Base Case

```python
if not root:
    return 0
```

  - This handles the edge case where the input tree is empty. An empty tree has no nodes and therefore a depth of `0`.

### Step 2: Queue Initialization

```python
queue = collections.deque([(root, 1)])
```

  - `collections.deque` is a highly efficient queue implementation in Python.
  - We don't just add the `root` node; we add a tuple `(root, 1)`. This is how we keep track of the depth of each node as we traverse. The root is considered to be at depth `1`.

### Step 3: The Main Loop

```python
while queue:
```

  - This loop will continue as long as there are nodes in the queue waiting to be processed.

### Step 4: Dequeueing

```python
node, depth = queue.popleft()
```

  - Inside the loop, `popleft()` removes and returns the item from the front of the queue (First-In, First-Out). This ensures we process nodes in the order of their level. We unpack the tuple into our `node` and `depth` variables.

### Step 5: The Goal Check (Finding a Leaf)

```python
if not node.left and not node.right:
    return depth
```

  - This is the most important check. For each node we process, we first see if it's a leaf.
  - If it is, we have found our answer. Because BFS guarantees we find the shallowest nodes first, this must be a leaf at the minimum possible depth. We can stop the entire process and return its `depth`.

### Step 6: Enqueueing Children

```python
if node.left:
    queue.append((node.left, depth + 1))
if node.right:
    queue.append((node.right, depth + 1))
```

  - If the current node is not a leaf, we continue the search by adding its children to the back of the queue.
  - Crucially, when we add them, we also pass along their depth, which is the parent's `depth + 1`.

## Step-by-Step Execution Trace

### Example: `root = [3, 9, 20, null, null, 15, 7]`

1.  **Initialization**: The `queue` starts as `deque([(Node(3), 1)])`.

| Action | `queue` state | Dequeued `(node, depth)` | Is it a leaf? | Return Value |
| :--- | :--- | :--- | :--- | :--- |
| **Start** | `deque([(Node(3), 1)])` | - | - | - |
| **Dequeue** | `deque([])` | `(Node(3), 1)` | No | - |
| **Enqueue Children** | `deque([(Node(9), 2), (Node(20), 2)])`| | | - |
| **Dequeue** | `deque([(Node(20), 2)])` | `(Node(9), 2)` | **Yes\!** | - |
| **Found Leaf\!** | - | - | - | **Return `depth` (2)** |

  - The process stops and returns **2** as soon as it processes `Node(9)`, because it is the first leaf node encountered. It never needs to process `Node(20)` or its children.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. In the best case (if the root has a leaf child), the algorithm can be faster, but in the worst case (a skewed tree), it will visit every node once.

### Space Complexity: O(w)

  - Where `w` is the maximum width of the tree. This is the maximum number of nodes that can be in the `queue` at one time, which corresponds to the number of nodes on the tree's widest level.

## Why BFS is Perfect for this Problem

BFS systematically explores the tree level by level. Think of it as sending out a search party from the root.

  - **Wave 1** visits all nodes at depth 1 (the root).
  - **Wave 2** visits all nodes at depth 2 (the root's children).
  - **Wave 3** visits all nodes at depth 3, and so on.

Because it never proceeds to a deeper level until the current level is fully explored, the first leaf it finds is guaranteed to be on the shallowest possible level. A Depth-First Search (DFS), in contrast, would dive deep down one path first, potentially finding a very deep leaf before finding a much shallower one in another branch.