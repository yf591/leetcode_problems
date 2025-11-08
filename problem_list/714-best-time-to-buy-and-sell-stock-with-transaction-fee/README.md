# 714\. Best Time to Buy and Sell Stock with Transaction Fee - Solution Explanation

## Problem Overview

You are given an array of stock `prices` and a transaction `fee`. The goal is to find the **maximum profit** you can make by buying and selling stock multiple times.

**Key Rules & Constraints:**

  - You can complete as many transactions as you like.
  - You must sell the stock before you can buy again (you can't hold multiple shares).
  - A single "transaction" (a buy and a sell) costs a `fee`, which is paid upon selling.

**Example:**

```python
Input: prices = [1,3,2,8,4,9], fee = 2
Output: 8
Explanation:
- Buy at prices[0] = 1
- Sell at prices[3] = 8
- Profit = (8 - 1) - 2 (fee) = 5
-
- Buy at prices[4] = 4
- Sell at prices[5] = 9
- Profit = (9 - 4) - 2 (fee) = 3
-
- Total Profit = 5 + 3 = 8.
```

## Deep Dive: What is Dynamic Programming (DP)? 🧠

Before the solution, let's understand the core concept. **Dynamic Programming (DP)** is an algorithmic technique for solving complex problems by breaking them down into simpler, **overlapping subproblems**.

  - **1D DP (like House Robber)**: The solution for a problem at step `i` (e.g., `dp[i]`) depends on the solutions from previous steps, like `dp[i-1]` or `dp[i-2]`. The "state" at `i` can be described by a single number.

  - **Multidimensional DP (like this problem)**: This is used when the state at a given step `i` cannot be described by a single number. You need more information.

      - For this problem, on any given day `i`, just knowing the "max profit so far" is not enough. We also need to know: **"Are we currently holding a stock?"**
      - This creates two distinct states for each day:
        1.  Max profit on day `i` if we are **holding** a stock.
        2.  Max profit on day `i` if we have **cash** (i.e., not holding a stock).
      - Because our state for day `i` depends on two values, a full DP table would be two-dimensional: `dp[n][2]`, where `n` is the number of days and `2` is the number of states. This is why LeetCode tags it as "Multidimensional DP."

## Key Insights: The State Machine

The problem can be perfectly modeled as a "state machine" with two states: `cash` and `hold`. At each day, we calculate the maximum possible profit for being in either of these two states.

### State 1: `cash` (Max profit if we do NOT hold a stock today)

How can we end up with `cash` (no stock) on day `i`?

  - **Option A: We had `cash` yesterday and did nothing.** (We "rested").
      - `profit = cash_yesterday`
  - **Option B: We `held` a stock yesterday and sold it today.**
      - `profit = hold_yesterday + prices[i] - fee`
  - We want the *maximum* of these, so:
    **`cash_today = max(cash_yesterday, hold_yesterday + prices[i] - fee)`**

### State 2: `hold` (Max profit if we DO hold a stock today)

How can we end up `hold`ing a stock on day `i`?

  - **Option A: We `held` a stock yesterday and did nothing.** (We "rested").
      - `profit = hold_yesterday`
  - **Option B: We had `cash` yesterday and bought the stock today.**
      - `profit = cash_yesterday - prices[i]`
  - We want the *maximum* of these, so:
    **`hold_today = max(hold_yesterday, cash_yesterday - prices[i])`**

### The "Aha\!" Moment: Space Optimization

If you look at the formulas above, to calculate the states for `cash_today` and `hold_today`, we *only* need the values from `cash_yesterday` and `hold_yesterday`. We never need the values from two or more days ago.

This means we don't need to store the entire `dp[n][2]` table. We can solve this using just **two variables** to store the previous day's `cash` and `hold` states, giving us a beautiful **`O(1)` space** solution.

## Solution Approach

This solution iterates through the `prices` array once. It maintains two variables, `cash` and `hold`, representing the maximum profit in each of the two states *at the end of the current day*. A temporary variable `prev_cash` is used to handle the dependencies correctly within the loop.

```python
from typing import List

class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:
        
        # 'cash': The max profit we have on the current day if we end
        #         the day with NO stock (i.e., cash in hand).
        cash = 0
        
        # 'hold': The max profit we have on the current day if we end
        #         the day HOLDING one share of stock.
        # Start at -infinity because it's impossible to hold a stock
        # before the first day, and this forces the first "buy" action.
        hold = -float('inf')
        
        for price in prices:
            # We need to save the 'cash' value from the previous day,
            # because the 'hold' calculation depends on it.
            prev_cash = cash
            
            # --- Calculate the new 'cash' state for today ---
            # We can either:
            # 1. Do nothing (keep the 'cash' from yesterday).
            # 2. Sell the stock we were holding ('hold') for today's 'price', minus the 'fee'.
            cash = max(cash, hold + price - fee)
            
            # --- Calculate the new 'hold' state for today ---
            # We can either:
            # 1. Do nothing (keep the 'hold' from yesterday).
            # 2. Buy a stock today, using the 'cash' we had yesterday ('prev_cash').
            hold = max(hold, prev_cash - price)
            
        # After iterating through all prices, the maximum profit is
        # the 'cash' state. (It's never optimal to end by holding a stock).
        return cash
```

## Detailed Code Analysis

### Step 1: Initialization

```python
cash = 0
hold = -float('inf')
```

  - `cash = 0`: We initialize our "cash-in-hand" profit to 0. We start with no money and no stock.
  - `hold = -float('inf')`: This is a very important trick. We initialize `hold` to negative infinity to represent that it's an "impossible" state to be in before the market opens. This forces the algorithm to make a "buy" action on the first day (or any day) it's profitable to do so. For example, `max(-inf, 0 - price)` will always be `-price`, correctly setting our `hold` state to the cost of our first purchase.

### Step 2: The Loop and `prev_cash`

```python
for price in prices:
    prev_cash = cash
    ...
```

  - We iterate through each `price` in the `prices` array.
  - `prev_cash = cash`: This is a critical step. Inside the loop, `cash` and `hold` represent the states from the *previous* day. We are about to calculate the new `cash` state, but the `hold` calculation *also* needs the old `cash` state. We save it in `prev_cash` before it gets overwritten.

### Step 3: Calculating the New `cash`

```python
cash = max(cash, hold + price - fee)
```

  - This line calculates the maximum profit we can have at the end of *this* day if we are **not** holding a stock.
  - `cash`: This is `prev_cash`, the profit from *resting* (not holding a stock yesterday, not buying today).
  - `hold + price - fee`: This is the profit from *selling*. `hold` is the value of our `hold` state from yesterday. We add today's `price` and subtract the `fee`.
  - `max(...)` takes the better of these two actions.

### Step 4: Calculating the New `hold`

```python
hold = max(hold, prev_cash - price)
```

  - This line calculates the maximum profit (or minimum loss) we can have at the end of *this* day if we **are** holding a stock.
  - `hold`: This is `prev_hold`, the value from *resting* (holding a stock yesterday, not selling today).
  - `prev_cash - price`: This is the value from *buying*. We use `prev_cash` (the cash we had *before* this day's calculations) and subtract today's `price` to buy the stock.

### Step 5: The Final Return

```python
return cash
```

  - After the loop finishes, we will have the final values for `cash` and `hold`. The maximum profit is always achieved by ending in the `cash` state, as ending in the `hold` state means you have an unsold asset. We return `cash`.

## Step-by-Step Execution Trace

Let's trace `prices = [1, 3, 2, 8]`, `fee = 2` with extreme detail.

### **Initial State:**

  - `cash = 0`
  - `hold = -inf`

-----

### **Loop 1: `price = 1`**

1.  `prev_cash = cash` -\> `prev_cash = 0`
2.  `cash = max(cash, hold + price - fee)`
      - `cash = max(0, -inf + 1 - 2)`
      - `cash = max(0, -inf)` -\> `cash = 0`
3.  `hold = max(hold, prev_cash - price)`
      - `hold = max(-inf, 0 - 1)`
      - `hold = max(-inf, -1)` -\> `hold = -1`
        **State after loop 1:** `cash = 0`, `hold = -1` (This means we are holding a stock we "bought" for 1, so our net worth is -1).

-----

### **Loop 2: `price = 3`**

1.  `prev_cash = cash` -\> `prev_cash = 0`
2.  `cash = max(cash, hold + price - fee)`
      - `cash = max(0, -1 + 3 - 2)`
      - `cash = max(0, 0)` -\> `cash = 0` (It's not profitable to sell yet).
3.  `hold = max(hold, prev_cash - price)`
      - `hold = max(-1, 0 - 3)`
      - `hold = max(-1, -3)` -\> `hold = -1` (It's better to keep holding the stock we "bought" at 1 than to buy a new one at 3).
        **State after loop 2:** `cash = 0`, `hold = -1`

-----

### **Loop 3: `price = 2`**

1.  `prev_cash = cash` -\> `prev_cash = 0`
2.  `cash = max(cash, hold + price - fee)`
      - `cash = max(0, -1 + 2 - 2)`
      - `cash = max(0, -1)` -\> `cash = 0`
3.  `hold = max(hold, prev_cash - price)`
      - `hold = max(-1, 0 - 2)`
      - `hold = max(-1, -2)` -\> `hold = -1`
        **State after loop 3:** `cash = 0`, `hold = -1`

-----

### **Loop 4: `price = 8`**

1.  `prev_cash = cash` -\> `prev_cash = 0`
2.  `cash = max(cash, hold + price - fee)`
      - `cash = max(0, -1 + 8 - 2)`
      - `cash = max(0, 5)` -\> `cash = 5` (We finally sell\! Our profit is 5).
3.  `hold = max(hold, prev_cash - price)`
      - `hold = max(-1, 0 - 8)`
      - `hold = max(-1, -8)` -\> `hold = -1`
        **State after loop 4:** `cash = 5`, `hold = -1`

-----

### **End of Algorithm**

  - The `for` loop finishes.
  - The function returns the final `cash` value, which is **5**. (Note: The example output is 8, my trace was for a truncated `prices`. The logic is sound and will produce 8 for the full example).

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of days (the length of the `prices` array). We iterate through the array exactly once.

### Space Complexity: O(1)

  - This is the optimized solution. We only use a few constant-space variables (`cash`, `hold`, `prev_cash`). The space required does not grow with the size of the input.