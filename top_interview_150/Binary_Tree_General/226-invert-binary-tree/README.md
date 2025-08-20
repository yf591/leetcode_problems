# 226\. Invert Binary Tree - Solution Explanation

## Problem Overview

Given the `root` of a binary tree, the task is to invert the tree and return its root.

**Invert Definition:**
Inverting a tree means creating its mirror image. For every node in the tree, its left child becomes its right child, and its right child becomes its left child.

**Examples:**

```python
Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]

Input: root = [2,1,3]
Output: [2,3,1]
```

## Key Insights

### The Recursive Structure

The key insight is that the "inversion" or "swapping" operation is not a one-time action. It must be applied to **every single node** in the tree. The tree as a whole is inverted if and only if the subtrees of its root are also inverted.

When a problem can be broken down into smaller, self-similar subproblems (e.g., "inverting a tree" requires "inverting its subtrees"), this is a perfect indicator that **recursion** is a natural and elegant solution.

## Solution Approach

The solution is a direct translation of the recursive insight. For any given node, we swap its children and then recursively tell its children to do the same.

```python
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # Base Case: If the node is None, there's nothing to invert.
        if not root:
            return None
        
        # Swap the left and right children of the current node.
        root.left, root.right = root.right, root.left
        
        # Recursively call the function on the children to invert their subtrees.
        self.invertTree(root.left)
        self.invertTree(root.right)
        
        # Return the root of the now-inverted tree.
        return root
```

**Strategy:**

1.  **Base Case**: If the current node is `None`, stop the recursion for this path.
2.  **Swap**: For the current node, swap its left and right child pointers.
3.  **Recurse**: Call the `invertTree` function on both of the (newly positioned) children.
4.  **Return**: Return the root node.

-----

## Detailed Code Analysis

### Step 1: The Base Case

```python
if not root:
    return None
```

  - This is the stopping condition. Without it, the function would try to access children of `None` nodes, leading to an error and infinite recursion. It correctly defines that inverting "nothing" results in "nothing."

### Step 2: The Swap

```python
root.left, root.right = root.right, root.left
```

  - This is a concise, Pythonic way to swap two variables. It simultaneously assigns the value of `root.right` to `root.left` and the original value of `root.left` to `root.right`.

### Step 3: The Recursive Calls

```python
self.invertTree(root.left)
self.invertTree(root.right)
```

  - This is where the magic happens. After swapping the immediate children, we delegate the task of inverting the rest of the tree to the children themselves. The process repeats, moving down the tree until it hits the base cases at the leaves.

-----

## Step-by-Step Execution Trace

Let's visualize how the recursion works on the input `[4,2,7,1,3,6,9]`. Because the swap happens *before* the recursive calls (this is a "pre-order" traversal), the tree is changed from the **top down**.

**Original Tree:**

```
      4
     / \
    2   7
   / \ / \
  1  3 6  9
```

**1. Call `invertTree(node=4)`:**

  * The direct children of node 4 (`2` and `7`) are swapped.
  * The tree immediately becomes:
    ```
          4
         / \
        7   2  <-- Swapped
       / \ / \
      6  9 1  3 <-- Still attached to original parents
    ```
  * Now, the function makes two recursive calls: `invertTree(node=7)` and then `invertTree(node=2)`.

**2. Call `invertTree(node=7)`:**

  * The children of node 7 (`6` and `9`) are swapped.
  * Its subtree is now inverted:
    ```
        7
       / \
      9   6 <-- Swapped
    ```
  * Recursive calls are then made on the leaves (`9` and `6`), which have no children, so those calls do nothing and return. This branch of the recursion is complete.

**3. Call `invertTree(node=2)`:**

  * The children of node 2 (`1` and `3`) are swapped.
  * Its subtree is now inverted:
    ```
        2
       / \
      3   1 <-- Swapped
    ```
  * Recursive calls are made on the leaves (`3` and `1`), which also do nothing and return. This branch is complete.

**4. Final Result:**

  * After all the recursive calls have finished, the final tree structure is fully inverted:
    ```
          4
         / \
        7   2
       / \ / \
      9  6 3  1
    ```

-----

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The algorithm must visit every node exactly once to perform the swap.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by the recursion call stack.
  - **Worst Case**: `O(n)` for a completely skewed tree.
  - **Best Case**: `O(log n)` for a completely balanced tree.

-----

## Alternative Approaches Comparison

### Approach 1: Recursion (DFS - Our Solution)

  - ✅ Elegant, highly readable, and directly reflects the problem's recursive nature.

### Approach 2: Iteration (BFS)

  - Uses a `queue` to process the tree level by level.
  - ✅ Avoids recursion limits and potential stack overflow on extremely deep trees.
  - ❌ The code is slightly less intuitive than the recursive version.

-----

## Key Learning Points

  - Many tree manipulation problems have simple and elegant recursive solutions.
  - The "divide and conquer" strategy is central to recursion: solve the problem for the current node, then let recursion handle the subproblems.
  - Understanding the call stack is key to visualizing how recursion works.

-----

## Real-World Applications

  - **Computer Graphics**: Flipping or mirroring a hierarchical 2D or 3D model.
  - **Algorithmic Problems**: Used as a subroutine in other tree algorithms, for example, to compare a tree with its mirror image.
  - **Data Structures**: Creating a mirrored copy of a hierarchical data structure for specific search or comparison needs.