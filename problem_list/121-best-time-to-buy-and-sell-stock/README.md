# 121\. Best Time to Buy and Sell Stock - Solution Explanation

## Problem Overview

You are given a list of stock prices, where each index represents a day. You need to find the maximum profit you can make by buying the stock on one day and selling it on a **future** day.

**Key Rules**

  - You can only perform one transaction (one buy, one sell).
  - You must buy before you can sell.
  - If no profit can be made, the maximum profit is 0.

**Examples**

```python
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: The best time to buy is on day 2 (price=1) and sell on day 5 (price=6). Profit = 6 - 1 = 5.

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: The price is always decreasing, so no profitable transaction is possible.
```

## Key Insights

### Single-Pass Optimization

A brute-force solution would be to check every possible pair of buy and sell days, which would be too slow (O(n²)). The key insight for an efficient solution is that this can be solved in a **single pass** through the price list.

As we iterate through the days, we only need to keep track of two things:

1.  The lowest stock price we've seen **so far**.
2.  The maximum profit we could have achieved **so far**.

At each day, we can ask: "If I sold today, what would my profit be?" The profit would be today's price minus the lowest price we've seen up to this point.

## Solution Approach

This solution iterates through the `prices` list once, maintaining two variables to track the minimum price and maximum profit.

```python
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price_so_far = float('inf')
        max_profit = 0
        
        for price in prices:
            # Calculate the potential profit if we were to sell today
            potential_profit = price - min_price_so_far
            
            # Update the overall maximum profit if today's is better
            max_profit = max(max_profit, potential_profit)
            
            # Update the minimum price we've seen for future calculations
            min_price_so_far = min(min_price_so_far, price)
            
        return max_profit
```

**Strategy**

1.  **Initialize**: Set `min_price_so_far` to infinity and `max_profit` to 0.
2.  **Iterate**: Loop through each price in the `prices` list.
3.  **Calculate & Update**: In each iteration, first calculate the potential profit based on the current price and the minimum price seen so far. Update `max_profit`. Then, update `min_price_so_far`.
4.  **Return**: After the loop, `max_profit` will hold the highest possible profit.

## Detailed Code Analysis

### Step 1: Initialization

```python
min_price_so_far = float('inf')
max_profit = 0
```

  - We initialize `min_price_so_far` to infinity (`float('inf')`) so that the very first price we see is guaranteed to be lower.
  - We initialize `max_profit` to `0` because if we can't make a profit, the answer must be 0.

### Step 2 & 3: Calculating and Updating Profit

```python
potential_profit = price - min_price_so_far
max_profit = max(max_profit, potential_profit)
```

  - For each `price` in our loop, we calculate the profit we would get if we sold on this day. The best buy price would have been the `min_price_so_far`.
  - We then use `max()` to update `max_profit` only if this `potential_profit` is greater than any profit we've seen before.

### Step 4: Updating the Minimum Price

```python
min_price_so_far = min(min_price_so_far, price)
```

  - This is a crucial step. After we've checked for a potential sale on the current day, we update our `min_price_so_far`. This ensures that for all future days, we are always comparing against the absolute lowest price seen up to that point.

## Step-by-Step Execution Trace

### Example: `prices = [7, 1, 5, 3, 6, 4]`

| Current `price` | `min_price_so_far` (start of loop) | `potential_profit` (price - min\_price) | `max_profit` (after update) | `min_price_so_far` (end of loop) |
| :--- | :--- | :--- | :--- | :--- |
| **7** | `inf` | `-inf` | 0 | 7 |
| **1** | 7 | `1 - 7 = -6` | 0 | 1 |
| **5** | 1 | `5 - 1 = 4` | 4 | 1 |
| **3** | 1 | `3 - 1 = 2` | 4 | 1 |
| **6** | 1 | `6 - 1 = 5` | 5 | 1 |
| **4** | 1 | `4 - 1 = 3` | 5 | 1 |

  - After the loop, the final `max_profit` is **5**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in the `prices` list. We iterate through the list only once.

### Space Complexity: O(1)

  - We only use two variables (`min_price_so_far` and `max_profit`) to store our state. The space required is constant and does not grow with the size of the input list.

## Why the Order of Operations Matters

Inside the loop, it is critical that we calculate the potential profit *before* updating the minimum price.

```python
# Correct Order
potential_profit = price - min_price_so_far
max_profit = max(max_profit, potential_profit)
min_price_so_far = min(min_price_so_far, price)
```

If we updated `min_price_so_far` first, we would always be comparing the current price against itself on the day the new minimum is found, resulting in a profit of 0 for that day.

## Key Learning Points

  - Many array problems that seem to require nested loops (`O(n^2)`) can be optimized to a single pass (`O(n)`) by tracking state in a few variables.
  - The "Kadane's Algorithm" pattern (tracking a current best and an overall best) is very powerful and applies to many problems.

## Common Pitfalls Avoided

  - Using a slow `O(n^2)` brute-force solution.
  - Incorrectly calculating `max(prices) - min(prices)`, which ignores the rule that you must buy before you sell.
  - Updating the minimum price *before* calculating the potential profit for the current day.

## Real-World Applications

  - **Financial Analysis**: This is a direct, simplified model for finding the maximum possible gain from one trade in a historical stock dataset.
  - **Data Analysis**: Finding the maximum rise between a trough and a subsequent peak in any time-series data (e.g., temperature, sales volume, user activity).