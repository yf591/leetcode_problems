# 222\. Count Complete Tree Nodes - Solution Explanation

## Problem Overview

Given the `root` of a **complete binary tree**, the task is to return the total number of nodes in the tree.

**Key Definitions:**

  - **Complete Binary Tree**: A binary tree where every level, except possibly the last, is completely filled, and all nodes in the last level are as far left as possible.
  - **The Constraint**: The main challenge is to design an algorithm that is **faster than `O(n)`**, where `n` is the total number of nodes. This rules out a simple traversal that visits every node.

**Examples:**

```python
Input: root = [1,2,3,4,5,6]
Output: 6

Input: root = []
Output: 0
```

## Key Insights

### The `O(n)` Trap and the "Complete" Clue

A simple recursive or iterative traversal would visit every node, resulting in an `O(n)` solution. The constraint that the solution must be faster than `O(n)` forces us to leverage the special properties of a **complete** binary tree.

### The Perfect Tree Shortcut

If a binary tree is **perfect** (meaning all levels are completely full), we can calculate the number of nodes without visiting them all. A perfect binary tree of height `h` has exactly `2^h - 1` nodes. This formula is our shortcut.

### Finding Perfect Subtrees

The key insight is that any complete binary tree is composed of smaller perfect binary trees. We can identify these perfect subtrees by comparing the height of the tree's leftmost path with the height of its rightmost path. In a complete tree, we only need to check the "left-biased" height.

The core logic is:

1.  Calculate the height of the tree by only following `left` children from the root's left child. Let's call this `left_height`.
2.  Calculate the height of the tree by only following `left` children from the root's right child. Let's call this `right_height`.
3.  **If `left_height == right_height`**: This tells us the **left subtree is a perfect binary tree**. The last, incomplete level of the main tree must be in the right subtree.
4.  **If `left_height != right_height`**: This tells us the **right subtree is a perfect binary tree** (and is one level shorter). The last, incomplete level of the main tree must be in the left subtree.

This allows us to instantly calculate the size of one of the two subtrees and only recursively explore the other one, which is much faster than exploring both.

## Solution Approach

This solution implements the recursive, divide-and-conquer strategy.

```python
class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        # Helper to find height by just going left. This is fast (O(log n)).
        def get_height(node):
            height = 0
            while node:
                height += 1
                node = node.left
            return height

        left_height = get_height(root.left)
        right_height = get_height(root.right)

        if left_height == right_height:
            # The left subtree is a perfect binary tree.
            # Total nodes = (1 for root) + (2^h - 1 for left subtree) + (nodes in right subtree)
            # This simplifies to 2^h + countNodes(right subtree).
            # (1 << left_height) is a fast way to calculate 2^left_height.
            return (1 << left_height) + self.countNodes(root.right)
        else:
            # The right subtree is a perfect binary tree.
            # Total nodes = (1 for root) + (nodes in left subtree) + (2^h - 1 for right subtree)
            # This simplifies to countNodes(left subtree) + 2^h.
            return (1 << right_height) + self.countNodes(root.left)
```

**Strategy:**

1.  **Base Case**: An empty tree has 0 nodes.
2.  **Calculate Heights**: For the current `root`, calculate the left-biased heights of its left and right children.
3.  **Compare and Conquer**: Based on the comparison of the heights, determine which subtree is perfect, calculate its size using the `2^h` formula, and recursively call the function on the other, non-perfect subtree.

## Detailed Code Analysis

### `get_height(node)` Helper Function

```python
def get_height(node):
    height = 0
    while node:
        height += 1
        node = node.left
    return height
```

  - This function is an `O(h)` or `O(log n)` operation. It efficiently finds the height of a complete subtree by traversing only its leftmost edge.

### The Main Logic

```python
left_height = get_height(root.left)
right_height = get_height(root.right)

if left_height == right_height:
    return (1 << left_height) + self.countNodes(root.right)
else:
    return (1 << right_height) + self.countNodes(root.left)
```

  - This is the core of the algorithm. It compares the two heights.
  - `1 << h` is a fast, bitwise operation to calculate `2^h`.
  - If `left_height == right_height`, we know the count of the entire left side is `2^left_height` (1 for the root of the subtree + `2^left_height - 1` for a perfect tree). We then only need to recursively count the right side.
  - If they are not equal, the roles are reversed.

## Step-by-Step Execution Trace

### Example: `root = [1,2,3,4,5,6]`

```
      1
     / \
    2   3
   / \ /
  4  5 6
```

1.  **`countNodes(1)` is called:**

      * Find height of left subtree (rooted at `2`): Path `2->4`. `left_height = 2`.
      * Find height of right subtree (rooted at `3`): Path `3->6`. `right_height = 2`.
      * **Heights are equal (2 == 2)**. This means the left subtree (rooted at `2`) is a perfect tree.
      * Its size can be calculated instantly: `2^2 = 4` nodes. Wait, the formula is `1 (root) + (2^h-1)`. The number of nodes in a perfect tree of height `h` is `2^h - 1`. Total nodes including the current root is `1 + (2^lh - 1) + countNodes(right)` -\> `(1 << lh) + countNodes(right)`. The number of nodes in the left subtree is `2^2 - 1 = 3`. The total count is `1 (root) + 3 (left subtree) + countNodes(right) = 4 + countNodes(3)`.
      * Returns `(1 << 2) + countNodes(3)` which is `4 + countNodes(3)`.

2.  **`countNodes(3)` is called:**

      * Find height of left subtree (rooted at `6`): `left_height = 1`.
      * Find height of right subtree (rooted at `None`): `right_height = 0`.
      * **Heights are not equal (1 \!= 0)**. This means the right subtree (rooted at `None`) is perfect.
      * Returns `(1 << right_height) + countNodes(3.left)` which is `(1 << 0) + countNodes(6)` or `1 + countNodes(6)`.

3.  **`countNodes(6)` is called:**

      * It's a leaf. Its left and right children are `None`.
      * `left_height = 0`, `right_height = 0`.
      * **Heights are equal**.
      * Returns `(1 << 0) + countNodes(None)` which is `1 + 0 = 1`.

4.  **Results Propagate Back:**

      * `countNodes(3)` returns `1 + 1 = 2`.
      * `countNodes(1)` returns `4 + 2 = 6`.

The final answer is **6**.

## Performance Analysis

### Time Complexity: O((log n)²)

  - The algorithm traverses the height of the tree, which is `O(log n)`. At each node it visits, it calls the `get_height` function, which also takes `O(log n)` time. This results in a total complexity of `O(log n * log n)`.

### Space Complexity: O(log n)

  - The space is determined by the recursion depth, which is the height of the tree, `h`, or `O(log n)`.

## Alternative Approaches Comparison

### Approach 1: Divide and Conquer (Our Solution)

  - ✅ **Time: O((log n)²)**, **Space: O(log n)**.
  - ✅ Meets the "faster than O(n)" requirement.
  - ✅ A very clever use of the properties of a complete tree.

### Approach 2: Simple Traversal (DFS or BFS)

  - ❌ **Time: O(n)**, **Space: O(n)**.
  - ❌ Does not meet the time complexity requirement of the problem.
  - ✅ Simpler to write.

## Key Learning Points

  - How to leverage the specific properties of a data structure (like a complete tree) for a more efficient algorithm.
  - The "divide and conquer" recursive pattern where you can solve one subproblem instantly with a formula and only recurse on the other.
  - The use of bitwise shifts (`1 << h`) as a fast way to compute powers of 2.