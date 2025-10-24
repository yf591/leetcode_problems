# 841\. Keys and Rooms - Solution Explanation

## Problem Overview

You are given a scenario with `n` locked rooms, labeled from `0` to `n-1`. Only **Room 0 is initially unlocked**. Inside each room `i`, there is a list of keys, `rooms[i]`, where each key unlocks another room. The goal is to determine if it's possible to visit **every single room**, starting from Room 0.

**Key Definitions & Rules:**

  - You start in Room 0.
  - Entering a room allows you to collect all the keys inside it.
  - You can only enter a room if you have its corresponding key.
  - The objective is to see if all rooms are eventually reachable.

**Examples:**

```python
Input: rooms = [[1],[2],[3],[]]
Output: true
Explanation:
1. Start in Room 0 (unlocked). Find key 1.
2. Use key 1 to enter Room 1. Find key 2.
3. Use key 2 to enter Room 2. Find key 3.
4. Use key 3 to enter Room 3. Find no keys.
All rooms (0, 1, 2, 3) were visited.

Input: rooms = [[1,3],[3,0,1],[2],[0]]
Output: false
Explanation:
1. Start in Room 0. Find keys 1 and 3.
2. Visit Room 1. Find keys 3, 0, 1 (duplicates don't matter).
3. Visit Room 3. Find key 0.
We have keys 0, 1, 3. We never found key 2, so we cannot enter Room 2.
```

## Key Insights

### 1\. Modeling as a Graph

This problem can be perfectly modeled as a **directed graph**:

  - **Nodes**: Each room (`0` to `n-1`) is a node.
  - **Edges**: A key for room `j` found inside room `i` represents a directed edge from node `i` to node `j` (`i -> j`). This means if you are at room `i`, you can potentially reach room `j`.

### 2\. The Core Question: Connectivity

Once modeled as a graph, the problem becomes: **"Starting from node 0, can we reach all other nodes in the graph?"** This is a standard **graph reachability** or **connectivity** problem.

### 3\. Traversal Algorithms: DFS or BFS

To determine reachability, we need a graph traversal algorithm. Both **Depth-First Search (DFS)** and **Breadth-First Search (BFS)** are suitable:

  - **DFS**: Explores as far as possible down one path before backtracking. Can be implemented elegantly with recursion or an explicit stack.
  - **BFS**: Explores the graph layer by layer using a queue.

We will use an iterative DFS approach with an explicit stack for this explanation.

### 4\. Avoiding Cycles and Redundant Work: The `visited` Set

Graphs can have cycles. If we don't keep track of the rooms we've already visited, our traversal could get stuck in an infinite loop. Also, visiting the same room multiple times is inefficient. A **hash set** (`set` in Python) is the perfect data structure to store the indices of visited rooms, providing `O(1)` average time complexity for checking if a room has already been visited.

## Solution Approach

This solution implements a Depth-First Search (DFS) starting from Room 0. It uses an explicit stack to manage the order of rooms to visit and a set to keep track of visited rooms. After the traversal, it checks if the number of visited rooms equals the total number of rooms.

```python
from typing import List

class Solution:
    def canVisitAllRooms(self, rooms: List[List[int]]) -> bool:
        num_rooms = len(rooms)
        
        # A set to keep track of rooms we have already visited.
        visited = set()
        
        # A stack (using a list) to manage the rooms we need to explore.
        # We start by adding Room 0, the only initially accessible room.
        stack = [0]
        
        # Mark the starting room (Room 0) as visited.
        visited.add(0)
        
        # --- The DFS Traversal ---
        # Continue as long as there are rooms in our stack to explore.
        while stack:
            # Get the next room to visit from the top of the stack (LIFO).
            current_room = stack.pop()
            
            # Look at the keys (which lead to next rooms) found in the current room.
            for key_to_next_room in rooms[current_room]:
                # If the room unlocked by this key hasn't been visited yet...
                if key_to_next_room not in visited:
                    # ...mark it as visited...
                    visited.add(key_to_next_room)
                    # ...and add it to the stack to explore its keys later.
                    stack.append(key_to_next_room)
                    
        # --- Final Check ---
        # After the traversal, if the number of unique visited rooms
        # equals the total number of rooms, we could reach everywhere.
        return len(visited) == num_rooms
```

## Detailed Code Analysis

### Step 1: Initialization

```python
num_rooms = len(rooms)
visited = set()
stack = [0]
visited.add(0)
```

  - `num_rooms`: Stores the total number of rooms for the final comparison.
  - `visited = set()`: An empty set to store the indices of rooms we've successfully entered. Using a set gives us fast `O(1)` checks for `key not in visited`.
  - `stack = [0]`: A list used as a stack. We initialize it with `0` because Room 0 is our starting point.
  - `visited.add(0)`: We mark Room 0 as visited immediately since we start there.

### Step 2: The Main Traversal Loop

```python
while stack:
```

  - This loop is the heart of the DFS. It continues as long as there are rooms on our stack that we haven't fully explored (i.e., whose keys we haven't processed yet).

### Step 3: Processing a Room

```python
current_room = stack.pop()
```

  - `stack.pop()` removes and returns the last element added to the list (LIFO behavior). This gives us the index of the next room whose keys we need to examine.

### Step 4: Exploring Keys (Edges)

```python
for key_to_next_room in rooms[current_room]:
    if key_to_next_room not in visited:
        visited.add(key_to_next_room)
        stack.append(key_to_next_room)
```

  - We iterate through the list of `keys` found in the `current_room`. Each `key` is the index of a `next_room`.
  - **`if key_to_next_room not in visited:`**: This is the crucial check. We only care about keys that lead to rooms we haven't entered before.
  - **`visited.add(key_to_next_room)`**: If it's a new room, we immediately mark it as visited.
  - **`stack.append(key_to_next_room)`**: We add this newly discovered room to our stack. The `while` loop will eventually `pop` this room and explore *its* keys.

### Step 5: The Final Check

```python
return len(visited) == num_rooms
```

  - After the `while` loop finishes (meaning the stack is empty and we have explored every room reachable from Room 0), we perform the final check.
  - We compare the number of rooms in our `visited` set to the `num_rooms`. If they are equal, it means our traversal successfully reached every room, and we return `True`. Otherwise, we return `False`.

## Step-by-Step Execution Trace

Let's trace the algorithm with `rooms = [[1, 3], [3, 0, 1], [2], [0]]` with extreme detail.

### **Initial State:**

  - `num_rooms = 4`
  - `visited = {0}`
  - `stack = [0]`

-----

### **Main Loop - Iteration 1**

1.  `while stack:` (Stack is `[0]`). True.
2.  `current_room = stack.pop()` -\> `current_room = 0`. Stack is `[]`.
3.  Keys in `rooms[0]` are `[1, 3]`.
4.  **Process key `1`**:
      - `1 not in visited`? True.
      - `visited.add(1)`. `visited` is `{0, 1}`.
      - `stack.append(1)`. `stack` is `[1]`.
5.  **Process key `3`**:
      - `3 not in visited`? True.
      - `visited.add(3)`. `visited` is `{0, 1, 3}`.
      - `stack.append(3)`. `stack` is `[1, 3]`.

-----

### **Main Loop - Iteration 2**

1.  `while stack:` (Stack is `[1, 3]`). True.
2.  `current_room = stack.pop()` -\> `current_room = 3`. Stack is `[1]`.
3.  Keys in `rooms[3]` are `[0]`.
4.  **Process key `0`**:
      - `0 not in visited`? False (`0` is already in `visited`). Do nothing.

-----

### **Main Loop - Iteration 3**

1.  `while stack:` (Stack is `[1]`). True.
2.  `current_room = stack.pop()` -\> `current_room = 1`. Stack is `[]`.
3.  Keys in `rooms[1]` are `[3, 0, 1]`.
4.  **Process key `3`**:
      - `3 not in visited`? False. Do nothing.
5.  **Process key `0`**:
      - `0 not in visited`? False. Do nothing.
6.  **Process key `1`**:
      - `1 not in visited`? False. Do nothing.

-----

### **End of Traversal**

  - `while stack:` (Stack is `[]`). **False**. The loop terminates.

### **Final Check**

  - The code executes `return len(visited) == num_rooms`.
  - `visited` is `{0, 1, 3}`. `len(visited)` is 3.
  - `num_rooms` is 4.
  - `3 == 4` is **False**.
  - The function returns **`False`**, correctly indicating that Room 2 was unreachable.

## Performance Analysis

### Time Complexity: O(N + K)

  - Where `N` is the number of rooms and `K` is the total number of keys across all rooms.
  - The algorithm visits each room (node) at most once due to the `visited` set.
  - When visiting a room, it iterates through all the keys (edges) originating from that room.
  - Therefore, the total time complexity is proportional to the sum of the number of nodes and the number of edges.

### Space Complexity: O(N)

  - The space is dominated by the `visited` set and the `stack`.
  - In the worst case, the `visited` set can store up to `N` room indices.
  - In the worst case (e.g., a long chain of rooms), the `stack` can also grow up to size `N`.
  - Therefore, the space complexity is `O(N)`.