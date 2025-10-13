# 236\. Lowest Common Ancestor of a Binary Tree - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree and two nodes, `p` and `q`, that are guaranteed to be in the tree. The task is to find their **Lowest Common Ancestor (LCA)**.

**LCA Definition:**
The Lowest Common Ancestor is the deepest node in the tree that has both `p` and `q` as descendants. A key part of the definition is that **a node can be a descendant of itself**.

**In Simple Terms:**
Imagine the tree is a family tree. The LCA of two people is their closest shared ancestor. For example:

  - The LCA of you and your sibling is your parent.
  - The LCA of you and your cousin is your shared grandparent.
  - The LCA of you and your child is **you** (because a node can be a descendant of itself).

**Examples:**

```python
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
Explanation: Nodes 5 and 1 are in different subtrees of the root 3. Their closest shared parent is 3.

Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5
Explanation: Node 4 is a descendant of Node 5. Therefore, Node 5 is the LCA.
```

## Key Insights

### The Recursive "Bottom-Up" Approach

The key insight to solving this elegantly is to use **recursion**. We can traverse the tree with a function that asks a simple question at every node: "Does this subtree contain `p` or `q`?" The answer will "bubble up" from the bottom of the tree.

This is a form of **post-order traversal** (`Left -> Right -> Root`), because a node can only make a decision about itself *after* it has received the results from its left and right children.

### The Three Scenarios

For any given `node` in the tree, after it recursively calls the function on its left and right children, there are three possible outcomes:

1.  **One Child Found Something**: If the left subtree found one of the nodes (`p` or `q`) and the right subtree found nothing, it means both `p` and `q` must be in the left subtree. The LCA must also be in the left subtree. So, we pass the result from the left child up to the parent. The same logic applies if only the right child found something.

2.  **Both Children Found Something**: If the left subtree returned a node (say `p`) and the right subtree returned a node (say `q`), then our current `node` is the **first meeting point** for these two branches. This `node` is therefore the **Lowest Common Ancestor**. This is the "Aha\!" moment where we find our answer.

3.  **This Node *is* `p` or `q`**: If our current `node` is one of the targets (`p` or `q`), we don't need to look any further down this path. We can stop and report this node back up to its parent.

## Solution Approach

This solution is a direct and beautiful implementation of the recursive, post-order traversal strategy. The function's return value is used to pass information up the call stack.

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # Base Case: If the current node is null, or if it is one of the nodes
        # we are looking for (p or q), we have found what we need on this path.
        # Return this node.
        if not root or root == p or root == q:
            return root
            
        # Recursive Step: Search for p and q in the left and right subtrees.
        left_result = self.lowestCommonAncestor(root.left, p, q)
        right_result = self.lowestCommonAncestor(root.right, p, q)
        
        # --- Analysis Step (after children have reported back) ---
        
        # Case 1: p and q were found in different subtrees (one left, one right).
        # This means the current 'root' is their meeting point, the LCA.
        if left_result and right_result:
            return root
            
        # Case 2: Both p and q are in one of the subtrees.
        # One of the results will be a node, the other will be None.
        # The 'or' operator elegantly returns the non-None result, passing
        # the potential LCA up the call stack.
        return left_result or right_result
```

## Detailed Code Analysis

### Step 1: The Base Case

```python
if not root or root == p or root == q:
    return root
```

  - This is the **stopping condition** for the recursion. The "search party" on a given path stops when:
      - `not root`: It hits an empty branch. It reports back `None` (found nothing).
      - `root == p` or `root == q`: It finds one of the targets\! It reports this node back up. This is crucial for the "node can be a descendant of itself" rule.

### Step 2: The Recursive Calls

```python
left_result = self.lowestCommonAncestor(root.left, p, q)
right_result = self.lowestCommonAncestor(root.right, p, q)
```

  - This is the "dive down" phase of the DFS. The function calls itself, sending search parties down into the left and right subtrees to find `p` or `q`.

### Step 3: The Analysis

This is the post-order part, happening after the recursive calls have returned.

```python
if left_result and right_result:
    return root
```

  - This is the "LCA found" condition. `left_result` being non-`None` means `p` or `q` (or their LCA) was found in the left subtree. `right_result` being non-`None` means the other one was found in the right.
  - If both are non-`None`, the current `root` is the first node that sits above both `p` and `q`. It is the LCA. We return it, and this becomes the final answer that bubbles all the way up.

<!-- end list -->

```python
return left_result or right_result
```

  - This line handles the case where `p` and `q` are in the same subtree.
  - If `left_result` is a node and `right_result` is `None`, the expression `Node or None` evaluates to `Node`.
  - If `left_result` is `None` and `right_result` is a node, the expression `None or Node` evaluates to `Node`.
  - If both are `None`, it returns `None`.
  - This elegantly "passes up" the result from whichever child found something, continuing the search for the meeting point at a higher level.

## Step-by-Step Execution Trace

Let's trace `root = [3,5,1,6,2,0,8,...,7,4]`, `p = 5`, `q = 4`.

**Tree Structure (simplified):**

```
      3
     / \
    5   1
   / \
  6   2
     / \
    7   4
```

The calls are indented to show depth.

1.  `LCA(3, p=5, q=4)` is called.

      - Calls `LCA(5, p=5, q=4)`.

2.  `LCA(5, p=5, q=4)` is called.

      - **Base Case hits\!** `root == p` is true.
      - **Returns `Node(5)`**.

3.  Back at `LCA(3, p=5, q=4)`:

      - `left_result` is now `Node(5)`.
      - Now it calls `LCA(1, p=5, q=4)`.

4.  `LCA(1, p=5, q=4)` is called.

      - Calls `LCA(0, p=5, q=4)`, which will return `None`.
      - Calls `LCA(8, p=5, q=4)`, which will return `None`.
      - `left_result` is `None`, `right_result` is `None`.
      - **Returns `None or None` -\> `None`**.

5.  Back at the top-level `LCA(3, p=5, q=4)`:

      - `left_result` is `Node(5)`.
      - `right_result` is `None`.
      - The `if left_result and right_result:` check is **false**.
      - It executes `return left_result or right_result`.
      - `Node(5) or None` evaluates to `Node(5)`.
      - The function **returns `Node(5)`**, which is the correct answer.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The DFS algorithm visits every node at most once.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by the recursion call stack.
  - **Worst Case**: `O(n)` for a completely skewed tree.
  - **Best Case**: `O(log n)` for a completely balanced tree.