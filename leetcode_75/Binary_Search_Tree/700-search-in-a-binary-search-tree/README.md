# 700\. Search in a Binary Search Tree - Solution Explanation

## Problem Overview

You are given the `root` of a **Binary Search Tree (BST)** and an integer `val`. Your task is to find the node in the BST whose value is equal to `val`.

**Output:**

  - If the node is found, return the node itself (which includes the entire subtree rooted at that node).
  - If no such node exists, return `null` (or `None` in Python).

**Examples:**
```
      50
     / \
    40  70
   /    / 
  30   60

Binary Search Tree (BST) Data Structure
```

```python
Input: root = [4,2,7,1,3], val = 2
Output: [2,1,3] # The subtree rooted at node 2

Input: root = [4,2,7,1,3], val = 5
Output: [] # An empty list represents null/None
```

## Key Insights

### The Power of the BST Property

The most important piece of information in this problem is that the tree is a **Binary Search Tree (BST)**. This is not just any binary tree; it has a special, strict ordering rule:

> For any given node, all values in its **left** subtree are **smaller** than the node's own value, and all values in its **right** subtree are **larger**.

This property is the key to an efficient solution. It means we don't have to search the entire tree. At every node, we can make an intelligent decision to **eliminate half of the remaining search space**. This is the exact same principle as a binary search on a sorted array.

## Solution Approach

The solution uses an iterative approach to traverse the tree. We start at the root and, at each step, decide whether to go left, go right, or stop because we've found our value. This avoids the overhead of recursion and uses constant extra space.

```python
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        # Start our search pointer at the root of the tree.
        current_node = root
        
        # Loop as long as we are on a valid, existing node.
        while current_node:
            # Case 1: We found the value.
            if val == current_node.val:
                return current_node
            
            # Case 2: The target value is smaller, so it must be in the left subtree.
            elif val < current_node.val:
                current_node = current_node.left
            
            # Case 3: The target value is larger, so it must be in the right subtree.
            else: # val > current_node.val
                current_node = current_node.right
                
        # If the loop finishes, it means we reached a null pointer (fell off the tree),
        # so the value does not exist.
        return None
```

**Strategy:**

1.  **Initialize**: Create a pointer `current_node` that starts at the `root`.
2.  **Loop**: Continue searching as long as `current_node` is not `None`.
3.  **Compare**: In each step, compare the target `val` with `current_node.val`.
4.  **Decide**:
      - If equal, return the `current_node`.
      - If `val` is smaller, move left: `current_node = current_node.left`.
      - If `val` is larger, move right: `current_node = current_node.right`.
5.  **Not Found**: If the loop terminates, the value wasn't in the tree. Return `None`.

## Detailed Code Analysis

### Step 1: Initialization

```python
current_node = root
```

- We create a single variable, `current_node`, to keep track of our position in the tree. It starts at the very top.

### Step 2: The Loop Condition

```python
while current_node:
```

- This is shorthand for `while current_node is not None:`. The loop will continue as long as our pointer is pointing to an actual node. If we ever try to move to a child that doesn't exist (e.g., the left child of a leaf node), `current_node` will become `None`, and the loop will terminate.

### Step 3: The Three-Way Comparison

```python
if val == current_node.val:
    return current_node
elif val < current_node.val:
    current_node = current_node.left
else: # val > current_node.val
    current_node = current_node.right
```

- This `if/elif/else` block is the heart of the search. At every node, it makes one of three decisions:
    1.  **Found it\!** (`val == current_node.val`): The search is over. We return the node we are currently on.
    2.  **Go Left** (`val < current_node.val`): We know the value must be on the left side, so we update our `current_node` pointer to point to its left child.
    3.  **Go Right** (`val > current_node.val`): We know the value must be on the right side, so we update our `current_node` pointer to point to its right child.

## Step-by-Step Execution Trace

### Example 1 (Success): `root = [4,2,7,1,3]`, `val = 2`

**Tree Structure:**

```
      4
     / \
    2   7
   / \
  1   3
```

| Step | `current_node` | `val` vs `current_node.val` | Decision |
| :--- | :--- | :--- | :--- |
| **Start** | Node(4) | `2 < 4` | Go Left. `current_node` becomes `Node(2)`. |
| **1** | Node(2) | `2 == 2` | Found\! Return `Node(2)`. |

### Example 2 (Failure): `root = [4,2,7,1,3]`, `val = 5`

| Step | `current_node` | `val` vs `current_node.val` | Decision |
| :--- | :--- | :--- | :--- |
| **Start** | Node(4) | `5 > 4` | Go Right. `current_node` becomes `Node(7)`. |
| **1** | Node(7) | `5 < 7` | Go Left. `current_node` becomes `Node(7).left`. |
| **2** | `None` | - | `current_node` is now `None`. The `while` loop terminates. |

  - After the loop, the function returns `None`.

## Performance Analysis

### Time Complexity: O(h)

  - Where `h` is the height of the tree. In each step, we move down one level of the tree.
  - **Best/Average Case (Balanced Tree)**: The height `h` is approximately `log n`, so the complexity is **`O(log n)`**.
  - **Worst Case (Skewed Tree)**: The tree is essentially a linked list. The height `h` is `n`, so the complexity is **`O(n)`**.

### Space Complexity: O(1)

  - The iterative solution uses only one pointer (`current_node`). The space required is constant and does not depend on the size of the tree.

## Alternative Approaches Comparison

### Approach 1: Iteration (Our Solution)

  - ✅ **Space: O(1)**.
  - ✅ Fast and efficient, avoids recursion overhead.

### Approach 2: Recursion

```python
class Solution:
    def searchBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if not root or val == root.val:
            return root
        
        if val < root.val:
            return self.searchBST(root.left, val)
        else:
            return self.searchBST(root.right, val)
```

- ✅ Very elegant and a direct translation of the mathematical definition of the search.
  - ❌ **Space: O(h)**. Uses space on the recursion call stack, which is proportional to the height of the tree.

## Key Learning Points

  - The **BST property** (`left < root < right`) is the single most important concept for all BST-related algorithms.
  - This property allows searching in `O(log n)` average time, which is a massive improvement over the `O(n)` time required for a regular binary tree.
  - Tree traversal problems can often be solved either **iteratively** (with a `while` loop and pointers) or **recursively**.