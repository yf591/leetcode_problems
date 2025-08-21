# 101\. Symmetric Tree - Solution Explanation

## Problem Overview

Given the `root` of a binary tree, the task is to check if it's a mirror of itself (i.e., symmetric around its center).

**Symmetry Definition:**
A tree is symmetric if its left subtree is a perfect mirror image of its right subtree.

**Examples:**

```python
# This tree is symmetric
Input: root = [1,2,2,3,4,4,3]
Output: true

# This tree is not symmetric
Input: root = [1,2,2,null,3,null,3]
Output: false
```

## Key Insights

### Recursive Definition of Symmetry

The problem has a natural recursive structure. A tree is symmetric if its root's children are mirror images of each other. This leads to a key question: when are two subtrees, `tree1` and `tree2`, mirror images?

They are mirror images if:

1.  The root nodes of `tree1` and `tree2` have the same value.
2.  The **left** child of `tree1` is a mirror image of the **right** child of `tree2`.
3.  The **right** child of `tree1` is a mirror image of the **left** child of `tree2`.

This "criss-cross" comparison is the core of the algorithm. We can implement this with a recursive helper function that compares two nodes at a time.

## Solution Approach

The solution uses a main function to handle the initial call and a recursive helper function, `isMirror`, to perform the symmetric comparison between two subtrees.

```python
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        return self.isMirror(root.left, root.right)

    def isMirror(self, node1: Optional[TreeNode], node2: Optional[TreeNode]) -> bool:
        # If both nodes are None, they are symmetric.
        if not node1 and not node2:
            return True
        
        # If only one of them is None, they are not.
        if not node1 or not node2:
            return False
            
        # Check if values match and if the subtrees are mirrors.
        return (node1.val == node2.val and
                self.isMirror(node1.left, node2.right) and
                self.isMirror(node1.right, node2.left))
```

**Strategy:**

1.  **Initial Call**: The main `isSymmetric` function calls a helper, `isMirror`, on the root's left and right children.
2.  **Base Cases**: The `isMirror` function first checks for stopping conditions: if both nodes are `None` (symmetric), or if only one is `None` (not symmetric).
3.  **Recursive Check**: If the nodes exist, it checks if their values are equal AND if their children are symmetric in a "criss-cross" fashion.

## Detailed Code Analysis

### `isSymmetric` (Main Function)

```python
if not root:
    return True
return self.isMirror(root.left, root.right)
```

  - This function is the entry point. An empty tree is considered symmetric. Otherwise, it kicks off the recursive comparison on the two main subtrees.

### `isMirror` (Helper Function)

```python
if not node1 and not node2: return True
if not node1 or not node2: return False
```

  - These are the **base cases**. They handle the ends of branches. If both are `None`, that part of the tree is symmetric. If only one is `None`, the structure doesn't match, so it's not symmetric.

<!-- end list -->

```python
return (node1.val == node2.val and
        self.isMirror(node1.left, node2.right) and
        self.isMirror(node1.right, node2.left))
```

  - This is the **recursive step**. It returns `True` only if all three conditions are met:
    1.  The current nodes' values are equal.
    2.  The "outer" children (`node1.left` and `node2.right`) are mirrors of each other.
    3.  The "inner" children (`node1.right` and `node2.left`) are mirrors of each other.

## Step-by-Step Execution Trace

Let's visualize how the recursion works on `root = [1,2,2,3,4,4,3]`.

**Tree Structure:**

```
      1 (Root)
     / \
  2(L)  2(R)
 / \   / \
3(LL)4(LR)4(RL)3(RR)
```

The execution flow looks like a series of questions:

1.  **`isSymmetric(1)` asks:** "Is my left child `2(L)` a mirror of my right child `2(R)`?"

      * Calls `isMirror(2(L), 2(R))`

2.  **`isMirror(2(L), 2(R))` asks:**

      * "Is `2(L).val == 2(R).val`?" -\> `2 == 2`. **Yes**.
      * "Now, is my outer pair, `2(L).left` and `2(R).right`, a mirror?"
          * Calls `isMirror(3(LL), 3(RR))`
      * "And is my inner pair, `2(L).right` and `2(R).left`, a mirror?"
          * Calls `isMirror(4(LR), 4(RL))`

3.  **`isMirror(3(LL), 3(RR))` asks:**

      * "Is `3(LL).val == 3(RR).val`?" -\> `3 == 3`. **Yes**.
      * "Is my outer pair, `3(LL).left` (`None`) and `3(RR).right` (`None`), a mirror?"
          * Calls `isMirror(None, None)`. This hits a base case and returns **`True`**.
      * "Is my inner pair, `3(LL).right` (`None`) and `3(RR).left` (`None`), a mirror?"
          * Calls `isMirror(None, None)`. This also returns **`True`**.
      * Since all checks passed, `isMirror(3(LL), 3(RR))` returns **`True`**.

4.  **`isMirror(4(LR), 4(RL))` asks:**

      * This follows the same logic as the step above and will also return **`True`**.

5.  **Conclusion:**

      * The call to `isMirror(2(L), 2(R))` receives `True` from its first sub-problem and `True` from its second. Since `2==2` was also true, it returns **`True`**.
      * The original `isSymmetric(1)` call receives this `True` value and returns it as the final answer.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. We must visit every node exactly once to check for symmetry.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by the recursion call stack.
  - **Worst Case**: `O(n)` for a completely skewed (unbalanced) tree.
  - **Best Case**: `O(log n)` for a completely balanced tree.

## Why the "Criss-Cross" Check Matters

The core of this problem is the "criss-cross" recursive call:
`isMirror(node1.left, node2.right)` and `isMirror(node1.right, node2.left)`

This is what checks for a **mirror image**. A common mistake is to check `left-to-left` and `right-to-right`, which is the logic for checking if two trees are **identical** (like in the "Same Tree" problem), not if they are symmetric.

## Key Learning Points

  - Recursion is a powerful tool for tree problems where the logic applies to the node and its subtrees.
  - Using a helper function that takes two nodes is a common pattern for comparison problems.
  - Understanding the difference between checking for equality and checking for symmetry is crucial.

## Real-World Applications

  - **Computer Graphics & CAD**: Verifying if a 2D or 3D model is symmetrical before manufacturing or rendering.
  - **Image and Pattern Recognition**: Algorithms can check for symmetrical patterns in visual data.
  - **Chemistry/Biology**: Analyzing the symmetry of molecular structures.