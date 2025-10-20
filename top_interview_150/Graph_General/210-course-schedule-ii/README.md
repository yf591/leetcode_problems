# 210\. Course Schedule II - Solution Explanation

## Problem Overview

You are given a total number of courses (`numCourses`) and a list of prerequisites. Each prerequisite is a pair `[a, b]`, meaning you must complete course `b` before you can take course `a`. The task is to return **one possible order** in which you can take all the courses to satisfy the prerequisites.

**Key Definitions & Rules:**

  - **Prerequisite**: `[a, b]` implies `b` must be finished before `a`.
  - **Output**: A list representing a valid sequence of courses. If multiple valid sequences exist, any one is acceptable.
  - **Impossibility**: If it's impossible to finish all courses (due to a circular dependency/cycle), return an empty list `[]`.

**Examples:**

```python
Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
Explanation: Take course 0, then course 1.

Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,2,1,3] # or [0,1,2,3]
Explanation: 0 must be taken first. Then 1 and 2 can be taken. Finally, 3 can be taken.

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: []
Explanation: A cycle exists, impossible to finish.
```

## Key Insights

### 1\. Graph Representation (Same as Course Schedule I)

This problem is fundamentally about dependencies, which can be modeled as a **directed graph**:

  - **Nodes**: Each course from `0` to `numCourses - 1`.
  - **Edges**: A prerequisite `[a, b]` represents a directed edge **`b -> a`** (meaning `b` must happen before `a`).
    We will use an **adjacency list** to store the graph, where `graph[b]` contains a list of courses that have `b` as a prerequisite.

### 2\. The Goal: Topological Sort

Finding a valid order to take the courses is exactly the definition of a **Topological Sort**. A topological sort provides a linear ordering of nodes in a directed graph such that for every directed edge `u -> v`, node `u` comes before node `v` in the ordering.

  - A topological sort is only possible if the graph is a **Directed Acyclic Graph (DAG)**, meaning it has no cycles.
  - If the graph contains a cycle, a topological sort is impossible, which matches the problem's requirement to return an empty list in that case.

### 3\. Kahn's Algorithm (BFS-based Topological Sort)

Kahn's algorithm is an efficient and intuitive way to find a topological sort. It works by tracking the **in-degree** of each node (the number of prerequisites).

  - **The Logic**:
    1.  Start with the courses that have an in-degree of 0 (no prerequisites). These can be taken first.
    2.  Put these courses into a queue.
    3.  Maintain a list to store the final sorted order.
    4.  While the queue is not empty:
        a.  Dequeue a course `u`. This simulates "taking" the course. Add it to the sorted order list.
        b.  For every neighbor `v` of `u` (i.e., courses that had `u` as a prerequisite), decrease the in-degree of `v`. This signifies that one of its prerequisites has been met.
        c.  If the in-degree of `v` drops to 0, it means all its prerequisites are now satisfied, so enqueue `v`.
    5.  After the loop, if the number of courses in our sorted order list equals `numCourses`, we have successfully found a valid order. Otherwise, a cycle prevented some courses from being processed, and we return an empty list.

## Solution Approach

This solution implements Kahn's algorithm. It builds the graph, calculates in-degrees, uses a queue to process courses, and builds the topological order list. Finally, it checks if all courses were included in the order.

```python
import collections
from typing import List

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        
        # --- Step 1: Build the graph and calculate in-degrees ---
        # graph: maps prerequisite -> list of courses that depend on it
        # in_degree: counts how many prerequisites each course has
        graph = collections.defaultdict(list)
        in_degree = [0] * numCourses
        
        for course, prereq in prerequisites:
            graph[prereq].append(course) # Add edge prereq -> course
            in_degree[course] += 1       # Increment in-degree of 'course'
            
        # --- Step 2: Initialize the queue ---
        # Add all courses with 0 prerequisites to the queue
        queue = collections.deque([i for i in range(numCourses) if in_degree[i] == 0])
        
        # --- Step 3: Initialize the result list ---
        result_order = []
        
        # --- Step 4: Process the queue (Kahn's Algorithm) ---
        while queue:
            # Take a course whose prerequisites are met
            course = queue.popleft()
            # Add it to the result order
            result_order.append(course)
            
            # Reduce the in-degree of its neighbors
            for neighbor in graph[course]:
                in_degree[neighbor] -= 1
                # If a neighbor now has 0 prerequisites, add it to the queue
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        # --- Step 5: Check if a valid order was found ---
        if len(result_order) == numCourses:
            return result_order
        else:
            # If the length doesn't match, it means there was a cycle
            return []
```

## Detailed Code Analysis

### Step 1: Building the Graph and In-Degrees

```python
graph = collections.defaultdict(list)
in_degree = [0] * numCourses

for course, prereq in prerequisites:
    graph[prereq].append(course)
    in_degree[course] += 1
```

  - `graph = collections.defaultdict(list)`: Creates our adjacency list. `graph[X]` will give a list of courses that have `X` as a prerequisite.
  - `in_degree = [0] * numCourses`: Creates an array to store the in-degree count for each course, initialized to zero.
  - The loop iterates through each prerequisite pair `[course, prereq]`.
  - `graph[prereq].append(course)`: Adds a directed edge `prereq -> course`. This means `course` depends on `prereq`.
  - `in_degree[course] += 1`: Increments the count of prerequisites for `course`.

### Step 2: Initializing the Queue

```python
queue = collections.deque([i for i in range(numCourses) if in_degree[i] == 0])
```

  - `collections.deque` provides an efficient queue.
  - This line uses a list comprehension to find all course indices `i` where the `in_degree[i]` is currently `0`. These are the courses we can take immediately.
  - These initial courses are added to the queue.

### Step 3: Initializing the Result List

```python
result_order = []
```

  - This empty list will be populated with the courses in a valid topological order as we process them.

### Step 4: Processing the Queue (The BFS Core)

```python
while queue:
    course = queue.popleft()
    result_order.append(course)
    
    for neighbor in graph[course]:
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)
```

  - **`while queue:`**: The loop continues as long as there are courses ready to be taken (whose prerequisites are met).
  - **`course = queue.popleft()`**: We dequeue a course. This simulates "taking" the course.
  - **`result_order.append(course)`**: **This is the key difference from Course Schedule I.** We add the course we just "took" to our result list.
  - **`for neighbor in graph[course]:`**: We look at all courses (`neighbor`) that depend on the `course` we just took.
  - **`in_degree[neighbor] -= 1`**: For each `neighbor`, we decrement its in-degree because one of its prerequisites is now satisfied.
  - **`if in_degree[neighbor] == 0:`**: If decrementing brings the `neighbor`'s in-degree to zero, it means *all* of its prerequisites are now met.
  - **`queue.append(neighbor)`**: We add this newly available `neighbor` course to the queue, so it can be "taken" in a future iteration.

### Step 5: The Final Check

```python
if len(result_order) == numCourses:
    return result_order
else:
    return []
```

  - After the `while` loop finishes, we check if we were able to process all courses.
  - If `len(result_order)` equals `numCourses`, it means we successfully added every course to our list, implying a valid topological sort exists (no cycle). We return the `result_order`.
  - If the length is less than `numCourses`, it means the loop terminated because the queue became empty, but there were still courses with non-zero in-degrees. This only happens if there's a cycle. We return an empty list `[]`.

## Step-by-Step Execution Trace

Let's trace `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`.

1.  **Build Graph & In-Degrees**:
      - `graph`: `{ 0: [1, 2], 1: [3], 2: [3] }`
      - `in_degree`: `[0, 1, 1, 2]` (Course 0:0, 1:1, 2:1, 3:2)
2.  **Initialize Queue**:
      - Find courses with `in_degree == 0`. Only Course 0.
      - `queue` starts as `deque([0])`.
3.  **Initialize Result**: `result_order = []`.
4.  **Process Queue**:

| `queue` (start) | Dequeued `course` | `result_order` (after append) | Neighbors | Actions on Neighbors (`in_degree`, `queue`) | `queue` (end) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `[0]` | 0 | `[0]` | `[1, 2]` | `in_degree[1]=0`, `in_degree[2]=0`. Enqueue 1, Enqueue 2. | `[1, 2]` |
| `[1, 2]` | 1 | `[0, 1]` | `[3]` | `in_degree[3]=1`. | `[2]` |
| `[2]` | 2 | `[0, 1, 2]` | `[3]` | `in_degree[3]=0`. Enqueue 3. | `[3]` |
| `[3]` | 3 | `[0, 1, 2, 3]` | `[]` | - | `[]` |

5.  **Final Check**:
      - `len(result_order)` is 4. `numCourses` is 4. `4 == 4` is **True**.
      - Return `result_order`: `[0, 1, 2, 3]`. (Note: If 2 was dequeued before 1, the result would be `[0, 2, 1, 3]`, which is also valid).

## Performance Analysis

### Time Complexity: O(V + E)

  - Where `V` is the number of courses (`numCourses`) and `E` is the number of prerequisites.
  - Building the graph and calculating in-degrees takes `O(E + V)` time.
  - Initializing the queue takes `O(V)` time.
  - The main `while` loop processes each course (vertex) and each prerequisite (edge) exactly once. Dequeueing/Enqueuing is `O(1)`.
  - The total time is `O(V + E)`.

### Space Complexity: O(V + E)

  - The `graph` (adjacency list) can store up to `E` edges and `V` vertices.
  - The `in_degree` array takes `O(V)` space.
  - The `queue` can, in the worst case, hold up to `V` vertices.
  - The `result_order` list takes `O(V)` space.
  - The total space is `O(V + E)`.