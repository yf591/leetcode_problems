# 735\. Asteroid Collision - Solution Explanation

## Problem Overview

You are given an array of integers `asteroids`, representing asteroids in a single row. The goal is to simulate all possible collisions and return the state of the asteroids after all collisions have occurred.

**Key Definitions & Rules:**

  - **Size**: The absolute value of the number (e.g., `abs(-5)` is 5).
  - **Direction**: The sign of the number. Positive means moving right, negative means moving left.
  - **Collision**: A collision **only** happens when a right-moving asteroid is followed by a left-moving one (`... 10, -5 ...`). Two asteroids moving in the same direction, or moving away from each other, will never collide.
  - **Collision Outcome**:
      - If one asteroid is bigger, the smaller one explodes.
      - If both are the same size, both explode.
      - The surviving asteroid continues on its path.

**Example:**

```python
Input: asteroids = [10, 2, -5]
Output: [10]
Explanation:
1. First, 2 (right) and -5 (left) collide. Since abs(-5) > abs(2), the 2 explodes. The list becomes [10, -5].
2. Now, 10 (right) and -5 (left) collide. Since abs(10) > abs(-5), the -5 explodes. The list becomes [10].
3. No more collisions are possible. The final state is [10].
```

## Key Insights

### The Nature of Collisions & The Stack

This is the most critical insight. A new asteroid moving through space will only ever interact with the **last stable asteroid** it encounters.

  - If you have a row of survivors `[5, 10]` and a new asteroid `-5` comes along, it will first collide with the `10`.
  - If the `-5` survives that collision (it doesn't), it would *then* collide with the `5`.

This pattern, where the newest item (`-5`) interacts with the most recently added stable item (`10`), is a perfect example of a **Last-In, First-Out (LIFO)** process. The ideal data structure for managing LIFO interactions is a **stack**.

Our stack will represent the list of asteroids that have survived all collisions so far. We will process each new asteroid from the input list and see how it interacts with the top of our stack.

## Solution Approach

This solution uses a list to function as a stack. We iterate through each `asteroid` from the input. For each `new_ast`, we check if it can collide with the asteroid at the top of the stack. A `while` loop handles the chain reaction of collisions until the `new_ast` is either destroyed or becomes stable.

```python
from typing import List

class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        # The stack will store the asteroids that have survived collisions so far.
        stack = []
        
        for new_ast in asteroids:
            # A collision happens if the stack has a right-moving asteroid
            # and the new asteroid is a left-moving one. We loop until
            # this condition is false or the new asteroid is destroyed.
            while stack and new_ast < 0 and stack[-1] > 0:
                # Get the last asteroid from the stack (the one moving right).
                last_ast = stack[-1]
                
                # Case 1: Both asteroids are the same size; both explode.
                if abs(new_ast) == abs(last_ast):
                    stack.pop() # The asteroid on the stack explodes.
                    break       # The new asteroid also explodes; stop its processing.
                
                # Case 2: The asteroid on the stack is bigger.
                elif abs(last_ast) > abs(new_ast):
                    # The new asteroid explodes; the one on the stack survives.
                    break       # Stop processing the new asteroid.
                
                # Case 3: The new asteroid is bigger.
                else: # abs(new_ast) > abs(last_ast)
                    # The asteroid on the stack explodes.
                    stack.pop()
                    # The loop continues, as the new asteroid survived and must now
                    # check against the NEXT asteroid on the stack.
            else:
                # This 'else' block is special. It only runs if the 'while' loop
                # finished without being terminated by a 'break' statement.
                # This means the new_ast either didn't cause a collision or
                # it won every collision. In either case, it survives.
                stack.append(new_ast)
                
        return stack
```

## Detailed Code Analysis

### Step 1: Initialization

```python
stack = []
```

  - We initialize an empty list that will serve as our stack. It will hold the final state of the asteroids.

### Step 2: The Main Loop

```python
for new_ast in asteroids:
```

  - We iterate through every asteroid in the input list, from left to right.

### Step 3: The Collision `while` Loop

```python
while stack and new_ast < 0 and stack[-1] > 0:
```

  - This is the heart of the collision detection logic. The loop only runs if all three conditions are met:
    1.  `stack`: The stack is not empty (there's something to collide with).
    2.  `new_ast < 0`: The incoming asteroid is moving left.
    3.  `stack[-1] > 0`: The last surviving asteroid is moving right.
  - This `while` loop will continue as long as the incoming `new_ast` keeps destroying asteroids on the stack.

### Step 4: The Collision Logic (Inside the `while` loop)

```python
if abs(new_ast) == abs(last_ast):
    stack.pop()
    break
```

  - **Equal Size**: Both asteroids are destroyed. We `pop()` the one from the stack, and `break` the loop, which prevents the `new_ast` from being added later.

<!-- end list -->

```python
elif abs(last_ast) > abs(new_ast):
    break
```

  - **Stack Asteroid is Bigger**: The `new_ast` is destroyed. We do nothing to the stack. We just `break` the loop to stop processing the `new_ast`.

<!-- end list -->

```python
else: # abs(new_ast) > abs(last_ast)
    stack.pop()
```

  - **New Asteroid is Bigger**: The asteroid on the stack is destroyed, so we `pop()` it. The loop **does not break**. It will repeat, checking the `new_ast` against the *new* top of the stack.

### Step 5: The `while...else` Block

```python
else:
    stack.append(new_ast)
```

  - This is a unique feature of Python's `for` and `while` loops. The `else` block is executed only if the loop completes **naturally** (its condition becomes false) and was **not** exited by a `break` statement.
  - This is perfect for our logic. If the `new_ast` is ever destroyed (by hitting a bigger or equal-sized asteroid), the `while` loop will `break`, and this `else` block will be skipped.
  - If the `new_ast` survives all its collisions (or if there were no collisions to begin with), the `while` loop's condition will eventually become false, and this `else` block will run, adding the victorious `new_ast` to the stack.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `asteroids = [10, 2, -5]` with extreme detail.

| `new_ast` | `stack` (start) | `while` loop runs? | Action inside `while` | `stack` (after `while`) | `else` block runs? | `stack` (final) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **10** | `[]` | No (new\_ast is not \< 0) | - | `[]` | Yes | `[10]` |
| **2** | `[10]` | No (new\_ast is not \< 0) | - | `[10]` | Yes | `[10, 2]` |
| **-5** | `[10, 2]` | **Yes** (`-5`\<0, `2`\>0) | `abs(-5)>abs(2)` -\> `else` branch -\> `stack.pop()` | `[10]` | - | - |
| (cont.)| `[10]` | **Yes** (`-5`\<0, `10`\>0) | `abs(10)>abs(-5)` -\> `elif` branch -\> `break` | `[10]` | **No** (loop broke)| `[10]` |

  - The `for` loop finishes.
  - The function returns the final `stack`, which is `[10]`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of asteroids. Although there is a nested `while` loop, this is a linear time solution. This is because each asteroid is pushed onto the stack at most once. It can only be popped once. The total number of push and pop operations is proportional to `n`.

### Space Complexity: O(n)

  - In the worst-case scenario (e.g., all asteroids are moving right, or all are moving left), no collisions occur, and the stack will grow to the same size as the input array.