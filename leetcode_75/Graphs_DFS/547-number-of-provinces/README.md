# 547\. Number of Provinces - Solution Explanation

## Problem Overview

You are given information about `n` cities and their direct connections. The connections are represented by an `n x n` **adjacency matrix** called `isConnected`.

  - `isConnected[i][j] = 1` means city `i` and city `j` are directly connected.
  - `isConnected[i][j] = 0` means they are not directly connected.
  - Connections are **symmetric** (`isConnected[i][j] == isConnected[j][i]`) and every city is connected to itself (`isConnected[i][i] == 1`).

The goal is to find the total number of **provinces**.

**Province Definition:**
A province is a group of cities where every city in the group is connected to every other city in the group, either directly or indirectly, and no city in the group is connected to any city outside the group. In graph theory terms, a province is a **connected component**.

**Examples:**

```python
Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2
Explanation:
City 0 and City 1 are connected.
City 2 is isolated.
There are two provinces: {0, 1} and {2}.

Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3
Explanation: All cities are isolated. Each forms its own province.
```

## Key Insights

### 1\. Modeling as a Graph

This problem is inherently about graphs.

  - **Nodes**: Each city (`0` to `n-1`) is a node.
  - **Edges**: A `1` at `isConnected[i][j]` represents an **undirected edge** between node `i` and node `j`. (Although the matrix *could* represent a directed graph, the problem states `isConnected[i][j] == isConnected[j][i]`, confirming it's undirected).

### 2\. The Goal: Counting Connected Components

The definition of a "province" is exactly the definition of a **connected component** in an undirected graph. The problem boils down to: "Count the number of connected components in the graph represented by the `isConnected` matrix."

### 3\. Traversal Algorithms (DFS/BFS)

To find connected components, we need a way to explore all nodes reachable from a starting node. Standard graph traversal algorithms like **Depth-First Search (DFS)** or **Breadth-First Search (BFS)** are perfect for this.

### 4\. Preventing Recounts: The `visited` Array

When we start a traversal (like DFS) from a city to find its province, we need to make sure we don't accidentally start another traversal from a different city that belongs to the *same* province later on. We also need to avoid getting stuck in infinite loops if the graph has cycles (which it will, since `i` is connected to `j` and `j` back to `i`).

A **`visited` array** (or set) is essential. Before starting a traversal from a city, we check if it has already been visited. If not, we increment our province count and start the traversal. During the traversal, we mark every city we reach as visited.

## Solution Approach

This solution uses a Depth-First Search (DFS) approach. It iterates through each city. If a city hasn't been visited yet, it increments the province count and initiates a DFS starting from that city. The DFS recursively explores all connected cities and marks them as visited.

```python
from typing import List

class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        # Create a boolean array to track visited cities.
        visited = [False] * n
        province_count = 0

        # Define the recursive DFS helper function.
        def dfs(city_index):
            # Mark the current city as visited immediately upon entry.
            visited[city_index] = True
            # Explore all potential neighbors.
            for neighbor_index in range(n):
                # Check for two conditions:
                # 1. Is there a direct connection? (isConnected == 1)
                # 2. Have we visited this neighbor before? (not visited)
                if isConnected[city_index][neighbor_index] == 1 and not visited[neighbor_index]:
                    # If connected and unvisited, recursively explore from the neighbor.
                    dfs(neighbor_index)

        # --- Main Logic ---
        # Iterate through all cities from 0 to n-1.
        for i in range(n):
            # If we find a city that hasn't been visited yet...
            if not visited[i]:
                # ...it means we've found a new, unexplored province.
                # Increment the province count.
                province_count += 1
                # Start a DFS traversal from this city to find and mark
                # all cities belonging to this province.
                dfs(i)
                
        # After checking all cities, return the total count.
        return province_count
```

## Detailed Code Analysis

### Step 1: Initialization

```python
n = len(isConnected)
visited = [False] * n
province_count = 0
```

  - `n`: Stores the number of cities.
  - `visited = [False] * n`: Creates a list (acting as a boolean array) of size `n`, initialized to `False`. `visited[i] = True` will mean city `i` has been visited and assigned to a province.
  - `province_count = 0`: Initializes our final answer.

### Step 2: The `dfs` Helper Function

```python
def dfs(city_index):
    visited[city_index] = True
    for neighbor_index in range(n):
        if isConnected[city_index][neighbor_index] == 1 and not visited[neighbor_index]:
            dfs(neighbor_index)
```

  - This function is the core of the traversal. Its job is to find and mark all cities reachable from a given `city_index`.
  - **`visited[city_index] = True`**: The first action is crucial. We mark the current city as visited *before* exploring its neighbors to prevent getting stuck in infinite loops (e.g., A connects to B, B connects back to A).
  - **`for neighbor_index in range(n):`**: We iterate through all possible cities to check for connections.
  - **`if isConnected[...][...] == 1`**: We check the adjacency matrix to see if a direct connection exists between `city_index` and `neighbor_index`.
  - **`and not visited[neighbor_index]`**: We only proceed if the connected neighbor hasn't already been visited (either by a previous call in this DFS or by a DFS for a different province).
  - **`dfs(neighbor_index)`**: If both conditions are met, we make a recursive call to explore from that neighbor, extending our search through the connected component.

### Step 3: The Main Loop

```python
for i in range(n):
    if not visited[i]:
        province_count += 1
        dfs(i)
```

  - This loop ensures we check every single city.
  - **`if not visited[i]:`**: This is where we identify new provinces. If we encounter a city `i` that hasn't been visited by any previous `dfs` call, it must belong to a new, undiscovered connected component (province).
  - **`province_count += 1`**: We increment our counter because we've found a new province.
  - **`dfs(i)`**: We immediately start a DFS from this city `i`. This `dfs` call will recursively find and mark *all* cities belonging to this new province. Consequently, when the main `for` loop later reaches any other city in this same province, the `if not visited[...]` condition will be false, and we won't incorrectly count it as a *new* province.

## Step-by-Step Execution Trace

Let's trace the algorithm with `isConnected = [[1,1,0],[1,1,0],[0,0,1]]` with extreme detail.

### **Initial State:**

  - `n = 3`
  - `visited = [False, False, False]`
  - `province_count = 0`

-----

### **Main Loop - `i = 0`**

1.  Check `if not visited[0]`: `not False` is **True**. We found a new province.
2.  `province_count` becomes **1**.
3.  Call **`dfs(0)`**:
      - Mark `visited[0] = True`. `visited` is `[True, False, False]`.
      - Check neighbors of 0:
          - `neighbor = 0`: `isConnected[0][0]==1` but `visited[0]` is True. Skip.
          - `neighbor = 1`: `isConnected[0][1]==1` and `visited[1]` is False. Call **`dfs(1)`**.
              - Mark `visited[1] = True`. `visited` is `[True, True, False]`.
              - Check neighbors of 1:
                  - `neighbor = 0`: `isConnected[1][0]==1` but `visited[0]` is True. Skip.
                  - `neighbor = 1`: `isConnected[1][1]==1` but `visited[1]` is True. Skip.
                  - `neighbor = 2`: `isConnected[1][2]==0`. Skip.
              - `dfs(1)` finishes and returns.
          - `neighbor = 2`: `isConnected[0][2]==0`. Skip.
      - `dfs(0)` finishes and returns.

-----

### **Main Loop - `i = 1`**

1.  Check `if not visited[1]`: `not True` is **False**. This city is already part of Province 1. Skip.

-----

### **Main Loop - `i = 2`**

1.  Check `if not visited[2]`: `not False` is **True**. We found a new province.
2.  `province_count` becomes **2**.
3.  Call **`dfs(2)`**:
      - Mark `visited[2] = True`. `visited` is `[True, True, True]`.
      - Check neighbors of 2:
          - `neighbor = 0`: `isConnected[2][0]==0`. Skip.
          - `neighbor = 1`: `isConnected[2][1]==0`. Skip.
          - `neighbor = 2`: `isConnected[2][2]==1` but `visited[2]` is True. Skip.
      - `dfs(2)` finishes and returns.

-----

### **End of Algorithm**

  - The main `for` loop finishes.
  - The function returns the final `province_count`, which is **2**.

## Performance Analysis

### Time Complexity: O(n²)

  - Where `n` is the number of cities.
  - The main loop iterates `n` times.
  - The `dfs` function, in the worst case, might visit every city (`n`) and check every potential connection for that city (`n`). Although the `visited` array prevents infinite loops, the structure of checking every entry in the adjacency matrix within the `dfs` leads to `O(n²)` complexity overall. Each edge (`isConnected[i][j] == 1`) is essentially checked twice (once from `dfs(i)` and once from `dfs(j)`).

### Space Complexity: O(n)

  - The `visited` array requires `O(n)` space.
  - The recursion call stack for `dfs` can go up to `n` levels deep in the worst case (if the graph is a single line), requiring `O(n)` space.