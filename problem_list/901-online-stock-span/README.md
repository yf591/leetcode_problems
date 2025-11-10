# 901\. Online Stock Span - Solution Explanation

## Problem Overview

You are asked to implement a `StockSpanner` class. This class does two things:

  - `__init__()`: Initializes the object.
  - `next(int price)`: Takes the current day's stock `price` and returns its **span**.

**Span Definition:**
The "span" of a stock's price today is the maximum number of **consecutive days** (starting from today and going backward) for which the stock's price was **less than or equal to** today's price.

**Example:**

  - Prices: `[100, 80, 60, 70, 60, 75, 85]`
  - Call `next(75)`:
      - Today's price: 75.
      - Looking back: `[75` (is \<= 75), `60` (is \<= 75), `70` (is \<= 75), `60` (is \<= 75), `80` (is \> 75).
      - The consecutive run is `[75, 60, 70, 60]`.
      - The span is **4**.
  - Call `next(85)`:
      - Today's price: 85.
      - Looking back: `[85, 75, 60, 70, 60, 80]`... wait, the full history is `[100, 80, 60, 70, 60, 75]`.
      - Looking back from 85: `[85` (\<= 85), `75` (\<= 85), `60` (\<= 85), `70` (\<= 85), `60` (\<= 85), `80` (\<= 85), `100` (\> 85).
      - The consecutive run is `[85, 75, 60, 70, 60, 80]`.
      - The span is **6**.

## Deep Dive: What is a Monotonic Stack? 📚

A **Monotonic Stack** is a special type of stack that maintains a specific order among its elements, either **monotonically increasing** or **monotonically decreasing**.

  - **Monotonic Decreasing Stack**: The elements in the stack are always in descending order from bottom to top. `[100, 80, 70]` is a valid state.
  - **Monotonic Increasing Stack**: The elements are always in ascending order. `[10, 20, 50]` is a valid state.

### The "Magic" of a Monotonic Stack

The power of this data structure is in its push operation. When you push a new element, you must maintain the monotonic property.

  - **Example (Decreasing Stack)**:
      - Stack is `[100, 80, 60]`.
      - New price `70` arrives.
      - To maintain the decreasing order, we must **pop** all elements smaller than `70` *before* pushing `70`.
      - `60 < 70`? Yes. Pop `60`. Stack is `[100, 80]`.
      - `80 < 70`? No. Stop.
      - Push `70`. Stack is `[100, 80, 70]`.

### Why is this useful?

This "pop-until-valid" action is incredibly useful for problems involving "the next greater element" or, in our case, "the **previous greater element**."

The `span` of a price is simply the number of days until we hit a "blocker" - a day with a price *greater than* the current price. A monotonic decreasing stack is the perfect tool to keep track of these "blockers."

## Key Insights for This Problem

### 1\. The Inefficient (Naive) Approach

We could store all past prices in a list. For every `next(price)` call, we would add the price to the list and then loop *backwards* through the list, counting until we find a price `> price`.

  - **Problem**: This loop is an `O(n)` operation *for each call*. If we make `n` calls, the total time is `O(n²)`, which is too slow.

### 2\. The Efficient (Monotonic Stack) Insight

The naive approach re-scans the same small numbers over and over.

  - When `75` arrives, we scan `[60, 70, 60]`.
  - When `85` arrives, we scan `[75, 60, 70, 60]`.
    We are re-scanning `60, 70, 60`. How can we avoid this?

Let's not just store prices on the stack, but store the **span** we calculated for that price. Our stack will hold `(price, span)` pairs.

When a new `price` arrives (e.g., `75`), we calculate its `span`, starting at 1 (for itself).

  - We look at the top of the stack: `(60, 1)`.
  - Is `75 >= 60`? Yes. This means the `60` is *not* a blocker. Its entire span of `1` day is part of our `75`'s span.
  - We "absorb" its span: `current_span += 1`. `current_span` is now `2`.
  - We `pop` `(60, 1)`.
  - We look at the new top: `(70, 2)`.
  - Is `75 >= 70`? Yes. This `70` is also not a blocker. Its entire span of `2` days (`[60, 70]`) is part of our `75`'s span.
  - We absorb its span: `current_span += 2`. `current_span` is now `4`.
  - We `pop` `(70, 2)`.
  - We look at the new top: `(80, 1)`.
  - Is `75 >= 80`? No. `80` is a blocker. We stop.
  - We push our new state onto the stack: `stack.append((75, 4))`.

This process finds the span in a single, amortized `O(1)` operation.

## Solution Approach

This solution implements the Monotonic Decreasing Stack. The stack stores `(price, span)` tuples. For each `next` call, it pops all smaller or equal elements from the stack, summing their spans into the new element's span, before pushing the new element.

```python
from typing import List

class Solution:

    def __init__(self):
        # The stack will store tuples of: (price, span)
        # It will be maintained as a monotonically decreasing stack
        # (based on the price).
        self.stack = []

    def next(self, price: int) -> int:
        
        # Step 1: Initialize the span for the current day to 1 (for itself).
        current_span = 1
        
        # Step 2: Use the monotonic stack logic.
        # While the stack is not empty AND
        # today's price is greater than or equal to the price at the top of the stack...
        while self.stack and price >= self.stack[-1][0]:
            
            # ...it means the new price's span can "absorb" the span
            # of the (popped) element, because the popped element is not
            # a "blocker".
            
            # Pop the (price, span) tuple of the smaller, preceding day.
            popped_price, popped_span = self.stack.pop()
            
            # Add its span to our current span.
            current_span += popped_span
            
        # Step 3: After the loop, the stack is either empty or the top
        # element is a "blocker" (a price greater than the current one).
        
        # Add the new price and its total calculated span to the stack.
        self.stack.append((price, current_span))
        
        # Step 4: Return the span we just calculated.
        return current_span
```

## Step-by-Step Execution Trace

Let's trace the full example `[100, 80, 60, 70, 60, 75, 85]` with extreme detail.

### **Initial State:**

  - `obj = StockSpanner()`
  - `stack = []`

-----

### **Call 1: `next(100)`**

1.  `current_span = 1`.
2.  `while stack...`: Stack is empty. Loop does not run.
3.  `stack.append((100, 1))`.
4.  **Return `1`**.

<!-- end list -->

  - **Stack state:** `[(100, 1)]`

-----

### **Call 2: `next(80)`**

1.  `current_span = 1`.
2.  `while stack...`: `100` is on stack. `80 >= 100`? **False**. Loop does not run.
3.  `stack.append((80, 1))`.
4.  **Return `1`**.

<!-- end list -->

  - **Stack state:** `[(100, 1), (80, 1)]`

-----

### **Call 3: `next(60)`**

1.  `current_span = 1`.
2.  `while stack...`: `80` is on top. `60 >= 80`? **False**. Loop does not run.
3.  `stack.append((60, 1))`.
4.  **Return `1`**.

<!-- end list -->

  - **Stack state:** `[(100, 1), (80, 1), (60, 1)]`

-----

### **Call 4: `next(70)`**

1.  `current_span = 1`.
2.  `while stack...`: `60` is on top. `70 >= 60`? **True**.
      - `popped_span = 1` (from `(60, 1)`).
      - `current_span = 1 + 1 = 2`.
      - `stack.pop()`. Stack is now `[(100, 1), (80, 1)]`.
3.  `while stack...`: `80` is on top. `70 >= 80`? **False**. Loop terminates.
4.  `stack.append((70, 2))`.
5.  **Return `2`**.

<!-- end list -->

  - **Stack state:** `[(100, 1), (80, 1), (70, 2)]`

-----

### **Call 5: `next(60)`**

1.  `current_span = 1`.
2.  `while stack...`: `70` is on top. `60 >= 70`? **False**. Loop does not run.
3.  `stack.append((60, 1))`.
4.  **Return `1`**.

<!-- end list -->

  - **Stack state:** `[(100, 1), (80, 1), (70, 2), (60, 1)]`

-----

### **Call 6: `next(75)`**

1.  `current_span = 1`.
2.  `while stack...`: `60` is on top. `75 >= 60`? **True**.
      - `popped_span = 1`. `current_span = 1 + 1 = 2`.
      - `stack.pop()`. Stack is `[(100, 1), (80, 1), (70, 2)]`.
3.  `while stack...`: `70` is on top. `75 >= 70`? **True**.
      - `popped_span = 2`. `current_span = 2 + 2 = 4`.
      - `stack.pop()`. Stack is `[(100, 1), (80, 1)]`.
4.  `while stack...`: `80` is on top. `75 >= 80`? **False**. Loop terminates.
5.  `stack.append((75, 4))`.
6.  **Return `4`**.

<!-- end list -->

  - **Stack state:** `[(100, 1), (80, 1), (75, 4)]`

-----

### **Call 7: `next(85)`**

1.  `current_span = 1`.
2.  `while stack...`: `75` is on top. `85 >= 75`? **True**.
      - `popped_span = 4`. `current_span = 1 + 4 = 5`.
      - `stack.pop()`. Stack is `[(100, 1), (80, 1)]`.
3.  `while stack...`: `80` is on top. `85 >= 80`? **True**.
      - `popped_span = 1`. `current_span = 5 + 1 = 6`.
      - `stack.pop()`. Stack is `[(100, 1)]`.
4.  `while stack...`: `100` is on top. `85 >= 100`? **False**. Loop terminates.
5.  `stack.append((85, 6))`.
6.  **Return `6`**.

<!-- end list -->

  - **Stack state:** `[(100, 1), (85, 6)]`

## Performance Analysis

### Time Complexity: Amortized O(1)

  - This is the most brilliant part of this solution. A single `next` call *could* be `O(n)` in the worst case (e.g., if a new price of 200 arrives and the stack has 100 elements, it will pop all of them).
  - However, over `n` calls to `next()`, each element is **pushed** onto the stack exactly once and **popped** at most once.
  - The total work for `n` calls is `O(n)` (for all pushes and pops combined).
  - Therefore, the **amortized** (or average) time complexity per call is `O(n) / n = O(1)`.

### Space Complexity: O(n)

  - Where `n` is the number of calls made to `next()`.
  - In the worst-case scenario (a strictly decreasing list of prices like `[100, 80, 70, 60]`), the stack will store every element, leading to `O(n)` space.