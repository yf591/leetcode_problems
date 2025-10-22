# 450\. Delete Node in a BST - Solution Explanation

## Problem Overview

You are given the `root` of a **Binary Search Tree (BST)** and an integer `key`. The task is to delete the node containing the `key` (if it exists) from the BST. Crucially, the tree must **remain a valid BST** after the deletion. You should return the `root` of the (potentially modified) BST.

**BST Property Reminder:**
For any node:

  - All values in its left subtree are strictly less than the node's value.
  - All values in its right subtree are strictly greater than the node's value.
  - Both subtrees are also BSTs.

**The Process:**
The problem breaks down into two main stages:

1.  **Search**: Find the node with the value equal to `key`.
2.  **Delete**: If found, remove the node while preserving the BST structure.

**Examples:**

```python
Input: root = [5,3,6,2,4,null,7], key = 3
Output: [5,4,6,2,null,null,7] # or [5,2,6,null,4,null,7]
Explanation: Node 3 is found and removed. The BST structure is maintained by promoting a child or successor.

Input: root = [5,3,6,2,4,null,7], key = 0
Output: [5,3,6,2,4,null,7]
Explanation: Key 0 is not found, so the tree remains unchanged.
```

## Key Insights

### 1\. Searching in a BST

Because it's a BST, searching for the `key` is efficient. We can use the core BST property:

  - If `key < current_node.val`, the key must be in the left subtree.
  - If `key > current_node.val`, the key must be in the right subtree.
  - If `key == current_node.val`, we've found the node to delete.
    This naturally leads to a recursive search approach.

### 2\. The Complexity of Deletion

Deleting a node is straightforward if it's a leaf or has only one child. The real complexity arises when the node to be deleted has **two children**. Simply removing it would break the tree into three parts (the parent, the left subtree, and the right subtree). We need a way to reconnect these parts while maintaining the BST order.

### 3\. Handling the Deletion Cases

There are three distinct cases when we find the node (`node_to_delete`) with `node_to_delete.val == key`:

  * **Case 1: No Children (Leaf Node)**

      - This is the simplest case. We can just remove the node by returning `None` to its parent (the parent's `left` or `right` pointer will be set to `None`).

  * **Case 2: One Child (Left or Right)**

      - We can "replace" the node to be deleted with its single child. We do this by returning the child node to the parent (the parent's `left` or `right` pointer will be set to point to the child).

  * **Case 3: Two Children**

      - This is the most complex. We need to find a node to replace `node_to_delete` that preserves the BST order. There are two standard choices:
        1.  The **In-order Successor**: The smallest node in the node's *right* subtree.
        2.  The **In-order Predecessor**: The largest node in the node's *left* subtree.
      - Let's choose the **in-order successor**. Find this successor node (let's call it `successor`).
      - Copy the `successor`'s value into the `node_to_delete`.
      - Now, the original problem transforms into a simpler one: **delete the `successor` node** from the *right subtree*. Since the successor is the smallest in its subtree, it cannot have a left child, guaranteeing that its deletion will fall into Case 1 or Case 2.

### 4\. Recursion for Structure Modification

Recursion is particularly well-suited for BST operations. A recursive function `deleteNode(node, key)` can perform the search. Crucially, it should **return the root of the modified subtree**. This allows the parent node to update its `left` or `right` pointer correctly:
`node.left = deleteNode(node.left, key)`
`node.right = deleteNode(node.right, key)`

## Solution Approach

This solution uses recursion. The `deleteNode` function searches for the `key`. When found, it handles the three deletion cases. For the two-child case, it finds the minimum value in the right subtree (the successor), replaces the current node's value with it, and then recursively calls `deleteNode` again to remove the successor from the right subtree.

```python
from typing import Optional

class Solution:
    def findMin(self, node: TreeNode) -> TreeNode:
        """Helper function: Find the node with the minimum value in a BST subtree."""
        current = node
        # The minimum value is always the leftmost node.
        while current and current.left:
            current = current.left
        return current

    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        # --- Base Case for Recursion ---
        if not root:
            return None # Key not found, or subtree is empty

        # --- Recursive Search Phase ---
        if key < root.val:
            # Key is smaller, so it must be in the left subtree.
            # Recursively call deleteNode on the left child. The result of the call
            # (which might be the modified left child or None) becomes the new root.left.
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            # Key is larger, so it must be in the right subtree.
            root.right = self.deleteNode(root.right, key)
        
        # --- Deletion Phase (key == root.val) ---
        else: 
            # Found the node to delete! Now handle the 3 cases.
            
            # Case 1 & 2: Node has 0 or 1 child (Right child only, or No children)
            if not root.left:
                # Replace this node with its right child. If right child is also None,
                # this correctly returns None, deleting a leaf.
                temp = root.right
                root = None # Help garbage collection (optional in Python)
                return temp
            
            # Case 2: Node has 1 child (Left child only)
            elif not root.right:
                # Replace this node with its left child.
                temp = root.left
                root = None # Help garbage collection (optional in Python)
                return temp
                
            # Case 3: Node has two children.
            else:
                # Find the in-order successor (smallest node in the right subtree).
                successor_node = self.findMin(root.right)
                
                # Copy the successor's value to this node.
                root.val = successor_node.val
                
                # Now, recursively delete the successor node from the right subtree.
                # The successor's value (which we just copied into root.val) is the key to delete.
                root.right = self.deleteNode(root.right, successor_node.val) 
                
        # Return the (possibly updated) root of the current subtree.
        return root
```

## Detailed Code Analysis

### Base Case

```python
if not root:
    return None
```

  - This is the fundamental stopping condition for the recursion. If we reach an empty spot (`None`) while searching, it means the `key` is not in this branch (or the initial tree was empty). We return `None` up the call stack.

### Recursive Search

```python
if key < root.val:
    root.left = self.deleteNode(root.left, key)
elif key > root.val:
    root.right = self.deleteNode(root.right, key)
```

  - This implements the standard BST search.
  - The crucial part is `root.left = ...` and `root.right = ...`. The recursive call `self.deleteNode(...)` will return the root of the *modified* subtree (or `None` if the node was deleted). By assigning this return value back to `root.left` or `root.right`, we correctly update the parent's pointer to reflect any changes made deeper in the tree.

### Deletion Logic (`else: key == root.val`)

**Cases 1 & 2 (0 or 1 Child):**

```python
if not root.left: return root.right
elif not root.right: return root.left
```

  - These two checks handle the simple cases efficiently.
  - If `root.left` is `None`, it means there's either only a right child or no children. We return `root.right`. If `root.right` was also `None`, this correctly returns `None` (deleting a leaf). If `root.right` existed, it returns the right child, effectively replacing the `root` with it.
  - The `elif` handles the case where there's only a left child.

**Case 3 (Two Children):**

```python
successor_node = self.findMin(root.right)
root.val = successor_node.val
root.right = self.deleteNode(root.right, successor_node.val)
```

  - `successor_node = self.findMin(root.right)`: We call a helper function (`findMin`) to find the smallest node in the *right* subtree. This node is the in-order successor.
  - `root.val = successor_node.val`: We replace the value of the node we want to "delete" with the value of its successor. Now, the original value `key` is gone, but we have a duplicate of the successor's value in the tree.
  - `root.right = self.deleteNode(root.right, successor_node.val)`: This is the clever part. We now make a recursive call to `deleteNode`, but this time the goal is to remove the *original successor node* (which is guaranteed to have 0 or 1 child) from the *right subtree*. The `key` we pass is the `successor_node.val` (which is now also in `root.val`). The result of this deletion is correctly assigned back to `root.right`.

### `findMin` Helper

```python
def findMin(self, node: TreeNode) -> TreeNode:
    current = node
    while current and current.left:
        current = current.left
    return current
```

  - This function simply iterates down the leftmost path from the given `node` to find the smallest value in that subtree.

## Step-by-Step Execution Trace

Let's trace `deleteNode(root=[5,3,6,2,4,null,7], key=3)`.

1.  **`deleteNode(Node(5), 3)`**: `key < root.val`. Calls `deleteNode(Node(3), 3)` and sets `Node(5).left` to its result.
2.  **`deleteNode(Node(3), 3)`**: `key == root.val`. Found the node to delete\!
      - Does it have a left child? Yes (`Node(2)`).
      - Does it have a right child? Yes (`Node(4)`). -\> **Case 3 (Two Children)**.
      - Call `findMin(Node(3).right)` which is `findMin(Node(4))`.
          - `findMin` goes left from `Node(4)`. There's no left child.
          - `findMin` returns `Node(4)`. So, `successor_node = Node(4)`.
      - Copy successor's value: `Node(3).val` becomes `4`. (The node we are currently at *is still* the `Node(3)` object, but its value is now `4`).
      - Recursively delete the successor from the right subtree: Call `deleteNode(Node(4), 4)` and set `Node(3).right` (which is still pointing to the original `Node(4)`) to its result.
3.  **`deleteNode(Node(4), 4)`**: `key == root.val`. Found the node to delete\!
      - Does it have a left child? No.
      - `if not root.left:` is true.
      - It returns `root.right`, which is `None`.
4.  Back at **`deleteNode(Node(3), 3)`** (which now has `val=4`):
      - The call to delete the successor returned `None`.
      - `root.right` (which was `Node(4)`) is set to `None`.
      - The function returns `root` (the node that originally held 3 but now holds 4).
5.  Back at the top-level **`deleteNode(Node(5), 3)`**:
      - The call on the left child returned the modified node (value 4, left child 2, right child None).
      - `Node(5).left` is updated to point to this modified node.
      - The function returns the original `root` (`Node(5)`).

The final tree structure corresponds to `[5, 4, 6, 2, null, null, 7]`.

## Performance Analysis

### Time Complexity: O(h)

  - Where `h` is the height of the tree. In each step, we either go down one level (in the search phase) or, in the two-child deletion case, we find the successor (`O(h)`) and make one recursive call (`O(h)`).
  - **Best/Average Case (Balanced Tree)**: `h = log n`. Complexity is **`O(log n)`**.
  - **Worst Case (Skewed Tree)**: `h = n`. Complexity is **`O(n)`**.

### Space Complexity: O(h)

  - The space complexity is determined by the depth of the recursion call stack, which is equal to the height of the tree, `h`.
  - **Worst Case**: `O(n)`. **Best Case**: `O(log n)`.