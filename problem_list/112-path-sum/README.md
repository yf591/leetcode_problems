# 112\. Path Sum - Solution Explanation

## Problem Overview

Given the `root` of a binary tree and a `targetSum`, the task is to determine if there exists a **root-to-leaf** path where the sum of all the node values along that path equals the `targetSum`.

**Key Definitions:**

  - **Root-to-leaf path**: A path that starts at the root node and ends at a leaf node.
  - **Leaf node**: A node that has no children (both its `left` and `right` pointers are `None`).

**Examples:**

```python
Input: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
Output: true
Explanation: The path 5 -> 4 -> 11 -> 2 has a sum of 5 + 4 + 11 + 2 = 22.

Input: root = [1,2,3], targetSum = 5
Output: false
Explanation: No root-to-leaf path sums to 5.
```

## Key Insights

### Recursive Path Exploration

This problem is about exploring paths. The most natural way to explore paths in a tree is with a **Depth-First Search (DFS)**, which is elegantly implemented using **recursion**.

The core idea is to think of the problem in terms of a "remaining sum." Instead of adding up values as we go down, we can subtract the node's value from the `targetSum` at each level.

  - At the root, we ask, "Can either of my children find a path that sums to `targetSum - my_value`?"
  - This question is then asked recursively by each child node until a leaf is reached.

### The Leaf Node Condition

The problem is specifically about **root-to-leaf** paths. This is a critical constraint. A path is only valid if it ends at a leaf node. When we reach a leaf, we must make our final check: does the remaining sum we're looking for exactly match this leaf's value?

## Solution Approach

This solution is a direct implementation of the recursive, top-down DFS strategy.

```python
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        # Base Case 1: An empty tree has no paths.
        if not root:
            return False

        # Subtract the current node's value from the target.
        remaining_sum = targetSum - root.val

        # Base Case 2: Check if the current node is a leaf.
        if not root.left and not root.right:
            # If it's a leaf, the path is valid only if the remaining sum is zero.
            return remaining_sum == 0
        
        # Recursive Step: If not a leaf, check the left OR the right subtree.
        return self.hasPathSum(root.left, remaining_sum) or self.hasPathSum(root.right, remaining_sum)
```

**Strategy:**

1.  **Handle Empty Tree**: First, check if the `root` is `None`. If so, no paths exist.
2.  **Update Target**: At the current node, calculate the `remaining_sum` needed for the rest of the path.
3.  **Check for Leaf**: Determine if the current node is a leaf. If it is, this is a stopping point. The path is valid only if the `remaining_sum` is now exactly zero.
4.  **Recurse**: If the node is not a leaf, recursively call the function on its left and right children with the `remaining_sum`. The `or` operator ensures that if a valid path is found in *either* subtree, the function will return `True`.

## Detailed Code Analysis

### Step 1: Entry Base Case

```python
if not root:
    return False
```

  - This handles the case where the input tree is empty from the start. It also serves as the stopping condition for recursive calls made on the children of leaf nodes (which are `None`).

### Step 2: Leaf Node Check (Recursive Base Case)

```python
if not root.left and not root.right:
    return remaining_sum == 0
```

  - This is the most important condition. It correctly identifies when a full root-to-leaf path has been traversed.
  - At this point, we perform the final check. `remaining_sum == 0` is `True` only if the sum of all values on the path from the root to this leaf equals the original `targetSum`.

### Step 3: The Recursive Step

```python
return self.hasPathSum(root.left, remaining_sum) or self.hasPathSum(root.right, remaining_sum)
```

  - This line elegantly explores the rest of the tree.
  - The `or` is crucial. It means, "Return `True` if you find a valid path in the left subtree, OR if you find one in the right subtree." Python's `or` uses short-circuiting, so if the left side search (`hasPathSum(root.left, ...)`) finds a valid path and returns `True`, the right side search will not even be executed.

## Step-by-Step Execution Trace

Let's visualize the recursive calls for `root = [5,4,8,...]` and `targetSum = 22`.

The function calls are represented by indentation.

```
1. hasPathSum(node=5, target=22)
   - remaining_sum = 17
   - Asks: hasPathSum(node=4, target=17) OR hasPathSum(node=8, target=17)?

2.   hasPathSum(node=4, target=17)
     - remaining_sum = 13
     - Asks: hasPathSum(node=11, target=13) OR hasPathSum(node=None, target=13)?

3.     hasPathSum(node=11, target=13)
       - remaining_sum = 2
       - Asks: hasPathSum(node=7, target=2) OR hasPathSum(node=2, target=2)?

4.       hasPathSum(node=7, target=2)
         - This is a LEAF node.
         - Is remaining_sum (2) == 0? No.
         - Returns False.

5.       hasPathSum(node=2, target=2)
         - This is a LEAF node.
         - Is remaining_sum (2) == 0? Yes.
         - Returns True.

6.     Back at call #3: The result is (False OR True) -> True. It returns True.
7.   Back at call #2: The result is (True OR ...) -> True. It returns True.
8. Back at call #1: The result is (True OR ...) -> True. It returns True.
```

The final answer is **`True`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. In the worst case, we have to visit every node once.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by the recursion call stack.
  - **Worst Case**: `O(n)` for a completely skewed tree.
  - **Best Case**: `O(log n)` for a completely balanced tree.

## Why the Leaf Node Check Matters

It's tempting to just check `if remaining_sum == 0` at any node. This would be wrong. The problem strictly defines the path as **root-to-leaf**.

  - Consider the tree `[1, 2]` with `targetSum = 1`.
  - The path `1` has a sum of 1. However, node `1` is not a leaf.
  - Our code correctly continues to the leaf `2`, where the path sum is `3`, and correctly returns `False`. The `if not root.left and not root.right:` check is essential.

## Key Learning Points

  - Using recursion (DFS) is a natural way to explore all paths in a tree.
  - The strategy of passing a "remaining value" down the recursion is very common and useful.
  - Clearly defining and handling base cases (empty node, leaf node) is the most critical part of a recursive tree solution.