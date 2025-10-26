# 1466\. Reorder Routes to Make All Paths Lead to the City Zero - Solution Explanation

## Problem Overview

You are given a map of `n` cities (numbered 0 to `n-1`) and `n-1` one-way roads connecting them. The connections form a **tree** structure (meaning there's exactly one path between any two cities). City 0 is the capital.

The current road directions might prevent travel *towards* the capital. Your task is to find the **minimum number of roads** you need to reverse (reorient) so that it becomes possible to travel from **any city** to the capital (city 0).

**Input:**

  - `n`: The number of cities.
  - `connections`: A list of pairs `[a, b]`, representing a road directed **from `a` to `b`**.

**Output:**

  - The minimum number of road reversals needed.

**Example:**

```python
Input: n = 6, connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]
Output: 3
Explanation:
- The roads 0->1, 1->3, and 4->5 point away from city 0 if you start exploring from city 0. Reversing these three allows all cities to reach 0.
```

## Key Insights

### 1\. The Tree Structure Guarantee

The problem states the city network forms a **tree**. This is crucial because it means:

  - There are no cycles.
  - There is exactly one unique path between any two cities.
  - The goal of making city 0 reachable from *everywhere* is achievable.

### 2\. Thinking Backwards vs. Forwards

We want all paths to lead *to* city 0. It might seem intuitive to check paths from every city *towards* city 0. However, it's often easier in graph traversals to start from a known point and explore outwards.

What if we start our traversal **from city 0** and explore the city network? As we move from a city `u` to an adjacent city `v`, we can check the *original* direction of the road connecting them.

  - If the original road was `u -> v`, this road is pointing **away** from city 0 (relative to our traversal direction). It needs to be reversed.
  - If the original road was `v -> u`, this road is pointing **towards** city 0. It's already correct.

This gives us a clear strategy: Traverse the tree starting from city 0. Count how many roads are oriented *away* from our starting point during this traversal.

### 3\. Representing Edge Direction

Since the original `connections` list only gives us one direction (`a -> b`), but we need to traverse the tree freely (like an *undirected* graph for traversal purposes), we need an adjacency list that stores neighbors regardless of the original road direction. However, we *also* need to remember the original direction to count reversals.

We can build an adjacency list where each entry stores `(neighbor, cost)`:

  - For an original connection `[u, v]` (meaning `u -> v`):
      - When building the neighbors for `u`, add `(v, 1)`. The `1` signifies that moving from `u` to `v` follows the original *outward* direction, hence costing 1 reversal.
      - When building the neighbors for `v`, add `(u, 0)`. The `0` signifies that moving from `v` to `u` goes *against* the original outward direction (i.e., it points inwards), hence costing 0 reversals.

### 4\. Traversal Algorithm: BFS

A **Breadth-First Search (BFS)** is a suitable algorithm to explore the tree starting from city 0. We'll use a queue and a `visited` set to manage the traversal. As we explore an edge from `city` to `neighbor`, we simply add the associated `cost` (0 or 1) to our total count.

## Solution Approach

This solution builds an adjacency list that encodes the original direction of each road. It then performs a BFS starting from city 0, adding up the "costs" associated with traversing edges in the direction away from city 0.

```python
import collections
from typing import List

class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        
        # --- Step 1: Build the Graph Representation ---
        # We use an adjacency list. The graph is treated as undirected for traversal,
        # but we store the cost (need for reversal) for each direction.
        graph = collections.defaultdict(list)
        for u, v in connections:
            # For the original direction u -> v:
            #   - Traveling u to v follows the original arrow (away from 0 if u is closer). Cost = 1.
            graph[u].append((v, 1))
            #   - Traveling v to u goes against the original arrow (towards 0 if u is closer). Cost = 0.
            graph[v].append((u, 0))
            
        # --- Step 2: Initialize BFS ---
        queue = collections.deque([0]) # Start BFS from the capital, city 0.
        visited = {0}                  # Keep track of visited cities.
        reorder_count = 0              # Initialize the count of roads to reverse.
        
        # --- Step 3: Perform BFS ---
        while queue:
            # Get the current city from the front of the queue.
            city = queue.popleft()
            
            # Explore all neighbors connected to the current city.
            for neighbor, cost in graph[city]:
                # If we haven't visited this neighbor yet...
                if neighbor not in visited:
                    # Mark it as visited.
                    visited.add(neighbor)
                    # Add the cost to our reversal count.
                    # 'cost' is 1 if the original edge was city -> neighbor (needs reversal).
                    # 'cost' is 0 if the original edge was neighbor -> city (already correct).
                    reorder_count += cost 
                    # Add the neighbor to the queue to explore from it later.
                    queue.append(neighbor)
                    
        # --- Step 4: Return the total count ---
        return reorder_count
```

## Detailed Code Analysis

### Step 1: Building the Graph

```python
graph = collections.defaultdict(list)
for u, v in connections:
    graph[u].append((v, 1))
    graph[v].append((u, 0))
```

  - `graph = collections.defaultdict(list)`: We use a `defaultdict` to easily append neighbors. `graph[city]` will be a list of tuples.
  - The loop iterates through each connection `[u, v]`, which represents a road originally directed `u -> v`.
  - **`graph[u].append((v, 1))`**: We add an entry for city `u`. Its neighbor is `v`. The cost `1` signifies that traversing *from* `u` *to* `v` follows the original road direction. Since our BFS starts at 0 and moves outwards, following this original direction means the road points *away* from 0 and needs reversal.
  - **`graph[v].append((u, 0))`**: We also add an entry for city `v`. Its neighbor is `u`. The cost `0` signifies that traversing *from* `v` *to* `u` goes *against* the original road direction (`u -> v`). If our BFS takes this path, it means the original road was already pointing *towards* 0, so no reversal is needed for this specific traversal step.

### Step 2: Initializing BFS

```python
queue = collections.deque([0])
visited = {0}
reorder_count = 0
```

  - `queue`: An efficient `deque` initialized with our starting point, city 0.
  - `visited`: A `set` for fast O(1) checking of visited nodes. We add city 0 immediately.
  - `reorder_count`: Our accumulator for the final answer, initialized to 0.

### Step 3: The BFS Loop

```python
while queue:
    city = queue.popleft()
    # ... process neighbors ...
```

  - The loop continues as long as there are cities in the queue to explore. `popleft()` gets the next city in a FIFO manner.

### Step 4: Processing Neighbors

```python
for neighbor, cost in graph[city]:
    if neighbor not in visited:
        visited.add(neighbor)
        reorder_count += cost
        queue.append(neighbor)
```

  - We iterate through all adjacent cities (`neighbor`) connected to the current `city`.
  - **`if neighbor not in visited:`**: We only process neighbors we haven't reached before. This prevents infinite loops and ensures we traverse each necessary edge only once outwards from city 0.
  - **`visited.add(neighbor)`**: Mark the neighbor as visited.
  - **`reorder_count += cost`**: This is the core logic. We add the `cost` associated with the edge we just traversed (`city` -\> `neighbor`).
      - If the original road was `city -> neighbor`, the stored `cost` is `1`. This means the road pointed away from city 0, and we add `1` to our reversal count.
      - If the original road was `neighbor -> city`, the stored `cost` is `0`. This means the road pointed towards city 0, and we add `0` (no reversal needed for this edge).
  - **`queue.append(neighbor)`**: Add the newly visited neighbor to the queue so we can explore *its* neighbors later.

## Step-by-Step Execution Trace

Let's trace `n = 6`, `connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]` with extreme detail.

### **1. Build Graph:**

  - `graph = {`
    `0: [(1, 1), (4, 0)],`
    `1: [(0, 0), (3, 1)],`
    `2: [(3, 1)],`
    `3: [(1, 0), (2, 0)],`
    `4: [(0, 1), (5, 1)],`
    `5: [(4, 0)]`
  - `}`

### **2. Initialize BFS:**

  - `queue = deque([0])`
  - `visited = {0}`
  - `reorder_count = 0`

-----

### **BFS Loop Iterations:**

| Dequeued `city` | Neighbors `(neighbor, cost)` | `neighbor` | `visited` Check | Action (`reorder_count += cost`, add to `visited`, `queue`) | `reorder_count` | `visited` | `queue` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start**| - | - | - | - | 0 | `{0}` | `[0]` |
| **0** | `[(1, 1), (4, 0)]` | 1 | Not visited | `reorder += 1`. Add 1. Enqueue 1. | 1 | `{0, 1}` | `[4, 1]` |
| | | 4 | Not visited | `reorder += 0`. Add 4. Enqueue 4. | 1 | `{0, 1, 4}` | `[1, 4]` |
| **1** | `[(0, 0), (3, 1)]` | 0 | Visited | - | 1 | `{0, 1, 4}` | `[4]` |
| | | 3 | Not visited | `reorder += 1`. Add 3. Enqueue 3. | 2 | `{0, 1, 4, 3}`| `[4, 3]` |
| **4** | `[(0, 1), (5, 1)]` | 0 | Visited | - | 2 | `{0, 1, 4, 3}`| `[3]` |
| | | 5 | Not visited | `reorder += 1`. Add 5. Enqueue 5. | 3 | `{0, 1, 4, 3, 5}`| `[3, 5]` |
| **3** | `[(1, 0), (2, 0)]` | 1 | Visited | - | 3 | `{0, 1, 4, 3, 5}`| `[5]` |
| | | 2 | Not visited | `reorder += 0`. Add 2. Enqueue 2. | 3 | `{0,1,4,3,5,2}`| `[5, 2]` |
| **5** | `[(4, 0)]` | 4 | Visited | - | 3 | `{0,1,4,3,5,2}`| `[2]` |
| **2** | `[(3, 1)]` | 3 | Visited | - | 3 | `{0,1,4,3,5,2}`| `[]` |

  - The queue is now empty. The loop terminates.

-----

### **Final Result**

  - The function returns the final `reorder_count`, which is **3**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of cities (nodes).
  - The graph representation is a tree, so the number of connections (edges) is `n - 1`.
  - Building the graph takes `O(n)` time (proportional to the number of connections).
  - The BFS traversal visits each node and each edge exactly once. Since `E = n - 1`, the BFS takes `O(V + E) = O(n + n) = O(n)` time.
  - The overall time complexity is `O(n)`.

### Space Complexity: O(n)

  - The `graph` (adjacency list) stores `n` nodes and `2 * (n - 1)` edge entries, which is `O(n)`.
  - The `visited` set can store up to `n` elements.
  - The `queue` can store up to `n` elements in the worst case (a star graph).
  - The overall space complexity is `O(n)`.