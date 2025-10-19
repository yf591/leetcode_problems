# 207\. Course Schedule - Solution Explanation

## Problem Overview

You are given a total number of courses (`numCourses`) and a list of prerequisites. Each prerequisite is a pair `[a, b]`, meaning you must complete course `b` before you can take course `a`. The task is to determine if it is possible to finish **all** courses.

**Key Definitions:**

  - **Prerequisite**: A condition that must be met before something else can happen.
  - **The Goal**: Return `True` if a valid order of taking courses exists to finish everything, `False` otherwise.

**The Underlying Problem:**
This is fundamentally a problem about **dependencies**. The prerequisites define a directed graph where courses are nodes and a prerequisite `[a, b]` creates a directed edge from `b` to `a` (`b -> a`). The question "Can you finish all courses?" is equivalent to asking: **"Does this dependency graph contain a cycle?"** If there's a cycle (e.g., course 0 needs 1, and course 1 needs 0), it's impossible to satisfy the prerequisites.

**Examples:**

```python
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: You must take course 0 before course 1. This is possible. Graph: 0 -> 1.

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: To take 1 you need 0, and to take 0 you need 1. This is a cycle, impossible. Graph: 0 -> 1 and 1 -> 0.
```

## Key Insights

### 1\. Representing Dependencies as a Graph

The first step is to model the problem as a directed graph:

  - **Nodes**: Each course from `0` to `numCourses - 1`.
  - **Edges**: A prerequisite `[a, b]` means there's a directed edge `b -> a` (finish `b`, then you can take `a`).
    We can use an **adjacency list** (a dictionary mapping a course to a list of courses that depend on it) to represent this graph efficiently.

### 2\. Detecting Cycles: Topological Sort

The core problem is detecting cycles in a directed graph. A standard algorithm for this is **Topological Sort**. A topological sort finds a linear ordering of nodes such that for every directed edge `u -> v`, node `u` comes before node `v` in the ordering.

  - A topological sort is only possible if and only if the graph has **no directed cycles**.
  - If we can successfully perform a topological sort and include all `numCourses` in the sorted order, then there is no cycle, and we can finish all courses.

### 3\. Kahn's Algorithm (BFS-based Topological Sort)

Kahn's algorithm is an intuitive way to perform a topological sort using Breadth-First Search principles. It works based on **in-degrees**.

  - **In-degree**: The in-degree of a node (course) is the number of incoming edges it has (i.e., the number of prerequisites it requires).
  - **The Logic**:
    1.  You can only start with courses that have an in-degree of 0 (no prerequisites).
    2.  Put all these starting courses into a queue.
    3.  While the queue is not empty:
        a.  Dequeue a course `u`. This is like "taking" the course.
        b.  For every course `v` that had `u` as a prerequisite (`u -> v`), decrement the in-degree of `v`.
        c.  If the in-degree of `v` becomes 0, it means all its prerequisites are now met, so enqueue `v`.
    4.  Keep track of how many courses you successfully dequeued ("took"). If this final count equals `numCourses`, then a valid topological sort was possible (no cycle). Otherwise, a cycle must have prevented some courses from ever reaching an in-degree of 0.

## Solution Approach

This solution implements Kahn's algorithm. It first builds the graph representation (adjacency list) and calculates the in-degrees. Then, it uses a queue to process courses with no unmet prerequisites, decrementing the in-degrees of dependent courses until either all courses are processed or no more courses can be added to the queue (indicating a cycle).

```python
import collections
from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        
        # --- Step 1: Build the graph and calculate in-degrees ---
        graph = collections.defaultdict(list)
        in_degree = [0] * numCourses
        
        for course, prereq in prerequisites:
            # Add edge: prereq -> course
            graph[prereq].append(course)
            # Increment in-degree for the course that has a prerequisite
            in_degree[course] += 1
            
        # --- Step 2: Initialize the queue ---
        # Find all courses with an initial in-degree of 0
        queue = collections.deque([i for i in range(numCourses) if in_degree[i] == 0])
        
        # --- Step 3: Initialize the count of completed courses ---
        courses_taken = 0
        
        # --- Step 4: Process the queue (Kahn's Algorithm) ---
        while queue:
            # Take a course whose prerequisites are all met
            course = queue.popleft()
            courses_taken += 1
            
            # For each neighbor (courses that depend on this one)...
            for neighbor in graph[course]:
                # ...reduce their in-degree because we've completed a prerequisite.
                in_degree[neighbor] -= 1
                # If this neighbor now has all its prerequisites met...
                if in_degree[neighbor] == 0:
                    # ...add it to the queue to be taken later.
                    queue.append(neighbor)
                    
        # --- Step 5: Check if all courses were completed ---
        # If courses_taken == numCourses, it means there was no cycle.
        return courses_taken == numCourses
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
  - `graph[prereq].append(course)`: Adds a directed edge `prereq -> course`.
  - `in_degree[course] += 1`: Increments the count of prerequisites for `course`.

### Step 2: Initializing the Queue

```python
queue = collections.deque([i for i in range(numCourses) if in_degree[i] == 0])
```

  - `collections.deque` provides an efficient queue.
  - This line uses a list comprehension to find all course indices `i` where the `in_degree[i]` is currently `0`. These are the courses we can take immediately.
  - These initial courses are added to the queue.

### Step 3: Initializing the Counter

```python
courses_taken = 0
```

  - This variable will count how many courses we successfully process (dequeue).

### Step 4: Processing the Queue (The BFS Core)

```python
while queue:
    course = queue.popleft()
    courses_taken += 1
    
    for neighbor in graph[course]:
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)
```

  - **`while queue:`**: The loop continues as long as there are courses ready to be taken (whose prerequisites are met).
  - **`course = queue.popleft()`**: We dequeue a course. This simulates "taking" the course.
  - **`courses_taken += 1`**: We increment our count of completed courses.
  - **`for neighbor in graph[course]:`**: We look at all courses (`neighbor`) that depend on the `course` we just took.
  - **`in_degree[neighbor] -= 1`**: For each `neighbor`, we decrement its in-degree because one of its prerequisites is now satisfied.
  - **`if in_degree[neighbor] == 0:`**: If decrementing brings the `neighbor`'s in-degree to zero, it means *all* of its prerequisites are now met.
  - **`queue.append(neighbor)`**: We add this newly available `neighbor` course to the queue, so it can be "taken" in a future iteration.

### Step 5: The Final Check

```python
return courses_taken == numCourses
```

  - After the `while` loop finishes, we check our counter.
  - If `courses_taken` equals `numCourses`, it means we were able to process every single course. This implies there was no cycle in the dependency graph.
  - If `courses_taken` is less than `numCourses`, it means the loop terminated because the queue became empty, but there were still courses with non-zero in-degrees. This only happens if there's a cycle, preventing those courses' in-degrees from ever reaching zero.

## Step-by-Step Execution Trace

Let's trace the algorithm with the cycle example: `numCourses = 2`, `prerequisites = [[1,0], [0,1]]`.

1.  **Build Graph & In-Degrees**:
      - `graph`: `{ 0: [1], 1: [0] }`
      - `in_degree`: `[1, 1]` (Course 0 needs 1 prereq, Course 1 needs 1 prereq)
2.  **Initialize Queue**:
      - Are there any courses with `in_degree == 0`? No.
      - `queue` starts as `deque([])`.
3.  **Initialize Counter**: `courses_taken = 0`.
4.  **Process Queue**:
      - `while queue:` The queue is empty. The loop **never runs**.
5.  **Final Check**:
      - `return courses_taken == numCourses`
      - `return 0 == 2` -\> **`False`**.

The algorithm correctly detects the cycle and returns `False`.

Let's trace the success example: `numCourses = 2`, `prerequisites = [[1,0]]`.

1.  **Build Graph & In-Degrees**:
      - `graph`: `{ 0: [1] }`
      - `in_degree`: `[0, 1]` (Course 0 needs 0 prereqs, Course 1 needs 1 prereq)
2.  **Initialize Queue**:
      - Find courses with `in_degree == 0`. Only Course 0.
      - `queue` starts as `deque([0])`.
3.  **Initialize Counter**: `courses_taken = 0`.
4.  **Process Queue**:
      - **Loop 1**:
          - `queue` is not empty.
          - `course = queue.popleft()` -\> `course = 0`.
          - `courses_taken` becomes `1`.
          - Neighbors of course 0: `[1]`.
          - For `neighbor = 1`:
              - `in_degree[1]` becomes `1 - 1 = 0`.
              - Since `in_degree[1]` is now 0, `queue.append(1)`.
          - `queue` is now `deque([1])`.
      - **Loop 2**:
          - `queue` is not empty.
          - `course = queue.popleft()` -\> `course = 1`.
          - `courses_taken` becomes `2`.
          - Neighbors of course 1: `[]`. The inner loop does nothing.
          - `queue` is now `deque([])`.
      - The `while` loop terminates.
5.  **Final Check**:
      - `return courses_taken == numCourses`
      - `return 2 == 2` -\> **`True`**.

The algorithm correctly determines it's possible and returns `True`.

## Performance Analysis

### Time Complexity: O(V + E)

  - Where `V` is the number of courses (`numCourses`) and `E` is the number of prerequisites.
  - Building the graph and calculating in-degrees takes `O(E)` time.
  - Initializing the queue takes `O(V)` time.
  - The main `while` loop processes each course (vertex) and each prerequisite (edge) exactly once. Dequeueing/Enqueuing is `O(1)`.
  - The total time is `O(V + E)`.

### Space Complexity: O(V + E)

  - The `graph` (adjacency list) can store up to `E` edges and `V` vertices.
  - The `in_degree` array takes `O(V)` space.
  - The `queue` can, in the worst case, hold up to `V` vertices.
  - The total space is `O(V + E)`.