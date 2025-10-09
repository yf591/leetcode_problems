# 106\. Construct Binary Tree from Inorder and Postorder Traversal - Solution Explanation

## Problem Overview

You are given two integer arrays: `inorder` and `postorder`. These represent the inorder and postorder traversals of the same binary tree. Your task is to **reconstruct the original binary tree** from these two traversals.

**Traversal Definitions:**

  - **Inorder Traversal**: Visits nodes in the order: **Left Subtree -\> Root -\> Right Subtree**.
  - **Postorder Traversal**: Visits nodes in the order: **Left Subtree -\> Right Subtree -\> Root**.

**Example:**

```python
Input: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
Output: The root of the tree [3,9,20,null,null,15,7]

# Tree Structure:
#      3
#     / \
#    9   20
#       /  \
#      15   7
```

## Key Insights

This problem seems complex, but it can be solved elegantly with recursion by understanding the unique information each traversal provides.

### 1\. The Power of Postorder: Finding the Root

The most important property of a **postorder** traversal (`Left -> Right -> Root`) is that the **very last element** is *always* the **root** of the tree (or subtree).

  - In `[9,15,7,20,3]`, the last element `3` is the root of the entire tree.
  - This gives us a starting point for building our tree, from the top down.

### 2\. The Power of Inorder: Finding the Structure

Once we know the root's value (from the postorder list), we can find that same value in the **inorder** list (`Left -> Root -> Right`).

  - In `[9,3,15,20,7]`, the root `3` is at index 1.
  - This tells us everything to the **left** of `3` in the inorder list (`[9]`) belongs to the root's **left subtree**.
  - Everything to the **right** of `3` (`[15,20,7]`) belongs to the root's **right subtree**.

### 3\. The Recursive "Divide and Conquer" Strategy

By combining these two insights, we can define a recursive algorithm:

1.  Find the root of the current tree (it's the last element of the current postorder segment).
2.  Create a `TreeNode` for this root.
3.  Find the root in the inorder list to partition it into left and right sub-arrays.
4.  Use these partitions to also figure out which parts of the postorder array correspond to the left and right subtrees.
5.  Recursively call our function to build the left and right subtrees.

### 4\. The Critical Twist: **Build the Right Subtree First\!**

This is the most important detail that differs from the preorder/inorder version.

  - A postorder array is structured like `[...left_subtree_nodes..., ...right_subtree_nodes..., root]`.
  - We will process this array from the **end backwards**. After we've processed the `root`, the element we see next (at `index - 1`) is the root of the **right subtree**.
  - Therefore, our recursive calls must build the **right subtree first**, then the left subtree.

## Solution Approach

This solution implements the recursive, "divide and conquer" strategy. To make it efficient, we first convert the `inorder` list into a hash map for O(1) lookups of any node's index. A single pointer, `postorder_index`, is used to keep track of the current root in the `postorder` array, moving from right to left.

```python
from typing import List, Optional

class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        # Step 1: Create a hash map for O(1) lookups of inorder indices.
        inorder_map = {val: i for i, val in enumerate(inorder)}
        
        # This pointer tracks the current root in the postorder list, starting from the end.
        self.postorder_index = len(postorder) - 1
        
        def build_helper(in_left_idx, in_right_idx):
            # Base case: If there are no elements for this subtree.
            if in_left_idx > in_right_idx:
                return None
            
            # The current root is the value at postorder_index.
            root_val = postorder[self.postorder_index]
            self.postorder_index -= 1 # Move to the next root.
            
            root = TreeNode(root_val)
            
            # Partition the inorder array to find the boundaries of the subtrees.
            inorder_root_idx = inorder_map[root_val]
            
            # --- CRITICAL STEP: Build the RIGHT subtree first ---
            root.right = build_helper(inorder_root_idx + 1, in_right_idx)
            
            # Then, build the left subtree.
            root.left = build_helper(in_left_idx, inorder_root_idx - 1)
            
            return root

        # Start the recursive construction with the entire range of the inorder list.
        return build_helper(0, len(inorder) - 1)
```

## Detailed Code Analysis

### Step 1: The `inorder_map`

```python
inorder_map = {val: i for i, val in enumerate(inorder)}
```

  - This is a crucial optimization. Instead of searching the `inorder` list (`O(n)`) every time we need to find a root's position, we pre-process it into a hash map (`{value: index}`). This makes lookups `O(1)`, turning our overall algorithm from `O(n²)` to `O(n)`.

### Step 2: The `postorder_index`

```python
self.postorder_index = len(postorder) - 1
```

  - This pointer tells us which element in the `postorder` array is the root of the current subtree we are trying to build. We initialize it to the last index, which is the root of the entire tree. We will decrement this pointer each time we "use up" a root.

### Step 3: The `build_helper` Recursive Function

This is the core of the algorithm. It is responsible for building a tree or subtree given a specific portion of the `inorder` list, defined by `in_left_idx` and `in_right_idx`.

**The Base Case:**

```python
if in_left_idx > in_right_idx:
    return None
```

  - This is our stopping condition. If the left boundary pointer is greater than the right, it means the segment of the `inorder` array for this subtree is empty, so we return `None`.

**Finding and Creating the Root:**

```python
root_val = postorder[self.postorder_index]
self.postorder_index -= 1
root = TreeNode(root_val)
```

  - We get the current root's value from the `postorder` array.
  - We immediately decrement `self.postorder_index`. This is key: the next value we read from the end of `postorder` will be the root of the *next* subtree we build (which will be the right one).

**The Recursive Calls (RIGHT FIRST):**

```python
inorder_root_idx = inorder_map[root_val]
root.right = build_helper(inorder_root_idx + 1, in_right_idx)
root.left = build_helper(in_left_idx, inorder_root_idx - 1)
```

  - We use our map to find the root's index in the `inorder` list in `O(1)` time.
  - **`root.right = build_helper(inorder_root_idx + 1, in_right_idx)`**: This is the most important line. We make the recursive call to build the right subtree **first**. The `inorder` elements for the right subtree are from the index just after the root to the right boundary.
  - **`root.left = build_helper(in_left_idx, inorder_root_idx - 1)`**: After the entire right subtree has been built (and the `postorder_index` has been moved accordingly), we then build the left subtree.

## Step-by-Step Execution Trace

Let's trace `inorder = [9,3,15,20,7]`, `postorder = [9,15,7,20,3]`.

### **Initial State:**

  - `inorder_map` = `{9:0, 3:1, 15:2, 20:3, 7:4}`
  - `postorder_index` = `4`
  - Initial call: `build_helper(in_left=0, in_right=4)`

<!-- end list -->

1.  **`build_helper(0, 4)`:**

      - `postorder_index` is 4. `root_val` = `postorder[4]` = **3**. `postorder_index` becomes 3.
      - Create `root = TreeNode(3)`.
      - `inorder_root_idx` = `inorder_map[3]` = **1**.
      - **Call `root.right = build_helper(2, 4)`** (for inorder `[15,20,7]`).

2.  **`build_helper(2, 4)`:**

      - `postorder_index` is 3. `root_val` = `postorder[3]` = **20**. `postorder_index` becomes 2.
      - Create `root = TreeNode(20)`.
      - `inorder_root_idx` = `inorder_map[20]` = **3**.
      - **Call `root.right = build_helper(4, 4)`** (for inorder `[7]`).

3.  **`build_helper(4, 4)`:**

      - `postorder_index` is 2. `root_val` = `postorder[2]` = **7**. `postorder_index` becomes 1.
      - Create `root = TreeNode(7)`.
      - `inorder_root_idx` = `inorder_map[7]` = **4**.
      - Call `root.right = build_helper(5, 4)`. Base case hit, returns `None`.
      - Call `root.left = build_helper(4, 3)`. Base case hit, returns `None`.
      - **Returns `TreeNode(7)`**.

4.  Back at `build_helper(2, 4)` (`root=20`):

      - `root.right` is now `TreeNode(7)`.
      - **Call `root.left = build_helper(2, 2)`** (for inorder `[15]`).

5.  **`build_helper(2, 2)`:**

      - `postorder_index` is 1. `root_val` = `postorder[1]` = **15**. `postorder_index` becomes 0.
      - Create `root = TreeNode(15)`.
      - `inorder_root_idx` = `inorder_map[15]` = **2**.
      - Calls for left/right children hit the base case and return `None`.
      - **Returns `TreeNode(15)`**.

6.  Back at `build_helper(2, 4)` (`root=20`):

      - `root.left` is now `TreeNode(15)`.
      - The node `20` is fully built (`15 <- 20 -> 7`).
      - **Returns `TreeNode(20)`**.

7.  Back at the top-level `build_helper(0, 4)` (`root=3`):

      - `root.right` is now the `TreeNode(20)` subtree we just built.
      - **Call `root.left = build_helper(0, 0)`** (for inorder `[9]`).

8.  **`build_helper(0, 0)`:**

      - `postorder_index` is 0. `root_val` = `postorder[0]` = **9**. `postorder_index` becomes -1.
      - Create `root = TreeNode(9)`.
      - It's a leaf, so its children will be `None`.
      - **Returns `TreeNode(9)`**.

9.  Back at the top-level `build_helper(0, 4)` (`root=3`):

      - `root.left` is now `TreeNode(9)`.
      - The entire tree is now built.
      - **Returns the final `TreeNode(3)`**.

## Performance Analysis

### Time Complexity: O(n)

  - Building the `inorder_map` takes `O(n)` time.
  - The recursive `build_helper` function is called exactly once for each node in the tree. The work done inside each call is `O(1)` (thanks to the hash map). Therefore, the traversal part is also `O(n)`.

### Space Complexity: O(n)

  - The `inorder_map` requires `O(n)` space.
  - The recursion call stack requires space proportional to the height of the tree, `h`. In the worst case (a skewed tree), this is `O(n)`. In a balanced tree, it's `O(log n)`. The overall space is dominated by `O(n)`.