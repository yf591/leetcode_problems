# 110\. Balanced Binary Tree - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree. The task is to determine if the tree is **height-balanced**.

**Height-Balanced Definition:**
A binary tree is height-balanced if, for **every node** in the tree, the absolute difference between the height of its left subtree and the height of its right subtree is **no more than 1**.

**Examples:**

```python
Input: root = [3,9,20,null,null,15,7]
Output: true
# This tree is balanced at every node.

Input: root = [1,2,2,3,3,null,null,4,4]
Output: false
# The subtree at node 2 is unbalanced. Its left child (3) has a height of 2,
# while its right child (3) has a height of 1. But the root of that subtree, the node 2,
# has a left subtree of height 2 (rooted at 3) and a right subtree of height 0 (null),
# which is a difference of 2.
# More critically, the root node (1) has a left subtree of height 3 and a right subtree of height 1.
# The difference is 2, which is > 1.
```

## Key Insights

### The Recursive Nature of Balance

The definition of a balanced tree is inherently recursive. A tree is balanced if and only if:

1.  Its left subtree is balanced.
2.  Its right subtree is balanced.
3.  The heights of its left and right subtrees differ by at most 1.

### Avoiding Redundant Calculations

A naive approach would be to create a `getHeight()` function. Then, for every node in the tree, we would call `getHeight(node.left)` and `getHeight(node.right)` and check the difference. This is very inefficient (`O(n log n)`) because we would be recalculating the heights of the same subtrees over and over again as we move up the tree.

The key insight for an optimal `O(n)` solution is to combine the height calculation and the balance check into a **single traversal**. We can do this with a recursive helper function that works from the **bottom up**. As it calculates the height of a subtree, it simultaneously checks if that subtree is balanced.

## Solution Approach

This solution uses a recursive helper function (a post-order traversal) that cleverly uses its return value to pass two pieces of information: the height of a subtree and whether it's balanced.

  - If a subtree is **balanced**, the function returns its **height** (a non-negative integer).
  - If a subtree is **unbalanced**, the function immediately returns a special signal value, **-1**, to indicate failure.

Any parent node that receives a `-1` from one of its children knows that an imbalance exists below it, and it can immediately stop and propagate the `-1` signal up the call stack.

```python
from typing import Optional

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        
        def check_height(node: Optional[TreeNode]) -> int:
            """
            This helper function returns the height of a node if it's balanced,
            or -1 if it's unbalanced.
            """
            # Base Case: An empty tree is balanced and has a height of 0.
            if not node:
                return 0

            # Recursively check the left subtree.
            left_height = check_height(node.left)
            # If the left subtree is unbalanced, propagate the failure signal up.
            if left_height == -1:
                return -1

            # Recursively check the right subtree.
            right_height = check_height(node.right)
            # If the right subtree is unbalanced, propagate the failure signal up.
            if right_height == -1:
                return -1

            # Check if the current node is balanced.
            if abs(left_height - right_height) > 1:
                return -1  # Signal that this node is the point of imbalance.

            # If it is balanced, return its height for the parent node to use.
            return 1 + max(left_height, right_height)

        # The entire tree is balanced if the top-level check doesn't return -1.
        return check_height(root) != -1
```

## Detailed Code Analysis

### The `check_height` Helper Function

This is the core of the algorithm. It's a post-order traversal because it processes its children *before* processing itself.

**1. The Base Case**

```python
if not node:
    return 0
```

  - This is our stopping condition. An empty subtree (`None`) is perfectly balanced by definition, and its height is 0.

**2. The Recursive Calls**

```python
left_height = check_height(node.left)
if left_height == -1:
    return -1

right_height = check_height(node.right)
if right_height == -1:
    return -1
```

  - The function calls itself on its left and right children first.
  - Crucially, after each call, it checks if the returned value was the failure signal (`-1`). If it was, it means an imbalance was found deeper in the tree, so we don't need to do any more work for this branch. We just immediately pass the `-1` signal up to the parent.

**3. The Balance Check**

```python
if abs(left_height - right_height) > 1:
    return -1
```

  - This check only happens if both the left and right subtrees were themselves balanced. It checks the balance condition at the *current* node. If the heights differ by more than 1, this node is the source of an imbalance, so we return `-1`.

**4. The Success Return Value**

```python
return 1 + max(left_height, right_height)
```

  - If all checks pass, the current node and its subtrees are balanced. The function then returns the correct height of the subtree rooted at this node, which is `1` (for the node itself) plus the height of its tallest child.

## Step-by-Step Execution Trace

Let's trace the algorithm with the unbalanced example: `root = [1, 2, 2, 3, 3, null, null, 4, 4]`

**Tree Structure:**

```
      1
     / \
    2   2
   / \
  3   3
 / \
4   4
```

The execution works from the bottom up as the recursive calls return.

1.  **`check_height(node=1)` is called.** It recursively calls `check_height(node=2)` on its left.
2.  **`check_height(node=2)` is called.** It recursively calls `check_height(node=3)` on its left.
3.  **`check_height(node=3)` is called.** It recursively calls `check_height(node=4)` on its left.
4.  **`check_height(node=4)` is called.** It's a leaf. Its left and right children are `None`. The calls `check_height(None)` return `0`.
      - `left_height = 0`, `right_height = 0`.
      - `abs(0 - 0) <= 1`. It's balanced.
      - It returns its height: `1 + max(0, 0) = 1`.
5.  Control returns to **`check_height(node=3)`**.
      - It received `left_height = 1` (from the call on node 4).
      - It calls `check_height` on its right child (the other node 4), which also returns a height of `1`.
      - `left_height = 1`, `right_height = 1`.
      - `abs(1 - 1) <= 1`. It's balanced.
      - It returns its height: `1 + max(1, 1) = 2`.
6.  Control returns to **`check_height(node=2)`**.
      - It received `left_height = 2` (from the call on node 3).
      - It calls `check_height` on its right child (the other node 3). A similar process occurs, and it will return a height of `1`.
      - Now, at `node=2`, we have `left_height = 2` and `right_height = 1`.
      - `abs(2 - 1) <= 1`. The node `2` itself is balanced.
      - It returns its height: `1 + max(2, 1) = 3`.
7.  Control returns to **`check_height(node=1)`**.
      - It received `left_height = 3` (from the call on node 2).
      - It calls `check_height` on its right child (the other node 2). This node is a leaf, so it will return a height of `1`.
      - Now, at the `root` (node 1), we have `left_height = 3` and `right_height = 1`.
8.  **The Imbalance is Found\!**
      - The code checks the condition: `if abs(left_height - right_height) > 1`.
      - `abs(3 - 1)` is `2`.
      - `2 > 1` is **True**. An imbalance is detected at the root.
      - The function immediately returns the failure signal: **-1**.
9.  **Final Result**:
      - The initial call `isBalanced` receives the `-1`.
      - The final line `return check_height(root) != -1` evaluates to `return -1 != -1`, which is **`False`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes. This algorithm is a post-order traversal, which visits every node exactly once.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by the recursion call stack.
  - **Worst Case**: `O(n)` for a completely skewed (unbalanced) tree.
  - **Best Case**: `O(log n)` for a completely balanced tree.

## Key Learning Points

  - **Post-Order Traversal**: This "bottom-up" approach, where you process children before the parent, is very powerful for problems that depend on subtree properties (like height).
  - **Multi-purpose Return Values**: Using a special value (like `-1` or `None`) to signal failure is a clean and efficient way to stop recursion early and propagate an error condition up the call stack without using global flags.
  - This solution avoids the `O(n log n)` complexity of a naive top-down approach by calculating height and checking balance in a single, efficient pass.