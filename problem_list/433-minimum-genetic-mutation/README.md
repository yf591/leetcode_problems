# 433\. Minimum Genetic Mutation - Solution Explanation

## Problem Overview

You are given a starting gene string `startGene`, an ending gene string `endGene`, and a `bank` of valid gene strings. The task is to find the **minimum number of mutations** to get from `startGene` to `endGene`.

**Key Rules & Constraints:**

  - **Mutation**: A single mutation is defined as changing one character in a gene string.
  - **Valid Mutation**: A mutation from `gene_A` to `gene_B` is only valid if the resulting `gene_B` is in the `bank`.
  - **Goal**: Find the shortest "path" of mutations from `startGene` to `endGene`.
  - **Output**: The number of steps in the shortest path. If no path exists, return `-1`.
  - **Note**: `startGene` is considered valid but may not be in the `bank`.

**Example:**

```python
Input: startGene = "AACCGGTT", endGene = "AAACGGTA", bank = ["AACCGGTA","AACCGCTA","AAACGGTA"]
Output: 2
Explanation:
1. "AACCGGTT" -> "AACCGGTA" (1 mutation, "AACCGGTA" is in the bank)
2. "AACCGGTA" -> "AAACGGTA" (1 mutation, "AAACGGTA" is in the bank)
This is a path of 2 steps.
```

## Deep Dive: What is Graph BFS? 🧠

**BFS (Breadth-First Search)** is a fundamental algorithm for traversing a graph or tree.

**The Core Idea:**
BFS explores the graph **level by level**. It's like dropping a pebble in a pond:

  - The pebble is your **start node**.
  - **Wave 1 (Level 1)**: The BFS visits all nodes 1 step away from the start.
  - **Wave 2 (Level 2)**: It then visits all *new* nodes 2 steps away.
  - **Wave 3 (Level 3)**: It then visits all *new* nodes 3 steps away, and so on.

**How it Works (The Tools):**
BFS uses two key data structures to manage this exploration:

1.  **A Queue (First-In, First-Out)**: This is like a "to-do list" of nodes to visit. When we discover a neighbor, we add it to the *back* of the queue. When we're ready to explore a new node, we take it from the *front* of the queue. This ensures we process all of Level 1 before moving to Level 2.
2.  **A `visited` Set**: This is our "memory." A graph can have cycles. To prevent getting stuck in an infinite loop (e.g., A -\> B -\> A -\> B...) and to avoid doing redundant work, we mark each node as `visited` as soon as we add it to the queue. We never add a node to the queue if it's already in the `visited` set.

**Why BFS is Perfect for This Problem:**
The problem asks for the **"minimum number of mutations"** (the shortest path). Because BFS explores layer by layer, the **first time** it reaches the `endGene`, it is **guaranteed** to have found the path with the fewest steps.

## Key Insights

### 1\. The Implicit Graph

This problem doesn't give you a graph, but the rules *imply* one:

  - **Nodes**: Every gene in the `bank` plus the `startGene`.
  - **Edges**: A directed edge exists between two genes (`gene_A` and `gene_B`) if they are one mutation apart *and* `gene_B` is in the `bank`.

### 2\. The `bank` as a `set`

We will need to check if a gene is in the `bank` many times. Checking `if gene in my_list` is slow (`O(n)`). If we convert the `bank` (a list) into a `set` at the beginning, checking `if gene in my_set` is extremely fast (`O(1)` on average).

### 3\. Finding Neighbors Efficiently

For any `current_gene`, how do we find its valid neighbors?

  - **Slow way**: Iterate through the entire `bank_set` and check every gene to see if it's one mutation away. This is `O(BankSize)`.
  - **Fast way**: *Generate* all possible 1-character mutations of the `current_gene` and check if that mutation is in the `bank_set`.
      - A gene has 8 characters. Each can be 'A', 'C', 'G', or 'T'.
      - For each of the 8 positions, we can try 3 *other* characters.
      - This means there are only `8 * 3 = 24` possible neighbors to check.
      - Checking these 24 possibilities against the `bank_set` is much faster than iterating through the whole bank.

## Solution Approach

This solution implements a BFS to find the shortest path from `startGene` to `endGene`. It converts the `bank` to a `set` for fast lookups. It uses a queue to store `(gene, step_count)` tuples and a `visited` set to avoid cycles.

```python
import collections
from typing import List

class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        
        # --- Step 1: Initialization and Edge Cases ---
        
        # Convert the bank to a set for efficient O(1) lookups.
        bank_set = set(bank)
        
        # If the endGene isn't even in the bank, it's impossible to reach.
        if endGene not in bank_set:
            return -1
            
        # Initialize the queue for BFS. We store tuples of (gene_string, steps_so_far).
        queue = collections.deque([(startGene, 0)])
        
        # Keep track of genes we've already visited to avoid cycles.
        visited = {startGene}
        
        possible_chars = "ACGT"
        
        # --- Step 2: Perform BFS Traversal ---
        
        while queue:
            # Get the next gene and its step count from the front of the queue.
            current_gene, steps = queue.popleft()
            
            # --- Step 3: Check for Goal ---
            if current_gene == endGene:
                # We found the shortest path!
                return steps
                
            # --- Step 4: Find Valid Neighbors (Generate and Check) ---
            
            # Iterate through each character position in the gene.
            for i in range(len(current_gene)):
                original_char = current_gene[i]
                
                # For each position, try changing it to each possible gene character.
                for char in possible_chars:
                    if original_char == char:
                        continue
                    
                    # Create the new mutation.
                    new_gene = current_gene[:i] + char + current_gene[i+1:]
                    
                    # --- Step 5: Check if the new gene is a valid next step ---
                    if new_gene in bank_set and new_gene not in visited:
                        # If it is, mark it as visited and add it to the queue
                        # with an incremented step count.
                        visited.add(new_gene)
                        queue.append((new_gene, steps + 1))
                        
        # --- Step 6: No Path Found ---
        # If the queue becomes empty and we never reached the endGene, it's impossible.
        return -1
```

## Detailed Code Analysis

### Step 1: Initialization

```python
bank_set = set(bank)
if endGene not in bank_set:
    return -1
queue = collections.deque([(startGene, 0)])
visited = {startGene}
```

  - `bank_set = set(bank)`: This is a crucial `O(N)` optimization (where `N` is the length of `bank`). It converts the list into a hash set.
  - `if endGene not in bank_set:`: A vital edge case check. If the destination isn't a valid mutation, we can't get there.
  - `queue = collections.deque([(startGene, 0)])`: We use a `deque` (a fast queue) and add our starting point. The tuple `(startGene, 0)` means we are at `startGene` and have taken `0` steps.
  - `visited = {startGene}`: We immediately mark the `startGene` as visited so we don't accidentally come back to it.

### Step 2: The Main BFS Loop

```python
while queue:
    current_gene, steps = queue.popleft()
```

  - This loop runs as long as there are nodes to explore.
  - `queue.popleft()`: This is the FIFO (First-In, First-Out) operation. It gets the "oldest" item from the queue, which is the next node in the current "level" of our search.

### Step 3: Goal Check

```python
if current_gene == endGene:
    return steps
```

  - The first thing we do is check if the node we just dequeued is our target. Because this is a BFS, the first time we find `endGene`, we are *guaranteed* to have found it via the shortest possible path. We can immediately return the `steps` it took to get here.

### Step 4: Neighbor Generation

```python
for i in range(len(current_gene)):
    ...
    for char in "ACGT":
        ...
        new_gene = current_gene[:i] + char + current_gene[i+1:]
```

  - This is the "Generate and Check" strategy. The outer loop iterates 8 times (for each character index).
  - The inner loop iterates 4 times (for 'A', 'C', 'G', 'T').
  - `new_gene = ...`: This line efficiently creates a new string representing a 1-character mutation.

### Step 5: Neighbor Validation

```python
if new_gene in bank_set and new_gene not in visited:
    visited.add(new_gene)
    queue.append((new_gene, steps + 1))
```

  - This is the filter for our generated neighbors. A `new_gene` is a valid next step *only if* it meets both conditions:
    1.  `new_gene in bank_set`: It must be a valid gene in the provided bank.
    2.  `new_gene not in visited`: We must not have processed this gene before.
  - If both are true, we add the `new_gene` to our `visited` set and enqueue it for the *next* level of the search, incrementing the step count (`steps + 1`).

### Step 6: No Path Found

```python
return -1
```

  - If the `while` loop finishes, it means the `queue` became empty. We have explored every reachable gene and we never found the `endGene`. Therefore, no path exists, and we return `-1`.

## Step-by-Step Execution Trace

Let's trace `start="AAC", end="GGC", bank=["AGC", "GGC"]` (a simplified 3-char example).

### **Initial State:**

  - `bank_set = {"AGC", "GGC"}`
  - `endGene` ("GGC") is in `bank_set`.
  - `queue = deque([("AAC", 0)])`
  - `visited = {"AAC"}`

-----

### **BFS Loop - Iteration 1 (Level 0)**

1.  Dequeue `("AAC", 0)`. `current_gene="AAC"`, `steps=0`.
2.  `current_gene != endGene`.
3.  **Find Neighbors of "AAC"**:
      - Try mutating `i=0` ('A'):
          - `"CAC"`: Not in `bank_set`.
          - `"GAC"`: Not in `bank_set`.
          - `"TAC"`: Not in `bank_set`.
      - Try mutating `i=1` ('A'):
          - `"ACC"`: Not in `bank_set`.
          - `"AGC"`: **In `bank_set`** and **not in `visited`**.
              - `visited.add("AGC")`. `visited` is `{"AAC", "AGC"}`.
              - `queue.append(("AGC", 1))`.
          - `"ATC"`: Not in `bank_set`.
      - Try mutating `i=2` ('C'):
          - `"AAA"`: Not in `bank_set`.
          - `"AAG"`: Not in `bank_set`.
          - `"AAT"`: Not in `bank_set`.
4.  **Queue state**: `deque([("AGC", 1)])`

-----

### **BFS Loop - Iteration 2 (Level 1)**

1.  Dequeue `("AGC", 1)`. `current_gene="AGC"`, `steps=1`.
2.  `current_gene != endGene`.
3.  **Find Neighbors of "AGC"**:
      - Try mutating `i=0` ('A'):
          - `"CGC"`: Not in `bank_set`.
          - `"GGC"`: **In `bank_set`** and **not in `visited`**.
              - `visited.add("GGC")`. `visited` is `{"AAC", "AGC", "GGC"}`.
              - `queue.append(("GGC", 2))`.
          - ... (other mutations fail) ...
4.  **Queue state**: `deque([("GGC", 2)])`

-----

### **BFS Loop - Iteration 3 (Level 2)**

1.  Dequeue `("GGC", 2)`. `current_gene="GGC"`, `steps=2`.
2.  `current_gene == endGene`? **True\!**
3.  **Return `steps` (which is 2)**.

The algorithm terminates and returns `2`.

## Performance Analysis

### Time Complexity: O(L² \* N + M)

  - `M` = length of `bank`, `N` = length of `startGene` (which is 8), `A` = alphabet size (4).
  - This is a bit tricky. Let's redefine. `M` = number of words in `bank`, `L` = length of a gene (8).
  - **Preprocessing**: Creating `bank_set` takes `O(M * L)` time.
  - **BFS**:
      - In the worst case, we visit every node in the `bank`. So, `M` nodes.
      - For each node, we generate all `L * A` (or `8 * 3 = 24`) possible mutations. This takes `O(L)` time to create the string. Total: `O(L*A*L) = O(L^2)`.
      - Checking `new_gene in bank_set` is `O(L)` (to hash the string).
      - So, processing one node is `O(L^2 * A)` (using Python string slicing) or `O(L * A)` (if we build char list). Let's assume `O(L^2)`.
      - Total BFS time: `O(M * L^2)`.
  - **Total Time**: `O(M*L + M*L^2)`. Given `L=8` and `A=4`, `L^2` is a small constant (64). The complexity is effectively dominated by the size of the bank, `M`. A simpler way is `O(M * L^2)`.

\*Self-correction: String slicing in Python `s[:i] + c + s[i+1:]` is `O(L)`. So generating one new gene is `O(L)`. Trying all `L * A` mutations takes `O(L*L*A)`. Checking in the set is `O(L)`. This is getting complex. Let's simplify: `N` = num nodes (`M`), `K` = neighbors per node (`L*A`). Time is `O(V+E) = O(N*K) = O(M * L * A)`. Ah, but string hashing and comparison is `O(L)`.
*Let's try again:*

  - `M` = `len(bank)`, `L` = `len(startGene)` (8)
  - Build `bank_set`: `O(M*L)`
  - BFS:
      - Queue can hold at most `M` items.
      - `while` loop runs at most `M` times.
      - Inside `while`: `popleft` is `O(1)`.
      - Neighbor generation loop: `L * A` iterations.
      - Inside neighbor loop: Slicing is `O(L)`, `in bank_set` is `O(L)`, `visited.add` is `O(L)`, `queue.append` is `O(1)`.
      - Total time: `O(M*L + M * (L * A * L)) = O(M*L^2)`. Since `L=8` is a small constant, this is often just called **`O(M)`**.

### Space Complexity: O(M \* L)

  - `bank_set` stores `M` words of length `L`. Total `O(M * L)`.
  - `queue` in the worst case stores `M` items. Each item is a tuple `(string, int)`, so `O(M * L)`.
  - `visited` set also stores `M` strings of length `L`. Total `O(M * L)`.
  - The overall space is dominated by the storage of the genes.