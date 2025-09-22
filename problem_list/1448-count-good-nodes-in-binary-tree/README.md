# 1448\. Count Good Nodes in Binary Tree - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree. The task is to count the number of **"good nodes"**.

**"Good Node" Definition:**
A node is considered "good" if, on the path from the root to that node, there are **no nodes with a value greater than it**. In simpler terms, the node's value must be greater than or equal to the values of all its ancestors.

**Examples:**

```python
Input: root = [3,1,4,3,null,1,5]
Output: 4

# Tree Structure:
#       3  (Good, path [3])
#      / \
#     1   4  (Good, path [3,4])
#    /   / \
#   3   1   5 (Good, path [3,4,5])
# (Good, path [3,1,3])

Explanation:
- The root (3) is always good.
- In path (3 -> 4), 4 is the max. Good.
- In path (3 -> 4 -> 5), 5 is the max. Good.
- In path (3 -> 1 -> 3), the second 3 is the max. Good.
- Node 1 in path (3 -> 1) is not good because 3 > 1.
```

## Key Insights

### A Path-Dependent Problem

The "goodness" of a node is not an intrinsic property; it depends entirely on the values of its ancestors (the nodes on the path from the root). This tells us we need a traversal algorithm that can "remember" information about the path taken so far.

### Depth-First Search (DFS) with State

A **Depth-First Search (DFS)**, which naturally explores one path to its conclusion before backtracking, is the perfect way to solve this. We can implement DFS using recursion.

The key insight is that as we travel down a path, the only piece of information we need to carry with us is the **maximum value seen so far** on that path. When we visit a new node, we can instantly compare its value to this "max so far" to determine if it's a good node.

## Solution Approach

This solution uses a recursive helper function, `dfs`, to perform a pre-order traversal of the tree. This function keeps track of the maximum value encountered on the path from the root down to the current node.

```python
from typing import Optional

class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        
        def dfs(node: Optional[TreeNode], max_so_far: int) -> int:
            # Base Case: If we are at a null node, it can't be a good node.
            if not node:
                return 0
            
            # --- Check the current node ---
            # Initialize a count for this subtree. If the current node is good, count it.
            count = 1 if node.val >= max_so_far else 0
            
            # --- Propagate to children ---
            # Update the max value for the path going down to the children.
            new_max = max(max_so_far, node.val)
            
            # Recursively call on the left and right children and add their results.
            count += dfs(node.left, new_max)
            count += dfs(node.right, new_max)
            
            return count

        # Start the recursion from the root. The initial max value should be
        # very small to ensure the root node is always counted.
        return dfs(root, float('-inf'))
```

## Detailed Code Analysis

### The `dfs` Helper Function

This function is the core of the algorithm. It's designed to answer the question: "Starting from `node`, and given that the max value on the path to get here was `max_so_far`, how many good nodes are in this subtree?"

**1. The Base Case**

```python
if not node:
    return 0
```

  - This is the stopping condition for the recursion. An empty branch (`None`) contains zero good nodes.

**2. The "Good Node" Check**

```python
count = 1 if node.val >= max_so_far else 0
```

  - This line determines if the *current* node is good. It compares the node's value to the maximum value passed down from its parent.
  - If `node.val` is greater than or equal to `max_so_far`, we initialize our local `count` to `1`. Otherwise, it's `0`.

**3. Updating and Passing State**

```python
new_max = max(max_so_far, node.val)
```

  - Before we visit the children, we must update the maximum value for the path. The `new_max` for the children's path will be the greater of the previous max and the current node's value.

**4. The Recursive Calls**

```python
count += dfs(node.left, new_max)
count += dfs(node.right, new_max)
```

  - Here, we recursively call `dfs` on the left and right children, passing the `new_max` value down.
  - The results from these calls (the number of good nodes in the left and right subtrees) are added to our `count`.

**5. The Initial Call**

```python
return dfs(root, float('-inf'))
```

  - We kick off the entire process by calling `dfs` on the `root`.
  - We pass `float('-inf')` (negative infinity) as the initial `max_so_far`. This is a clean way to guarantee that the root node's value will always be greater than or equal to the initial max, ensuring it's correctly counted as the first good node.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `root = [3, 1, 4, 3]` with extreme detail.
**Tree Structure:**

```
      3
     / \
    1   4
   /
  3
```

The indented lines represent the recursive call stack.

1.  **`dfs(node=3, max_so_far=-inf)` is called.**

      - `3 >= -inf` is True. `count` is initialized to `1`.
      - `new_max` becomes `max(-inf, 3) = 3`.
      - Calls `dfs(node=1, max_so_far=3)`.

2.  **`dfs(node=1, max_so_far=3)` is called.**

      - `1 >= 3` is False. `count` is initialized to `0`.
      - `new_max` becomes `max(3, 1) = 3`.
      - Calls `dfs(node=3, max_so_far=3)`.

3.  **`dfs(node=3, max_so_far=3)` is called.**

      - `3 >= 3` is True. `count` is initialized to `1`.
      - `new_max` becomes `max(3, 3) = 3`.
      - Calls `dfs(node=None, max_so_far=3)`, which returns `0`.
      - Calls `dfs(node=None, max_so_far=3)`, which returns `0`.
      - This call returns `1 + 0 + 0 = 1`.

4.  Control returns to **`dfs(node=1)`**.

      - It received `1` from its left child call. `count` is now `0 + 1 = 1`.
      - Calls `dfs(node=None, max_so_far=3)` on its right child, which returns `0`.
      - `count` is now `1 + 0 = 1`.
      - This call returns `1`.

5.  Control returns to the top-level **`dfs(node=3)`**.

      - It received `1` from its left child call (`dfs(node=1)`). `count` is now `1 + 1 = 2`.
      - Calls `dfs(node=4, max_so_far=3)`.

6.  **`dfs(node=4, max_so_far=3)` is called.**

      - `4 >= 3` is True. `count` is initialized to `1`.
      - `new_max` becomes `max(3, 4) = 4`.
      - Its children are `None`, so the two recursive calls will both return `0`.
      - This call returns `1 + 0 + 0 = 1`.

7.  Control returns to the top-level **`dfs(node=3)`**.

      - It received `1` from its right child call (`dfs(node=4)`). `count` is now `2 + 1 = 3`.

8.  The function finishes and returns the final count of **3**. Wait, the example output is 4. Let's re-trace the example. `[3,1,4,3,null,1,5]`

**Corrected Trace for `root = [3,1,4,3,null,1,5]`**

```
dfs(3, -inf) -> count=1, new_max=3
  dfs(1, 3) -> count=0, new_max=3
    dfs(3, 3) -> count=1, new_max=3
      returns 1
    returns 0 + 1 + 0 = 1
  dfs(4, 3) -> count=1, new_max=4
    dfs(1, 4) -> count=0, new_max=4
      returns 0
    dfs(5, 4) -> count=1, new_max=5
      returns 1
    returns 1 + 0 + 1 = 2
  returns 1 + 1 + 2 = 4
```

The final result is **4**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The DFS algorithm visits every node exactly once.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by the recursion call stack.
  - **Worst Case**: `O(n)` for a completely skewed tree.
  - **Best Case**: `O(log n)` for a completely balanced tree.

## Key Learning Points

  - **DFS for Path Problems**: Depth-First Search is a natural fit for tree problems where the condition for a node depends on the path from the root to that node.
  - **Passing State via Recursion**: The technique of passing state (like `max_so_far`) down through recursive calls is a fundamental and powerful pattern in programming.
  - A complex problem can be solved by a simple recursive function that asks the right question at each node.