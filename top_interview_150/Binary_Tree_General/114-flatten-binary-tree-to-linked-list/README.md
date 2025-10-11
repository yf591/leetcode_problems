# 114\. Flatten Binary Tree to Linked List - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree. The task is to "flatten" this tree into a structure that resembles a linked list, **in-place**.

**The "Linked List" Structure:**

  - The flattened structure still uses `TreeNode` objects.
  - Each node's `left` child pointer must be set to `None`.
  - Each node's `right` child pointer acts like a `next` pointer, pointing to the next node in the sequence.

**The Required Order:**

  - The order of the nodes in the final "linked list" must be the same as a **pre-order traversal** (`Root -> Left -> Right`) of the original tree.

**Example:**

  - **Input Tree:**
    ```
          1
         / \
        2   5
       / \   \
      3   4   6
    ```
  - **Pre-order Traversal Sequence**: `[1, 2, 3, 4, 5, 6]`
  - **Output (Flattened Tree):**
    ```
    1
     \
      2
       \
        3
         \
          4
           \
            5
             \
              6
    ```

## Key Insights

### 1\. The Simple (but `O(n)` space) Approach

A straightforward way to solve this is to first perform a pre-order traversal and store all the nodes in a list or queue. Then, you can iterate through this list and re-wire the `right` and `left` pointers of each node. This works, but it requires `O(n)` extra space to store the list of nodes, which is not an "in-place" solution.

### 2\. The In-Place Challenge

The real challenge is to perform this re-wiring with `O(1)` extra space (ignoring the recursion stack). A direct pre-order traversal (`Root -> Left -> Right`) is tricky for in-place modification. If you are at a node, you need to connect its `right` pointer to its left child, but what do you do with its original right child? You would have to find the tail of the flattened left subtree to attach it, which is inefficient.

### 3\. The "Reverse" Insight: Building the List Backwards

This is the core, beautiful insight. The desired order is a pre-order traversal: `Root -> Left -> Right`. What if we think about the traversal in **reverse**?

A **reverse pre-order traversal** would be: **`Right -> Left -> Root`**.

Let's see what happens if we visit the nodes in this reverse order and try to build our linked list:

  - The **last** node we visit in this traversal is the original `root`. This should become the **head** of our final linked list.
  - The **second-to-last** node we visit should become the second node in the list, and its `right` pointer should point to the last node.
  - The **third-to-last** node we visit should become the third node, and its `right` pointer should point to the second-to-last node.

This reveals a powerful pattern: As we traverse the tree in `Right -> Left -> Root` order, each node we process becomes the **new head** of the linked list we have built so far. We can keep track of the head of this "already flattened" portion with a single pointer.

## Solution Approach

This solution uses a recursive Depth-First Search (DFS) that traverses the tree in a reverse pre-order (`Right -> Left -> Root`). It uses a single instance variable, `self.prev`, to keep track of the head of the flattened list as it's being constructed from tail to head.

```python
from typing import Optional

class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        # 'self.prev' will keep track of the previously visited node.
        # As we build the list backwards, this will always be the head
        # of the already-flattened part of the list.
        self.prev = None

        def dfs(node: Optional[TreeNode]):
            # Base Case: If the node is None, we've reached the end of a branch.
            if not node:
                return

            # Step 1: Traverse the Right subtree first.
            dfs(node.right)
            
            # Step 2: Traverse the Left subtree.
            dfs(node.left)

            # Step 3: Now, process the current node (the "Root" part of our traversal).
            # This code runs after the entire right and left subtrees have been flattened.
            
            # Re-wire the pointers:
            node.right = self.prev
            node.left = None
            
            # Update self.prev to be the current node, as it is now the new
            # head of our flattened list.
            self.prev = node

        # Start the recursive process from the root.
        dfs(root)
```

## Detailed Code Analysis

### Step 1: The `self.prev` Pointer

```python
self.prev = None
```

  - We use an instance variable (`self.prev`) so that its state persists across all the recursive calls of our `dfs` helper function.
  - We initialize it to `None`. This is because the very last node in our reverse traversal (which is the original tail of the flattened list) must have its `right` pointer set to `None`.

### Step 2: The `dfs` Helper Function

This is the core of the algorithm.

**The Traversal Order:**

```python
dfs(node.right)
dfs(node.left)
```

  - This is the implementation of our reverse pre-order traversal. By calling `dfs` on the `right` child *before* the `left` child, we ensure that we always visit and process the entire right subtree before we even touch the left subtree.

**The Re-wiring Logic:**

```python
# This code runs AFTER the recursive calls have returned.
node.right = self.prev
node.left = None
self.prev = node
```

  - This block is the "visit the root" part of our `Right -> Left -> Root` traversal. Because it runs after the recursion, it effectively builds the list from the tail backwards to the head.
  - **`node.right = self.prev`**: This is the crucial linking step. It sets the current node's `right` pointer to whatever `self.prev` is currently pointing to (which is the head of the already-flattened list segment).
  - **`node.left = None`**: The problem requires all `left` pointers to be `None`.
  - **`self.prev = node`**: This is the state update. We've just added the `node` to the front of our flattened list, so we update `self.prev` to point to this `node`, making it the new head for the next node we process.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `root = [1, 2, 5, 3, 4, null, 6]` with extreme detail.

**Tree Structure:**

```
      1
     / \
    2   5
   / \   \
  3   4   6
```

The reverse pre-order traversal sequence is `[6, 5, 4, 3, 2, 1]`. The `dfs` function will visit and **process** the nodes in this order as the recursion unwinds.

| `dfs` Call on Node | Action | `self.prev` (after processing) | State of the Node's Pointers |
| :--- | :--- | :--- | :--- |
| **Start** | - | `None` | - |
| **`dfs(6)`** | `6` is the first to be processed. | `Node(6)` | `6.right = None`, `6.left = None` |
| **`dfs(5)`** | `5` is processed next. | `Node(5)` | `5.right = self.prev` (Node 6), `5.left = None` |
| **`dfs(4)`** | `4` is processed next. | `Node(4)` | `4.right = self.prev` (Node 5), `4.left = None` |
| **`dfs(3)`** | `3` is processed next. | `Node(3)` | `3.right = self.prev` (Node 4), `3.left = None` |
| **`dfs(2)`** | `2` is processed next. | `Node(2)` | `2.right = self.prev` (Node 3), `2.left = None` |
| **`dfs(1)`** | `1` is the last to be processed. | `Node(1)` | `1.right = self.prev` (Node 2), `1.left = None` |

**Visualizing the Unwinding:**

1.  The recursion goes all the way down to the deepest, rightmost node: `dfs(6)`.
2.  `dfs(6)` runs. `self.prev` is `None`. It sets `6.right = None`, `6.left = None`. It updates `self.prev` to point to `Node(6)`. It returns.
3.  Control returns to `dfs(5)`. The right side is done. The left side (`None`) is done. Now it processes `Node(5)`.
      - It sets `5.right = self.prev` (which is `Node(6)`). The link `5 -> 6` is made.
      - It sets `5.left = None`.
      - It updates `self.prev` to point to `Node(5)`. It returns.
4.  Control returns to the parent of `5`, and so on... The process continues, with each node linking its `right` pointer to the head of the list built so far (`self.prev`).

After the initial `dfs(root)` call returns, the entire tree has been re-wired in place into the correct pre-order linked list structure.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The DFS algorithm visits every node exactly once.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by the recursion call stack. While the algorithm modifies the tree in-place, the recursion itself requires space.
  - **Worst Case**: `O(n)` for a completely skewed tree.
  - **Best Case**: `O(log n)` for a completely balanced tree.