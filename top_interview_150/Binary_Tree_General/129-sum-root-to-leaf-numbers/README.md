# 129\. Sum Root to Leaf Numbers - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree where each node contains a single digit (0-9). The task is to calculate the sum of all numbers represented by the root-to-leaf paths.

**Path-to-Number Definition:**
A path from the root to a leaf forms a number. For example, the path `1 -> 2 -> 3` represents the integer `123`.

**Examples:**

```python
Input: root = [1,2,3]
Output: 25
Explanation:
- The path 1->2 represents the number 12.
- The path 1->3 represents the number 13.
- The total sum is 12 + 13 = 25.

Input: root = [4,9,0,5,1]
Output: 1026
Explanation:
- The path 4->9->5 represents 495.
- The path 4->9->1 represents 491.
- The path 4->0 represents 40.
- The total sum is 495 + 491 + 40 = 1026.
```

## Key Insights

### Traversing with Memory

The problem requires us to process **root-to-leaf paths**. This immediately suggests a **Depth-First Search (DFS)**, as it naturally explores one full path at a time.

The key challenge is that as we traverse down the tree, we need to "build" the number represented by the path. This means our traversal function needs to carry some information with it—the "number formed so far."

### The "Number Building" Formula

As we move from a parent node to a child node, we are essentially appending a new digit to our number.

  - If we have the number `12` and we move to a child with value `3`, the new number is `123`.
  - The mathematical formula for this is: `new_number = previous_number * 10 + new_digit`.

This formula, combined with a recursive DFS, provides an elegant way to solve the problem.

## Solution Approach

This solution uses a recursive helper function, `dfs`. This function performs a pre-order traversal of the tree. It takes the current `node` and the `current_number` formed by the path to its parent as arguments. It calculates the number for the current path and, if it reaches a leaf, returns that number. Otherwise, it returns the sum of the results from its children's recursive calls.

```python
from typing import Optional

class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        
        def dfs(node: Optional[TreeNode], current_number: int) -> int:
            # Base Case 1: An empty branch contributes 0 to the sum.
            if not node:
                return 0

            # Update the number formed by the path down to the current node.
            current_number = current_number * 10 + node.val

            # Base Case 2: If the current node is a leaf, this path is complete.
            # We've found a full number, so we return it.
            if not node.left and not node.right:
                return current_number
            
            # Recursive Step: If it's not a leaf, the total sum from this point down
            # is the sum of the paths in the left subtree plus the sum of the paths
            # in the right subtree.
            return dfs(node.left, current_number) + dfs(node.right, current_number)

        # Start the entire recursive process from the root with an initial number of 0.
        return dfs(root, 0)
```

## Detailed Code Analysis

### The `dfs(node, current_number)` Helper Function

This is the core of the algorithm. It's designed to answer the question: "Starting from `node`, what is the sum of all root-to-leaf numbers that pass through this node, given that the number formed to get here was `current_number`?"

**1. The Base Case for Null Nodes**

```python
if not node:
    return 0
```

  - This is our primary stopping condition. If we try to traverse to a child that doesn't exist (e.g., `node.left` of a leaf), we hit this base case. An empty path contributes nothing (`0`) to the total sum.

**2. The Number Building Step**

```python
current_number = current_number * 10 + node.val
```

  - This is the first action we take for a valid node. We update the number passed down from the parent with the current node's digit.

**3. The Base Case for Leaf Nodes**

```python
if not node.left and not node.right:
    return current_number
```

  - This is the goal condition. A node is a leaf if both its children are `None`. When we reach a leaf, we have formed a complete root-to-leaf number. We return this number up the call stack.

**4. The Recursive Step**

```python
return dfs(node.left, current_number) + dfs(node.right, current_number)
```

  - If the current node is not a leaf, it's an intermediate node on one or more paths. The total sum for the subtree rooted here is the sum of whatever its left child finds plus the sum of whatever its right child finds.
  - We make two recursive calls, passing the newly updated `current_number` down to both children.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `root = [4, 9, 0, 5, 1]` and `targetSum = 1026` (wait, the problem is Sum Root to Leaf Numbers, not path sum). Let's trace `root = [1, 2, 3]`.

**Tree Structure:**

```
      1
     / \
    2   3
```

The indented lines represent the recursive call stack.

1.  **`sumNumbers()` calls `dfs(node=1, current_number=0)`**

      - `current_number` becomes `0 * 10 + 1 = 1`.
      - Node 1 is not a leaf.
      - It will return `dfs(node=2, 1) + dfs(node=3, 1)`.

2.  **`dfs(node=2, current_number=1)` is called.**

      - `current_number` becomes `1 * 10 + 2 = 12`.
      - Node 2 **is a leaf**.
      - It hits the leaf base case and **returns `12`**.

3.  **`dfs(node=3, current_number=1)` is called.**

      - `current_number` becomes `1 * 10 + 3 = 13`.
      - Node 3 **is a leaf**.
      - It hits the leaf base case and **returns `13`**.

4.  **Control returns to the top-level call** `dfs(node=1)`.

      - It receives `12` from its left child and `13` from its right child.
      - It calculates the final sum: `12 + 13 = 25`.
      - It returns **25**.

The final result is **25**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The DFS algorithm visits every node exactly once.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by the recursion call stack.
  - **Worst Case**: `O(n)` for a completely skewed tree.
  - **Best Case**: `O(log n)` for a completely balanced tree.