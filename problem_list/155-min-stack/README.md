# 155\. Min Stack - Solution Explanation

## Problem Overview

The task is to design a special stack, called `MinStack`, that supports all the standard stack operations (`push`, `pop`, `top`) but with an additional feature: a `getMin` function that retrieves the minimum element currently in the stack.

**The Crucial Constraint:**
Every single one of these functions—`push`, `pop`, `top`, and `getMin`—must have a time complexity of **O(1)**, meaning they must execute in constant time, no matter how many elements are in the stack.

**Example:**

```
minStack = MinStack()
minStack.push(-2)
minStack.push(0)
minStack.push(-3)
minStack.getMin()  // returns -3
minStack.pop()
minStack.top()     // returns 0
minStack.getMin()  // returns -2
```

## Key Insights

### The Challenge of `getMin` in O(1)

  - Implementing `push`, `pop`, and `top` in O(1) is simple with a standard list in Python (`append`, `pop`, `stack[-1]`).
  - The main challenge is `getMin`. A naive approach of searching the entire stack for the minimum (`min(self.stack)`) would be an `O(n)` operation, which is too slow.
  - What if we just use a single variable, `current_min`, to track the minimum? This seems promising until we `pop`. If we pop the `current_min` element, we have no way of knowing what the *new* minimum is without searching the entire stack again (`O(n)`).

### The Two-Stack Insight

The key to solving this is to realize that we need to keep a **history of the minimums**. For every state of our main stack, we need to know what the minimum value was at that specific point in time.

This leads to the elegant **two-stack solution**:

1.  **`stack`**: A normal stack that stores all the values pushed.
2.  **`min_stack`**: A second, parallel stack. For every element we push onto the main `stack`, we will push the **current overall minimum** onto this `min_stack`.

This way, the value at the top of the `min_stack` will *always* be the minimum value of the entire `stack`. When we pop from the main stack, we also pop from the `min_stack`, effectively "rewinding" to the previous state's minimum.

## Solution Approach

This solution implements the two-stack strategy. One stack holds the actual data, and the other holds the minimum value at each stage of the data stack's history.

```python
class MinStack:
    def __init__(self):
        """
        Initializes two lists that will function as our stacks.
        """
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        """
        Pushes a value onto the main stack and updates the min_stack.
        """
        # Always push the new value onto the main stack.
        self.stack.append(val)
        
        # Decide what the new current minimum is and push it onto the min_stack.
        if not self.min_stack:
            # If min_stack is empty, this is the first element, so it's the minimum.
            self.min_stack.append(val)
        else:
            # The new minimum is the smaller of the new value and the previous minimum.
            current_min = self.min_stack[-1]
            self.min_stack.append(min(val, current_min))

    def pop(self) -> None:
        """
        Pops from both stacks to keep them perfectly synchronized.
        """
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        """
        Returns the top element of the main data stack.
        """
        return self.stack[-1]

    def getMin(self) -> int:
        """
        Returns the overall minimum, which is always at the top of the min_stack.
        """
        return self.min_stack[-1]
```

## Detailed Code Analysis

### `__init__(self)`

```python
self.stack = []
self.min_stack = []
```

  - We initialize two empty lists. `self.stack` will store the actual numbers. `self.min_stack` will be our "shadow" stack that tracks the history of minimums.

### `push(self, val: int)`

This is the most important method.

```python
self.stack.append(val)
```

  - First, we perform the standard stack operation, adding the new `val` to the end of our main `stack`.

<!-- end list -->

```python
if not self.min_stack:
    self.min_stack.append(val)
else:
    current_min = self.min_stack[-1]
    self.min_stack.append(min(val, current_min))
```

  - Next, we must update our `min_stack` to reflect this new state.
  - **`if not self.min_stack:`**: This handles the case of the very first push. If the `min_stack` is empty, then the new `val` is automatically the first and only minimum value.
  - **`else:`**: If the stack is not empty, the new overall minimum will be either the `val` we are pushing (if it's smaller) or the previous overall minimum.
      - `current_min = self.min_stack[-1]` retrieves the previous minimum from the top of the `min_stack`.
      - `min(val, current_min)` calculates the new overall minimum.
      - `self.min_stack.append(...)` pushes this new minimum onto the `min_stack`.

### `pop(self)`

```python
self.stack.pop()
self.min_stack.pop()
```

  - This is simple but crucial. To keep our two stacks perfectly synchronized, whenever we remove an element from the main `stack`, we must also remove the corresponding minimum value from the `min_stack`. This correctly "rolls back" the minimum to what it was before the last push.

### `top(self)` and `getMin(self)`

```python
return self.stack[-1]
# ...
return self.min_stack[-1]
```

  - These methods are now trivial. They simply "peek" at the last element (`[-1]`) of the respective stacks. Because of the logic in `push` and `pop`, the last element of `min_stack` is guaranteed to be the current minimum of `stack`. Both are `O(1)` operations.

## Step-by-Step Execution Trace

Let's trace the exact sequence from the example: `["push",-2],["push",0],["push",-3],["getMin"],["pop"],["top"],["getMin"]` with extreme detail.

| Operation | `self.stack` State (after) | `self.min_stack` State (after) | Return Value | Explanation |
| :--- | :--- | :--- | :--- | :--- |
| **`__init__()`** | `[]` | `[]` | `null` | Stacks are initialized. |
| **`push(-2)`** | `[-2]` | `[-2]` | `null` | `min_stack` was empty, so `-2` is the new min. |
| **`push(0)`** | `[-2, 0]` | `[-2, -2]` | `null` | `min(0, -2)` is `-2`. Push `-2` to `min_stack`. |
| **`push(-3)`** | `[-2, 0, -3]`| `[-2, -2, -3]`| `null` | `min(-3, -2)` is `-3`. Push `-3` to `min_stack`. |
| **`getMin()`** | `[-2, 0, -3]`| `[-2, -2, -3]`| **-3** | Return the top of `min_stack`: `-3`. |
| **`pop()`** | `[-2, 0]` | `[-2, -2]` | `null` | Pop from both stacks. |
| **`top()`** | `[-2, 0]` | `[-2, -2]` | **0** | Return the top of `stack`: `0`. |
| **`getMin()`** | `[-2, 0]` | `[-2, -2]` | **-2** | Return the top of `min_stack`: `-2`. |

## Performance Analysis

### Time Complexity: O(1) for all operations

  - **`push`**: `append` is O(1). Accessing the last element (`[-1]`) is O(1).
  - **`pop`**: `pop` from the end of a list is O(1).
  - **`top`**: Accessing the last element is O(1).
  - **`getMin`**: Accessing the last element is O(1).

### Space Complexity: O(n)

  - Where `n` is the number of elements in the stack. We use two stacks, and in the worst case, each will hold `n` elements. Therefore, the space is proportional to the number of items pushed.

## Key Learning Points

  - **Augmenting Data Structures**: This problem demonstrates how to take a standard data structure (a stack) and augment it with extra capabilities (like `getMin`) by adding another data structure that runs in parallel.
  - **The Two-Stack Pattern**: The two-stack approach is a common and powerful pattern for problems that require tracking a running property (like a minimum, maximum, sum, etc.) in a LIFO manner.
  - **Time vs. Space Trade-off**: We achieve `O(1)` time for `getMin` by using `O(n)` extra space for the `min_stack`. This is a classic example of a time-space trade-off.