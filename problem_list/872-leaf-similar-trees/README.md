# 872\. Leaf-Similar Trees - Solution Explanation

## Problem Overview

You are given two binary trees, `root1` and `root2`. The task is to determine if they are **leaf-similar**.

**Leaf-Similar Definition:**
Two trees are considered leaf-similar if their **leaf value sequence** is the same. A leaf value sequence is created by reading the values of all the **leaf nodes** from **left to right**. A leaf is a node that has no children.

**Examples:**
Consider the two trees in the example:

  - **Tree 1**: Leaves, read left-to-right, are `[6, 7, 4, 9, 8]`.
  - **Tree 2**: Leaves, read left-to-right, are also `[6, 7, 4, 9, 8]`.
  - Since their leaf value sequences are identical, the trees are leaf-similar, and the output is `true`.

## Key Insights

### Decomposing the Problem

The problem "Are these two trees leaf-similar?" can be broken down into three simpler steps:

1.  Find the leaf value sequence for `tree1`.
2.  Find the leaf value sequence for `tree2`.
3.  Compare the two sequences.

This means we can focus on solving one core subproblem: "How do I get a left-to-right list of leaves for a single tree?"

### Traversal for "Left-to-Right" Order

To get the leaves in a "left-to-right" order, we need to use a traversal algorithm that guarantees it explores the left subtree of any node before it explores the right subtree. **Depth-First Search (DFS)** is a perfect and natural way to do this. We can implement DFS using recursion.

## Solution Approach

The solution uses a recursive helper function (`dfs`) to perform a Depth-First Search on each tree. This helper function finds all the leaves and adds their values to a list in the correct left-to-right order. Finally, the two lists of leaves are compared.

```python
from typing import Optional, List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        
        def dfs(node: Optional[TreeNode], leaves: List[int]):
            """
            A recursive helper to traverse the tree and collect leaf values.
            """
            # Base Case: If the node is None, stop this path.
            if not node:
                return
            
            # Check if the current node is a leaf (no left and no right child).
            if not node.left and not node.right:
                leaves.append(node.val)
            
            # Recursively traverse the left subtree first, then the right.
            # This ensures the left-to-right order.
            dfs(node.left, leaves)
            dfs(node.right, leaves)

        # Step 1: Get the leaf sequence for the first tree.
        leaves1 = []
        dfs(root1, leaves1)
        
        # Step 2: Get the leaf sequence for the second tree.
        leaves2 = []
        dfs(root2, leaves2)
        
        # Step 3: Compare the two sequences.
        return leaves1 == leaves2
```

## Detailed Code Analysis

### The `dfs` Helper Function

This is the core of the solution. It's designed to do one job: explore a tree and fill a given list with its leaf values.

**1. The Base Case**

```python
if not node:
    return
```

  - This is the most critical part of any recursive function. It provides the stopping condition. When the traversal reaches a `None` node (e.g., the child of a leaf), the function simply returns, and the program "unwinds" to the previous step.

**2. The Leaf Check**

```python
if not node.left and not node.right:
    leaves.append(node.val)
```

  - This condition checks if the current `node` is a leaf. A node is a leaf if and only if both its `left` and `right` children are `None`.
  - If it is a leaf, we add its value to the `leaves` list that was passed into the function.

**3. The Recursive Traversal**

```python
dfs(node.left, leaves)
dfs(node.right, leaves)
```

  - This is what drives the exploration. Crucially, we call `dfs` on the `left` child **before** calling it on the `right` child. This strict order guarantees that we will always discover and record the leaves on the left side of the tree before we discover the ones on the right side.

### The `leafSimilar` Main Function

```python
leaves1 = []
dfs(root1, leaves1)

leaves2 = []
dfs(root2, leaves2)
```

  - The main function first creates two empty lists, `leaves1` and `leaves2`.
  - It then calls the `dfs` helper function for each tree's root, passing in the corresponding list to be filled.

<!-- end list -->

```python
return leaves1 == leaves2
```

  - After both calls to `dfs` are complete, `leaves1` and `leaves2` contain the full, ordered leaf value sequences.
  - Python can directly compare two lists for equality with the `==` operator. It returns `True` if and only if they have the same elements in the same order.

## Step-by-Step Execution Trace

Let's trace `dfs` on a simple tree: `root = [3, 5, 1, 6, 2]`

**Tree Structure:**

```
      3
     / \
    5   1
   / \
  6   2
```

1.  **`dfs(node=3, leaves=[])`** is called.

      - Node 3 is not a leaf.
      - Call `dfs(node=5, leaves=[])`.

2.  **`dfs(node=5, leaves=[])`** is called.

      - Node 5 is not a leaf.
      - Call `dfs(node=6, leaves=[])`.

3.  **`dfs(node=6, leaves=[])`** is called.

      - Node 6 **is a leaf** (no children).
      - `leaves.append(6)`. The list is now `[6]`.
      - The function returns.

4.  Control returns to `dfs(node=5)`. It has finished the left side.

      - Now call `dfs(node=2, leaves=[6])`.

5.  **`dfs(node=2, leaves=[6])`** is called.

      - Node 2 **is a leaf**.
      - `leaves.append(2)`. The list is now `[6, 2]`.
      - The function returns.

6.  Control returns to `dfs(node=5)`. It has finished the right side. It returns.

7.  Control returns to `dfs(node=3)`. It has finished the left side.

      - Now call `dfs(node=1, leaves=[6, 2])`.

8.  **`dfs(node=1, leaves=[6, 2])`** is called.

      - Node 1 **is a leaf**.
      - `leaves.append(1)`. The list is now `[6, 2, 1]`.
      - The function returns.

9.  Control returns to `dfs(node=3)`. It has finished the right side. It returns.

10. The process is complete. The final leaf sequence is `[6, 2, 1]`.

## Performance Analysis

### Time Complexity: O(N1 + N2)

  - Where `N1` and `N2` are the number of nodes in `root1` and `root2`, respectively. The algorithm must visit every node in both trees exactly once.

### Space Complexity: O(H1 + H2 + L1 + L2)

  - This is the space required for the recursion call stacks and the lists of leaves.
  - `H1` and `H2` are the heights of the trees (for the recursion stack).
  - `L1` and `L2` are the number of leaves in the trees (for the lists).
  - In the worst case, this can be proportional to `O(N1 + N2)`.

## Key Learning Points

  - **Decomposition**: Breaking a complex problem into smaller, identical subproblems is a powerful strategy. Here, we broke "compare two trees" into "get sequence for one tree," which we solved twice.
  - **DFS for Ordered Traversal**: Depth-First Search is a fundamental tree traversal. By controlling the order of recursive calls (always visiting `left` before `right`), we can ensure a specific left-to-right processing order.
  - **Using Helper Functions**: A nested or helper function is a clean way to manage the logic and state (like the `leaves` list) of a recursive algorithm.