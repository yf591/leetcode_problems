# 437\. Path Sum III - Solution Explanation

## Problem Overview

You are given the `root` of a binary tree and an integer `targetSum`. The goal is to find the total number of **paths** in the tree where the sum of the node values along the path equals `targetSum`.

**Key Definitions:**

  - **Path**: A path must travel downwards from parent nodes to child nodes.
  - **Important**: The path **does not need to start at the root or end at a leaf**. It can begin at any node and end at any of its descendants.

**Example:**

```python
Input: root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
Output: 3
Explanation: The three paths that sum to 8 are:
1.  5 -> 3
2.  5 -> 2 -> 1
3. -3 -> 11
```

## Key Insights

### The Brute-Force (but slow) Approach

A naive way to solve this is to think of it as two nested problems:

1.  A function that traverses every node in the tree (`dfs_start_node`).
2.  For *each* of those nodes, start a *second* traversal downwards (`dfs_find_path`) that sums up all possible paths starting from that node and counts how many equal `targetSum`.

This is an `O(n²)` solution (or `O(n log n)` for a balanced tree) because of the nested traversals. It's too slow.

### The Prefix Sum Insight (The `O(n)` solution)

The key to an efficient solution is to avoid the nested traversals by using a clever mathematical trick common in array problems: the **prefix sum**.

A **prefix sum** for a tree path is the sum of values from the **root** down to a specific node.
Let's say we are currently at a node `C`, and the sum of the path from the root to `C` is `current_sum`. Let's also say there is some ancestor node `A` on the path to `C`. The sum from the root to `A` is `prefix_sum(A)`.

The sum of the path *between* `A` and `C` can be calculated as:
`path_sum(A to C) = current_sum - prefix_sum(A)`

We are looking for paths where `path_sum(A to C)` is equal to our `targetSum`.
`targetSum = current_sum - prefix_sum(A)`

By rearranging this equation, we get the magic formula:
**`prefix_sum(A) = current_sum - targetSum`**

This formula tells us that as we traverse the tree, if we are at a node with a `current_sum`, we just need to ask: "How many times on the path to get here have I seen a prefix sum equal to `current_sum - targetSum`?" Each time we have, it means we've just completed a valid path. A **hash map** is the perfect data structure to store and look up these prefix sum counts in O(1) time.

## Solution Approach

This solution uses a single Depth-First Search (DFS) traversal. It maintains a running `current_path_sum` and uses a hash map (`prefix_sum_counts`) to store the frequencies of the prefix sums encountered on the path to the current node. **Backtracking** is crucial to ensure that prefix sums from one branch do not affect sibling branches.

```python
import collections
from typing import Optional

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        # Map to store {prefix_sum: frequency}
        self.prefix_sum_counts = collections.defaultdict(int)
        # Base case: A sum of 0 has a frequency of 1 (the path before the root).
        self.prefix_sum_counts[0] = 1
        
        self.count = 0
        self.dfs(root, 0, targetSum)
        return self.count

    def dfs(self, node: Optional[TreeNode], current_path_sum: int, targetSum: int):
        # Base case for recursion
        if not node:
            return

        # 1. Update the current path sum with the current node's value.
        current_path_sum += node.val
        
        # 2. Check if a path ending here sums to targetSum.
        complement = current_path_sum - targetSum
        self.count += self.prefix_sum_counts[complement]
        
        # 3. Add the current path sum to the map for its descendants to use.
        self.prefix_sum_counts[current_path_sum] += 1
        
        # 4. Recurse on children.
        self.dfs(node.left, current_path_sum, targetSum)
        self.dfs(node.right, current_path_sum, targetSum)
        
        # 5. Backtrack: Remove the current path sum from the map when moving back up.
        self.prefix_sum_counts[current_path_sum] -= 1
```

## Detailed Code Analysis

### Step 1: Initialization

```python
self.prefix_sum_counts = collections.defaultdict(int)
self.prefix_sum_counts[0] = 1
self.count = 0
```

  - `prefix_sum_counts`: A hash map (specifically a `defaultdict` for convenience, which initializes new keys with a value of `0`) to store the frequency of each prefix sum.
  - **`self.prefix_sum_counts[0] = 1`**: This is a critical initialization. It represents a "path of sum 0" that exists before we even start at the root. This is necessary to correctly count paths that start from the root itself. For example, if a path from the root to a node has a sum equal to `targetSum`, then `current_path_sum - targetSum` will be `0`, and we need to find a count of `1` for the prefix sum of `0`.

### The `dfs` Helper Function

**Step 2: Update Current Sum**

```python
current_path_sum += node.val
```

  - As we move down to a new node, we add its value to the sum we've accumulated from its parent.

**Step 3: Check for Valid Paths**

```python
complement = current_path_sum - targetSum
self.count += self.prefix_sum_counts[complement]
```

  - This is the implementation of our key insight. We calculate the `complement` we are looking for (`current_sum - targetSum`).
  - We then look up this `complement` value in our `prefix_sum_counts` map. The value stored there tells us exactly how many ancestor nodes exist that can serve as a starting point for a valid path ending at our current node. We add this number to our total `count`.

**Step 4: Record for Descendants**

```python
self.prefix_sum_counts[current_path_sum] += 1
```

  - Before we visit the children of the current node, we must add its `current_path_sum` to the map. This makes it available for all of its descendants to use in their own calculations.

**Step 5: The Crucial Backtracking Step**

```python
self.prefix_sum_counts[current_path_sum] -= 1
```

  - This line is executed **after** the recursive calls to the left and right children have returned. It is the **backtracking** step.
  - When we finish exploring an entire branch (e.g., the whole left subtree), we must "undo" the changes we made to the `prefix_sum_counts` map for that branch.
  - By decrementing the count for the `current_path_sum`, we ensure that the prefix sums from the left subtree do not incorrectly influence the calculations for the right subtree (which is a sibling, not a descendant).

## Step-by-Step Execution Trace

Let's trace a simple path `10 -> 5 -> 3` from the example, with `targetSum = 8`.

| Function Call | `node.val`| `current_path_sum` | `complement` (`cps-8`) | `map` (before) | `self.count` (after check) | `map` (after update) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `dfs(10, 0, 8)` | 10 | 10 | 2 | `{0:1}` | `0 + map[2]` -\> 0 | `{0:1, 10:1}` |
| `dfs(5, 10, 8)` | 5 | 15 | 7 | `{0:1, 10:1}` | `0 + map[7]` -\> 0 | `{0:1, 10:1, 15:1}`|
| `dfs(3, 15, 8)` | 3 | 18 | 10 | `{0:1, 10:1, 15:1}`| `0 + map[10]` -\> 1 | `{0:1, 10:1, 15:1, 18:1}`|

Now, the recursion backtracks.

  - `dfs(3)` finishes. It executes `map[18] -= 1`. `map` becomes `{0:1, 10:1, 15:1}`.
  - `dfs(5)` finishes. It executes `map[15] -= 1`. `map` becomes `{0:1, 10:1}`.
  - `dfs(10)` finishes. It executes `map[10] -= 1`. `map` becomes `{0:1}`.

This trace shows how the count for the path `5 -> 3` (sum=8) was found. The `current_path_sum` at node 3 was 18. The `complement` was `18 - 8 = 10`. The map contained a count of 1 for the prefix sum of 10 (from the root node), so we added 1 to our total count.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of nodes in the tree. The DFS algorithm visits every node exactly once. Each operation inside the `dfs` function (dictionary lookup, addition) is `O(1)` on average.

### Space Complexity: O(h)

  - Where `h` is the height of the tree. This space is used by both the recursion call stack and the `prefix_sum_counts` hash map. In the worst case (a skewed tree), the height is `n`, so the space complexity becomes `O(n)`. In a balanced tree, it's `O(log n)`.