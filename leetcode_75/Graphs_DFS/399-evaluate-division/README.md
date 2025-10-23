# 399\. Evaluate Division - Solution Explanation

## Problem Overview

You are given a set of equations in the form `A / B = value`, represented by two lists: `equations` (pairs of variables like `["a", "b"]`) and `values` (the result of the division, like `2.0`). You are also given a list of `queries`, each asking for the result of a division `C / D = ?`.

Your task is to calculate the answer for each query. If the answer cannot be determined from the given equations (e.g., if a variable is unknown or there's no path between the variables), you should return `-1.0`.

**Examples:**

```python
Input:
equations = [["a","b"],["b","c"]], values = [2.0,3.0]
queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]

Output: [6.0, 0.5, -1.0, 1.0, -1.0]

Explanation:
Given: a/b = 2.0, b/c = 3.0
- a/c = (a/b) * (b/c) = 2.0 * 3.0 = 6.0
- b/a = 1 / (a/b) = 1 / 2.0 = 0.5
- a/e: 'e' is undefined. Result is -1.0
- a/a: Always 1.0 for defined variables.
- x/x: 'x' is undefined. Result is -1.0
```

## Key Insights

### 1\. The Graph Representation

The core insight is that the equations define a **directed graph**.

  - Each variable (like `"a"`, `"b"`) is a **node**.
  - Each equation `A / B = value` represents **two directed edges**:
      - An edge from `A` to `B` with a weight representing the ratio `A / B`.
      - An edge from `B` to `A` with a weight representing the ratio `B / A`, which is `1 / value`.

### 2\. Path Finding as Multiplication

The second key insight is how to evaluate a query like `C / D = ?`.

  - If we have a path from `C` to `D` in our graph, like `C -> n1 -> n2 -> D`, the value of `C / D` is the **product** of the edge weights along that path:
    `(C / n1) * (n1 / n2) * (n2 / D)`
  - This means the problem of evaluating a division query is equivalent to finding a path between the two nodes in the graph and multiplying the weights along that path.

### 3\. Choosing a Traversal Algorithm

Since we need to find *if* a path exists and calculate the product along it, both **Depth-First Search (DFS)** and **Breadth-First Search (BFS)** are suitable graph traversal algorithms. BFS is often slightly easier to implement iteratively using a queue and can be good for finding *a* path efficiently.

## Solution Approach

This solution builds a directed graph where edge weights represent the direct division ratio. It then uses BFS for each query to find a path from the numerator variable to the denominator variable, accumulating the product of the edge weights along the way.

```python
import collections
from typing import List

class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        
        # --- Step 1: Build the Graph ---
        # graph maps a variable -> list of (neighbor, ratio)
        # An edge from A to B with weight 'val' represents A / B = val.
        graph = collections.defaultdict(list)
        for i, (A, B) in enumerate(equations):
            val = values[i]
            graph[A].append((B, val))
            graph[B].append((A, 1.0 / val))

        # --- Step 2: Define the BFS function ---
        def bfs(start_node, end_node):
            """
            Performs BFS to find the value of start_node / end_node.
            Returns the product of weights along the path, or -1.0 if no path.
            """
            # Handle cases where one or both nodes are not in the graph at all.
            if start_node not in graph or end_node not in graph:
                return -1.0
            
            # Queue stores tuples of (current_node, current_product_value)
            # where current_product_value = start_node / current_node
            queue = collections.deque([(start_node, 1.0)])
            # 'visited' set tracks nodes visited *within this specific query*
            # to prevent infinite loops in cycles.
            visited = {start_node}
            
            while queue:
                current_node, current_product = queue.popleft()
                
                # Check if we have reached the target node.
                if current_node == end_node:
                    return current_product # Success!
                    
                # Explore neighbors.
                for neighbor, ratio in graph[current_node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        # The new product = (start / current) * (current / neighbor)
                        # This simplifies to start / neighbor.
                        new_product = current_product * ratio
                        queue.append((neighbor, new_product))
                        
            # If the queue becomes empty, no path was found.
            return -1.0

        # --- Step 3: Process all queries ---
        results = []
        for C, D in queries:
            # Add the result of the BFS (or -1.0) to our results list.
            # No special handling needed for C == D, BFS handles it correctly.
            results.append(bfs(C, D))
                
        return results
```

## Detailed Code Analysis

### Step 1: Building the Graph

```python
graph = collections.defaultdict(list)
for i, (A, B) in enumerate(equations):
    val = values[i]
    graph[A].append((B, val))
    graph[B].append((A, 1.0 / val))
```

  - `graph = collections.defaultdict(list)`: We use a `defaultdict` where each value is initialized as an empty list. This simplifies adding neighbors.
  - The loop iterates through each equation `A / B = val`.
  - `graph[A].append((B, val))`: We add an edge from `A` to `B` with the weight `val`, representing `A / B = val`.
  - `graph[B].append((A, 1.0 / val))`: We add the inverse edge from `B` to `A` with the weight `1.0 / val`, representing `B / A = 1 / val`.

### Step 2: The `bfs` Function

This function takes the `start_node` (numerator `C`) and `end_node` (denominator `D`) and finds the value `C / D`.

**Initialization and Edge Cases:**

```python
if start_node not in graph or end_node not in graph:
    return -1.0
queue = collections.deque([(start_node, 1.0)])
visited = {start_node}
```

  - The first `if` check handles cases where one of the query variables never appeared in the input equations.
  - The `queue` is initialized. The tuple `(node, product)` stores the node we are currently at and the accumulated product `start_node / node`. For the `start_node` itself, this ratio is `1.0`.
  - The `visited` set is crucial for each BFS call to prevent infinite loops if the graph has cycles and to avoid redundant calculations.

**The BFS Loop:**

```python
while queue:
    current_node, current_product = queue.popleft()
    if current_node == end_node:
        return current_product
    # ... explore neighbors ...
```

  - The loop continues as long as there are nodes to explore.
  - We dequeue the next node and its associated product.
  - If we've reached the `end_node`, the `current_product` is our answer (`start_node / end_node`).

**Exploring Neighbors:**

```python
for neighbor, ratio in graph[current_node]:
    if neighbor not in visited:
        visited.add(neighbor)
        new_product = current_product * ratio
        queue.append((neighbor, new_product))
```

  - We iterate through the neighbors of the `current_node`.
  - `ratio` is the value `current_node / neighbor`.
  - If we haven't visited this `neighbor` *during this specific BFS query*, we mark it as visited.
  - **`new_product = current_product * ratio`**: This is the core calculation.
      - `current_product = start_node / current_node`
      - `ratio = current_node / neighbor`
      - `new_product = (start_node / current_node) * (current_node / neighbor)`
      - `new_product = start_node / neighbor`
  - We enqueue the `neighbor` along with its calculated `new_product`.

**Failure Case:**

```python
return -1.0
```

  - If the `while` loop finishes without ever finding the `end_node`, it means there is no path, and we return `-1.0`.

### Step 3: Processing Queries

```python
results = []
for C, D in queries:
    results.append(bfs(C, D))
return results
```

  - We simply iterate through each query `[C, D]` and call our `bfs` function to get the result, appending it to our final `results` list. (Note: The BFS correctly handles `C == D` because it starts with `(C, 1.0)` and immediately finds `C == C`, returning `1.0`. It also correctly returns `-1.0` if `C` wasn't in the graph).

## Step-by-Step Execution Trace

Let's trace the query `["a", "c"]` for `equations = [["a","b"],["b","c"]]`, `values = [2.0,3.0]`.

1.  **Build Graph**:

      * `a / b = 2.0` -\> `graph['a'] = [('b', 2.0)]`, `graph['b'] = [('a', 0.5)]`
      * `b / c = 3.0` -\> `graph['b'].append(('c', 3.0))`, `graph['c'] = [('b', 1/3.0)]`
      * `graph` is `{ 'a': [('b', 2.0)], 'b': [('a', 0.5), ('c', 3.0)], 'c': [('b', 0.333...)] }`

2.  **Call `bfs(start_node='a', end_node='c')`**:

      * **Initialization**: `queue = deque([('a', 1.0)])`, `visited = {'a'}`.
      * **Loop 1**:
          * Dequeue `('a', 1.0)`. `current_node = 'a'`, `current_product = 1.0`.
          * `'a' != 'c'`.
          * Neighbors of 'a': `('b', 2.0)`.
          * `'b'` is not visited. Add `'b'` to `visited`.
          * `new_product = 1.0 * 2.0 = 2.0`.
          * Enqueue `('b', 2.0)`. `queue` is now `deque([('b', 2.0)])`.
      * **Loop 2**:
          * Dequeue `('b', 2.0)`. `current_node = 'b'`, `current_product = 2.0`.
          * `'b' != 'c'`.
          * Neighbors of 'b': `('a', 0.5)`, `('c', 3.0)`.
          * Neighbor 'a': `'a'` is in `visited`. Skip.
          * Neighbor 'c': `'c'` is not visited. Add `'c'` to `visited`.
          * `new_product = 2.0 * 3.0 = 6.0`.
          * Enqueue `('c', 6.0)`. `queue` is now `deque([('c', 6.0)])`.
      * **Loop 3**:
          * Dequeue `('c', 6.0)`. `current_node = 'c'`, `current_product = 6.0`.
          * `'c' == 'c'`. **Match found\!**
          * **Return `current_product` (6.0)**.

3.  The result `6.0` is added to the `results` list.

## Performance Analysis

### Time Complexity: O(E + Q \* (V + E)) -\> Simplified: O(N + Q\*N)

  - Where `N` is the number of equations (edges), `V` is the number of unique variables (vertices), and `Q` is the number of queries.
  - **Building the graph**: Takes `O(N)` time, as we process each equation once.
  - **BFS per query**: In the worst case, a BFS might visit all `V` nodes and `E` edges. `E` is at most `2*N`. So, one BFS is `O(V + E)`.
  - **Total**: `O(N + Q * (V + E))`. Since `V` can be up to `2*N`, this is roughly `O(N + Q*N)`.

### Space Complexity: O(N)

  - The `graph` stores `V` nodes and `E` edges. `V` is at most `2*N`, `E` is `2*N`. So, graph space is `O(N)`.
  - The BFS `queue` and `visited` set can grow up to `O(V)` in the worst case per query.
  - Overall space complexity is dominated by the graph storage, `O(N)`.