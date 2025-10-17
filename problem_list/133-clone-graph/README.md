# 133\. Clone Graph - Solution Explanation

## Problem Overview

You are given a single starting `node` from a **connected, undirected graph**. The task is to create a **deep copy** of the entire graph and return the copy of the starting node.

**Deep Copy Definition:**
A deep copy means that you must create a completely new graph.

  - Every node in the new graph must be a brand new `Node` object.
  - The value (`val`) of each new node must be the same as its corresponding original node.
  - The connections (the `neighbors` list) must be replicated. If `Node A` is connected to `Node B` in the original graph, then `Copy of A` must be connected to `Copy of B` in the new graph.
  - No node in the new graph should have any pointers leading back to a node in the original graph.

**Example:**

  - **Input Graph**: A graph where Node 1 is connected to Nodes 2 and 4.
  - **Output**: A reference to a *new* Node 1, which is part of a *new* graph that has the exact same structure as the original.

## Key Insights

### 1\. The Challenge: Cycles and Shared Nodes

This problem is more complex than just copying a list or a simple tree. Graphs have two key properties that make a naive traversal fail:

  - **Cycles**: A graph can have loops (e.g., A -\> B -\> C -\> A). A simple recursive traversal would enter this loop and run forever, causing a stack overflow.
  - **Shared Nodes**: A single node can be a neighbor to many other nodes (e.g., A -\> C and B -\> C). When we are cloning the neighbors of A, we create a copy of C. Later, when we are cloning the neighbors of B, we must connect to the **exact same copy of C we already made**, not create a second one.

### 2\. The Solution: A "Visited" Map

The key insight to solve both of these problems is to use a **hash map** (a `dict` in Python). This map will act as our memory, tracking the nodes we have already visited and copied.

The map will store key-value pairs of: **`{ original_node: its_copy }`**

This map serves two critical purposes:

1.  **It's a "visited" set**: Before we try to clone a node, we check if it's already a key in our map. If it is, we know we've been here before, which prevents us from getting stuck in cycles.
2.  **It's a "copy cache"**: If a node is in the map, we don't need to create a new copy. We can just grab the existing copy from the map's value. This ensures that a single original node only ever has a single corresponding copy.

### 3\. The Traversal: Depth-First Search (DFS)

A **Depth-First Search (DFS)**, implemented recursively, is a very natural way to explore a graph. We can create a recursive helper function that is responsible for cloning a single node and all of its descendants.

## Solution Approach

This solution uses a hash map to store the mapping from original nodes to their copies. A recursive DFS function, `dfs_clone`, is the engine of the algorithm. It ensures that each node is copied only once and handles cycles gracefully.

```python
from typing import Optional

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        # This hash map stores the mapping from old nodes to their new copies.
        # It also implicitly acts as our "visited" set.
        old_to_new = {}

        def dfs_clone(original_node):
            # Base Case / Cycle Detection: If we have already created a copy
            # of this node, don't do it again. Just return the existing copy.
            if original_node in old_to_new:
                return old_to_new[original_node]
            
            # If not, this is the first time we've seen this node.
            # 1. Create a new copy of the node.
            copy_node = Node(original_node.val)
            
            # 2. IMPORTANT: Add the copy to our map BEFORE the recursive calls.
            # This is what prevents infinite loops in cycles.
            old_to_new[original_node] = copy_node
            
            # 3. Now, recursively clone all of its neighbors.
            for neighbor in original_node.neighbors:
                copy_node.neighbors.append(dfs_clone(neighbor))
                
            # 4. Return the fully cloned node.
            return copy_node

        # Handle the edge case of an empty graph.
        if not node:
            return None
        
        # Start the recursive cloning process from the given starting node.
        return dfs_clone(node)
```

## Detailed Code Analysis

### The `old_to_new` Hash Map

```python
old_to_new = {}
```

  - This is the most important data structure in the solution. It is initialized once and shared across all recursive calls. It's our single source of truth for what has been copied.

### The `dfs_clone` Helper Function

This recursive function does all the heavy lifting. Its job is simple: "Given an `original_node`, return a complete, deep copy of it."

**1. The Base Case and Cycle Stopper**

```python
if original_node in old_to_new:
    return old_to_new[original_node]
```

  - This is the first and most critical step inside the recursive function. Before doing any work, it checks the map.
  - If the `original_node` is already a key in the map, it means we have already started (or finished) creating a copy of it during a previous step or recursive call.
  - We simply return the existing copy from the map. This action instantly solves both the "shared node" problem and the "infinite cycle" problem.

**2. Node Creation and Pre-caching**

```python
copy_node = Node(original_node.val)
old_to_new[original_node] = copy_node
```

  - If the node is not in the map, we create its copy.
  - The next line is **extremely important**. We immediately place this new, incomplete copy into the `old_to_new` map. Why? Imagine a cycle `A -> B -> A`. When `dfs_clone(A)` is called, it creates `copy_A` and puts it in the map. Then it calls `dfs_clone(B)`. Inside `dfs_clone(B)`, it creates `copy_B` and puts it in the map. Then `dfs_clone(B)` tries to clone its neighbor, which is `A`. This triggers a new call to `dfs_clone(A)`. This time, the base case `if A in old_to_new:` is **true**, and it returns the `copy_A` we created earlier, preventing an infinite loop.

**3. The Recursive Step**

```python
for neighbor in original_node.neighbors:
    copy_node.neighbors.append(dfs_clone(neighbor))
```

  - Now that our current `copy_node` is safely in the map, we can build its `neighbors` list.
  - We iterate through the neighbors of the `original_node`.
  - For each `neighbor`, we recursively call `dfs_clone`. This call will return a copy of that neighbor (either by creating a new one or by retrieving an existing one from the map).
  - We then `append` this returned copy to our `copy_node`'s neighbor list.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `adjList = [[2,4],[1,3],[2,4],[1,3]]` with extreme detail. Let's call the nodes N1, N2, N3, N4.

1.  **Initial Call**: `cloneGraph(N1)` is called. The `old_to_new` map is `{}`.

2.  `dfs_clone(N1)` is called.

      - `N1` is not in the map.
      - Create `copy_N1`.
      - Update map: `old_to_new` is now `{ N1: copy_N1 }`.
      - Loop through `N1`'s neighbors: `[N2, N4]`.
      - First neighbor is `N2`. Call `dfs_clone(N2)`.

3.  **`dfs_clone(N2)` is called.**

      - `N2` is not in the map.
      - Create `copy_N2`.
      - Update map: `old_to_new` is now `{ N1: copy_N1, N2: copy_N2 }`.
      - Loop through `N2`'s neighbors: `[N1, N3]`.
      - First neighbor is `N1`. Call `dfs_clone(N1)`.

4.  **`dfs_clone(N1)` is called again.**

      - **Base Case hits\!** `N1` is now in the `old_to_new` map.
      - It immediately returns the existing `copy_N1` from the map.

5.  Back inside `dfs_clone(N2)`:

      - The call for `N1` returned `copy_N1`. So, `copy_N2.neighbors.append(copy_N1)`.
      - Next neighbor of `N2` is `N3`. Call `dfs_clone(N3)`.

This process continues. The map acts as a central registry, ensuring that any time a node is needed, its one and only copy is used. The recursion naturally explores the entire graph, and the base case handles all the complexity of cycles and shared nodes.

## Performance Analysis

### Time Complexity: O(N + E)

  - Where `N` is the number of nodes (vertices) and `E` is the number of edges.
  - The DFS algorithm visits each node and each edge exactly once. For each node, we do a constant amount of work (creation, map insertion). For each edge, we make one recursive call.

### Space Complexity: O(N)

  - The space complexity is dominated by two factors:
    1.  The `old_to_new` hash map, which will store all `N` nodes.
    2.  The recursion call stack. In the worst case (a graph that is a long chain), the recursion depth can be `O(N)`.
  - Therefore, the total space complexity is `O(N)`.