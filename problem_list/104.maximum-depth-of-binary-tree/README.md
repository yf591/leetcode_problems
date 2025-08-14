# 104\. Maximum Depth of Binary Tree - Solution Explanation

## Problem Overview

Given the `root` of a binary tree, find its **maximum depth**.

**Maximum Depth Definition:**
The number of nodes along the longest path from the root node down to the farthest leaf node.

**Examples:**

```python
Input: root = [3,9,20,null,null,15,7]
Output: 3

Input: root = [1,null,2]
Output: 2
```

## Key Insights

### The Recursive Nature of Tree Depth

The key insight is that this problem has a natural recursive structure. The depth of any tree (or subtree) is defined by the depth of its children.

  * The depth of an empty tree is 0.
  * The depth of a non-empty tree is **1 (for the root itself) + the depth of its deepest child subtree**.

This leads to the formula: `Depth(node) = 1 + max(Depth(node.left), Depth(node.right))`

## Solution Approach

Our solution is a direct translation of the recursive formula.

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # Base case: an empty tree has a depth of 0
        if not root:
            return 0
        
        # Recursively find the depth of the left and right subtrees
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        
        # The depth is 1 + the max of the subtrees
        return 1 + max(left_depth, right_depth)
```

**Strategy:**

1.  **Base Case**: Handle an empty tree, which has a depth of 0. This is our stopping condition.
2.  **Recursive Calls**: For a given node, call the function on its left and right children to find their respective depths.
3.  **Combine Results**: Combine the results by taking the maximum of the two children's depths and adding 1 for the current node.

## Detailed Code Analysis

### Step 1: Base Case

```python
if not root:
    return 0
```

  - This is the most critical part of the recursion. If we encounter a `None` node (the child of a leaf), we've reached the end of a path. Its contribution to the depth is 0.

### Step 2: Recursive Calls

```python
left_depth = self.maxDepth(root.left)
right_depth = self.maxDepth(root.right)
```

  - The function calls itself to solve the same problem for the smaller left and right subtrees. This process continues until it hits the base case.

### Step 3: Combining the Results

```python
return 1 + max(left_depth, right_depth)
```

  - Once the depths of the left and right subtrees are returned, this line executes. It takes the larger of the two depths, adds 1 (to count the current node), and returns the result up the call stack.

## Step-by-Step Execution Trace

### Example: `root = [3, 9, 20, null, null, 15, 7]`

The calls unfold like this:

```
maxDepth(3)
  -> left_depth = maxDepth(9)
    -> left_depth = maxDepth(None) -> returns 0
    -> right_depth = maxDepth(None) -> returns 0
    -> returns 1 + max(0, 0) = 1
  -> right_depth = maxDepth(20)
    -> left_depth = maxDepth(15)
      -> returns 1 + max(0, 0) = 1
    -> right_depth = maxDepth(7)
      -> returns 1 + max(0, 0) = 1
    -> returns 1 + max(1, 1) = 2
  -> returns 1 + max(1, 2) = 3
```

The final result is `3`.

## Edge Cases Analysis

### Case 1: Empty Tree

```python
root = None
# The base case 'if not root:' is triggered immediately.
# Output: 0
```

### Case 2: Single Node Tree

```python
root = [1]
# The function calls maxDepth on its left (None) and right (None) children.
# Both calls return 0. The final result is 1 + max(0, 0) = 1.
# Output: 1
```

### Case 3: Skewed Tree

```python
root = [1, null, 2]
# The depth of the left subtree is 0.
# The depth of the right subtree is 1 (calculated recursively).
# The final result is 1 + max(0, 1) = 2.
# Output: 2
```

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The algorithm must visit every node exactly once.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by the recursion call stack.
  - **Worst Case**: `O(n)` for a completely skewed tree (like a linked list).
  - **Best Case**: `O(log n)` for a completely balanced tree.

## Alternative Approaches Comparison

### Approach 1: Recursion (DFS - Our Solution)

  - ✅ Elegant, concise, and directly mirrors the problem's definition.
  - ✅ Generally the preferred solution in interviews for its clarity.

### Approach 2: Iteration (BFS)

```python
def maxDepth(self, root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    
    depth = 0
    queue = collections.deque([root])
    
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return depth
```

  - ✅ Avoids recursion limits and potential stack overflow on extremely deep trees.
  - ❌ Slightly more complex to write and less intuitive than the recursive definition.

## Why the Base Case Matters

The `if not root: return 0` line is the foundation of the solution.

  - It provides the **stopping condition**. Without it, the function would call itself on `None` children indefinitely, leading to a stack overflow error.
  - It correctly defines the "depth of nothing" as 0, which allows the `1 + ...` logic at the leaf nodes to work correctly.

## Key Learning Points

  - Many tree problems can be solved elegantly with recursion.
  - The properties of a tree (like height/depth) are often defined recursively.
  - Identifying the correct base case is the most critical step in designing a recursive solution.

## Common Pitfalls Avoided

  - Forgetting the base case, causing infinite recursion.
  - Incorrectly adding `1` at the wrong step (e.g., `1 + self.maxDepth(root.left)`), which would count nodes incorrectly.
  - Returning `1` instead of `0` for an empty tree.

## Real-World Applications

  - Calculating the height of any hierarchical data structure (e.g., file system directory trees, XML/JSON documents, organizational charts).
  - Used as a subroutine in tree-balancing algorithms (e.g., AVL trees), where the balance factor is determined by the height of subtrees.
  - Analyzing the worst-case time complexity of tree operations, as many are proportional to the tree's height.