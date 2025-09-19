# 649\. Dota2 Senate - Solution Explanation

## Problem Overview

You are asked to predict the winner of a voting game in the Dota2 senate. The senate consists of two parties: **Radiant** (`R`) and **Dire** (`D`).

**The Game Rules:**

1.  **Turn-Based**: The senators take turns voting in the order they appear in the input string (e.g., in `"RD"`, the `R` senator goes first).
2.  **Circular Rounds**: After the last senator in the initial list votes, the first senator who is still able to vote starts the next round.
3.  **Voting Power**: On a senator's turn, they can do one of two things:
    a.  **Ban an Opponent**: Permanently remove one senator from the opposing party.
    b.  **Declare Victory**: If all senators who can still vote are from their own party, they can declare victory.
4.  **Optimal Strategy**: Every senator is smart. They will always make the best possible move for their party.

The goal is to determine which party will win.

## Key Insights

### The Optimal Greedy Strategy

The problem states that every senator plays optimally. What is the best move? To eliminate the opposition's voting power as quickly as possible. This means a senator should always ban the **opponent who is next in line to vote**. Banning an opponent who is far down the queue is less effective than banning one who is about to act against your party. This **greedy** choice is the key insight.

### Modeling the Turn Order with Queues

The game is round-based and senators act in a "first-come, first-served" manner. This is a perfect use case for the **Queue** data structure (First-In, First-Out).

Since we need to know which Radiant senator is next *and* which Dire senator is next, the best approach is to use **two separate queues**: one for the Radiant senators and one for the Dire.

Crucially, we can't just store the letters 'R' and 'D' in the queues. We need to store their **original indices** from the input string to know who gets to act first in any given confrontation.

## Solution Approach

This solution implements the greedy, two-queue strategy. We populate two queues with the initial indices of the Radiant and Dire senators. Then, we simulate the game round by round by comparing the indices at the front of each queue.

```python
import collections
from typing import List

class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        n = len(senate)
        
        # 1. Create two queues to store the indices of senators from each party.
        #    List comprehensions make this initialization clean and fast.
        radiant_q = collections.deque([i for i, party in enumerate(senate) if party == 'R'])
        dire_q = collections.deque([i for i, party in enumerate(senate) if party == 'D'])
        
        # 2. Simulate the rounds as long as both parties have senators.
        while radiant_q and dire_q:
            # 3. Get the next senator from the front of each queue.
            r_idx = radiant_q.popleft()
            d_idx = dire_q.popleft()
            
            # 4. The senator with the smaller index acts first and bans the other.
            if r_idx < d_idx:
                # The Radiant senator wins this turn. They get to vote again in the next round.
                # We add 'n' to their index to place them at the end of the next round's queue.
                radiant_q.append(r_idx + n)
            else:
                # The Dire senator wins this turn.
                dire_q.append(d_idx + n)
        
        # 5. The loop ends when one queue is empty. The non-empty queue's party wins.
        return "Radiant" if radiant_q else "Dire"
```

## Detailed Code Analysis

### Step 1: Queue Initialization

```python
n = len(senate)
radiant_q = collections.deque([i for i, party in enumerate(senate) if party == 'R'])
dire_q = collections.deque([i for i, party in enumerate(senate) if party == 'D'])
```

  - We use `collections.deque` for a highly efficient queue.
  - We iterate through the input `senate` string with `enumerate` to get both the index `i` and the party `party`.
  - We populate `radiant_q` with the indices of all 'R' senators and `dire_q` with the indices of all 'D' senators. This correctly sets up the initial turn order for both parties.

### Step 2: The Simulation Loop

```python
while radiant_q and dire_q:
```

  - The game continues as long as both parties still have at least one senator with the right to vote. The loop terminates as soon as one party is eliminated.

### Step 3: The Confrontation

```python
r_idx = radiant_q.popleft()
d_idx = dire_q.popleft()
```

  - `popleft()` removes and returns the senator from the **front** of the queue. These are the two senators, one from each party, who are next in line to vote.

### Step 4: The Greedy Choice and Re-queuing

```python
if r_idx < d_idx:
    radiant_q.append(r_idx + n)
else:
    dire_q.append(d_idx + n)
```

  - **`if r_idx < d_idx:`**: This is the core of the greedy strategy. The senator with the smaller original index appeared earlier in the turn order for the current round, so they get to exercise their right to ban.
  - **The Banning**: The losing senator (the one with the larger index) is simply not added back to their queue. They are now permanently banned.
  - **`append(r_idx + n)`**: This is the clever part. The winning senator gets to vote again, but only in the *next* round. By adding `n` (the total number of initial senators) to their index, we effectively place them at the back of the line for the next round, while still preserving their relative order against other winners from the same round.

### Step 5: Declaring the Winner

```python
return "Radiant" if radiant_q else "Dire"
```

  - When the `while` loop finishes, one of the queues will be empty.
  - This line is a concise way to check which queue still has elements. If `radiant_q` is not empty, Radiant wins. Otherwise, Dire must have won.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `senate = "RDD"` (`n=3`) with extreme detail.

1.  **Initialization**:
      * `n = 3`
      * `radiant_q` = `deque([0])`
      * `dire_q` = `deque([1, 2])`

-----

### **Loop 1**

  - **Condition**: `radiant_q` is not empty AND `dire_q` is not empty. True.
  - **Dequeue**: `r_idx = radiant_q.popleft()` -\> `r_idx = 0`. `radiant_q` is now `deque([])`.
  - **Dequeue**: `d_idx = dire_q.popleft()` -\> `d_idx = 1`. `dire_q` is now `deque([2])`.
  - **Compare**: `if r_idx < d_idx` -\> `if 0 < 1`. **True**.
  - **Action**: The Radiant senator at index 0 wins. The Dire senator at index 1 is banned. The Radiant senator is re-queued for the next round.
      * `radiant_q.append(0 + 3)` -\> `radiant_q.append(3)`.
  - **State at end of loop 1**: `radiant_q` is `deque([3])`, `dire_q` is `deque([2])`.

-----

### **Loop 2**

  - **Condition**: `radiant_q` is not empty AND `dire_q` is not empty. True.
  - **Dequeue**: `r_idx = radiant_q.popleft()` -\> `r_idx = 3`. `radiant_q` is now `deque([])`.
  - **Dequeue**: `d_idx = dire_q.popleft()` -\> `d_idx = 2`. `dire_q` is now `deque([])`.
  - **Compare**: `if r_idx < d_idx` -\> `if 3 < 2`. **False**. The `else` block runs.
  - **Action**: The Dire senator at index 2 wins. The Radiant senator at original index 0 (now with turn value 3) is banned. The Dire senator is re-queued for the next round.
      * `dire_q.append(2 + 3)` -\> `dire_q.append(5)`.
  - **State at end of loop 2**: `radiant_q` is `deque([])`, `dire_q` is `deque([5])`.

-----

### **End of Simulation**

  - **Condition**: `while radiant_q and dire_q`. `radiant_q` is now empty, so the condition is **False**. The loop terminates.

### **Final Result**

  - The code executes `return "Radiant" if radiant_q else "Dire"`.
  - Since `radiant_q` is empty, this evaluates to `False`, and the function returns **`"Dire"`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of senators. In each iteration of the `while` loop, one senator is permanently eliminated. Since there are `n` total senators, the loop can run at most `n-1` times before one party is completely gone. All queue operations (`append`, `popleft`) are `O(1)`.

### Space Complexity: O(n)

  - The queues will initially store the indices of all `n` senators. The space required is proportional to the input size.