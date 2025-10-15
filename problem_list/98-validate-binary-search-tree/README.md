# 98\. Validate Binary Search Tree - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree. The task is to determine if it is a **valid Binary Search Tree (BST)**.

**Definition of a Valid BST:** 🌳
A BST is a tree that follows a specific set of ordering rules:

1.  For any given node, all values in its **left subtree** must be **strictly less than** the node's own value.
2.  For any given node, all values in its **right subtree** must be **strictly greater than** the node's own value.
3.  Both the left and right subtrees must also be valid binary search trees themselves.

**Example of an Invalid Tree:**

```
    5
   / \
  1   4  <-- Invalid! 4 is in the right subtree of 5, but 4 is not > 5.
     / \
    3   6
```

## Key Insights

### The Common Trap

The most common mistake is to only check a node against its immediate children. For example, checking only `if node.left.val < node.val and node.right.val > node.val`. This is **not sufficient**. The BST property must hold for *all* descendants, not just the direct children. In the example above, the root's right child (4) is less than the root (5), violating the rule.

### The "Valid Range" Insight

The correct way to think about this is that each node in the tree must lie within a specific **valid range** of values.

  - The `root` node can be anything (its range is from negative infinity to positive infinity).
  - When we move to a `root`'s **left child**, we know that this child and all *its* descendants must be *less than* the `root`'s value. So, the `root`'s value becomes the new **upper bound** for the entire left subtree.
  - Similarly, when we move to a `root`'s **right child**, that child and all *its* descendants must be *greater than* the `root`'s value. So, the `root`'s value becomes the new **lower bound** for the entire right subtree.

This "passing down the bounds" logic is a perfect fit for a recursive solution.

## Solution Approach

This solution uses a recursive helper function, `validate`. This function performs a depth-first search of the tree, carrying the valid `lower_bound` and `upper_bound` for each node it visits.

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        
        def validate(node, lower_bound, upper_bound):
            # Base Case: An empty tree is a valid BST.
            if not node:
                return True
            
            # Check if the current node's value is within its valid range.
            # It must be > lower_bound AND < upper_bound.
            if not (lower_bound < node.val < upper_bound):
                return False
                
            # Recursively check the left and right subtrees with updated bounds.
            # For the left child, the parent's value becomes the new upper bound.
            is_left_valid = validate(node.left, lower_bound, node.val)
            # For the right child, the parent's value becomes the new lower bound.
            is_right_valid = validate(node.right, node.val, upper_bound)
            
            # The tree is valid only if the current node is valid AND
            # both of its subtrees are also valid.
            return is_left_valid and is_right_valid

        # Start the initial validation on the root with the widest possible range.
        return validate(root, float('-inf'), float('inf'))
```

## Detailed Code Analysis

### The `validate(node, lower_bound, upper_bound)` Helper

This is the core of the algorithm. It answers the question: "Is the tree rooted at `node` a valid BST, given that all its values must be between `lower_bound` and `upper_bound`?"

**1. The Base Case**

```python
if not node:
    return True
```

  - This is our stopping condition for the recursion. If we reach a `None` node (the child of a leaf), it represents an empty but valid subtree. So, we return `True`.

**2. The Current Node's Validation**

```python
if not (lower_bound < node.val < upper_bound):
    return False
```

  - This is the main validation check. Before checking its children, the function first checks if the `node` itself is valid.
  - Its value must be strictly greater than the `lower_bound` and strictly less than the `upper_bound` passed down from its ancestors. If it fails this check, we know immediately that the entire tree is invalid, and we can return `False`.

**3. The Recursive Calls (Passing Down Constraints)**

```python
is_left_valid = validate(node.left, lower_bound, node.val)
is_right_valid = validate(node.right, node.val, upper_bound)
```

  - This is where we "pass down the bounds."
  - **For the left child**: The `lower_bound` stays the same as what the parent had, but the **`upper_bound` is now the parent's value (`node.val`)**. This ensures everything in the left subtree is less than the parent.
  - **For the right child**: The `upper_bound` stays the same, but the **`lower_bound` is now the parent's value (`node.val`)**. This ensures everything in the right subtree is greater than the parent.

**4. Combining the Results**

```python
return is_left_valid and is_right_valid
```

  - A tree is only a valid BST if the current node is valid (which we already checked) AND its left subtree is a valid BST AND its right subtree is a valid BST. This line ensures that a `False` result from anywhere deep in the tree will correctly bubble up and cause the final result to be `False`.

## Step-by-Step Execution Trace

Let's trace the invalid example `root = [5, 1, 4, null, null, 3, 6]`.

1.  **`isValidBST()` calls `validate(Node(5), -inf, +inf)`**

      - `5` is between `-inf` and `+inf`. OK.
      - Calls `validate(Node(1), -inf, 5)` for the left child.
      - Calls `validate(Node(4), 5, +inf)` for the right child.

2.  **`validate(Node(1), -inf, 5)` runs.**

      - `1` is between `-inf` and `5`. OK.
      - Its children are `None`, so the recursive calls on them will return `True`.
      - This branch returns **`True`**.

3.  **`validate(Node(4), 5, +inf)` runs.**

      - The function checks `if not (5 < 4 < +inf)`.
      - The condition `5 < 4` is **`False`**. The `not` makes the whole check **`True`**.
      - It enters the `if` block and immediately **returns `False`**.

4.  **Back at the top-level call `validate(Node(5), ...)`:**

      - It receives `is_left_valid = True` from the left call.
      - It receives `is_right_valid = False` from the right call.
      - It executes `return True and False`.
      - The final result is **`False`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The algorithm visits every node in the tree exactly once.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by the recursion call stack.
  - **Worst Case**: `O(n)` for a completely skewed tree that resembles a linked list.
  - **Best Case**: `O(log n)` for a completely balanced tree.