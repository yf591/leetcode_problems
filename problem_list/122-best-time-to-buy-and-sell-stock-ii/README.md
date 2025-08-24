# 122\. Best Time to Buy and Sell Stock II - Solution Explanation

## Problem Overview

You are given a list of stock prices, where `prices[i]` is the price on day `i`. The goal is to find the maximum profit you can achieve by buying and selling the stock multiple times.

**Key Rules:**

  - You can complete as many transactions as you like.
  - You must sell a stock before you can buy another one (you can only hold one share at a time).
  - You are allowed to buy and immediately sell on the same day.

**Examples:**

```python
Input: prices = [7,1,5,3,6,4]
Output: 7
Explanation:
Buy on day 2 (price=1), sell on day 3 (price=5). Profit = 4.
Then, buy on day 4 (price=3), sell on day 5 (price=6). Profit = 3.
Total profit = 4 + 3 = 7.

Input: prices = [1,2,3,4,5]
Output: 4
Explanation: Buy on day 1 (price=1) and sell on day 5 (price=5). Total profit = 4.
```

## Key Insights

### The Power of a Greedy Approach

This problem seems complex because you have to decide when to buy and when to sell. However, the ability to transact as many times as you want simplifies it dramatically.

The key insight is that the total profit over a long upward trend is simply the sum of all the individual day-to-day price increases within that trend.

For example, the profit from buying at `1` and selling at `5` (`5 - 1 = 4`) is mathematically identical to the sum of these daily transactions:

  - `(2 - 1) + (3 - 2) + (4 - 3) + (5 - 4) = 1 + 1 + 1 + 1 = 4`

This means we don't need to worry about finding the best "peaks" and "valleys." We can adopt a simple **greedy** strategy: if there's a profit to be made from one day to the next, we take it.

## Solution Approach

This solution iterates through the `prices` list once, accumulating the profit from every single day-to-day price increase.

```python
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        total_profit = 0
        
        # Iterate through the prices starting from the second day.
        for i in range(1, len(prices)):
            # If today's price is higher than yesterday's price...
            if prices[i] > prices[i - 1]:
                # ...it represents a profitable opportunity. Add the profit.
                total_profit += prices[i] - prices[i - 1]
                
        return total_profit
```

**Strategy:**

1.  **Initialize Profit**: Start with `total_profit = 0`.
2.  **Iterate and Compare**: Loop through the prices from the second day onwards. Compare each day's price with the previous day's price.
3.  **Accumulate Gains**: If a price increase is found, add that gain to the `total_profit`. If the price decreases or stays the same, do nothing.
4.  **Return**: The final `total_profit` is the maximum possible profit.

## Detailed Code Analysis

### Step 1: Initialization

```python
total_profit = 0
```

  - We start our `total_profit` at 0. If there are no profitable opportunities, this will be the value we return.

### Step 2: Iteration

```python
for i in range(1, len(prices)):
```

  - The loop starts at index `1` (the second day). This is necessary so that we can always access the previous day's price at `prices[i - 1]`.

### Step 3: The Core Logic

```python
if prices[i] > prices[i - 1]:
    total_profit += prices[i] - prices[i - 1]
```

  - This is the heart of the greedy algorithm.
  - `prices[i] > prices[i - 1]` checks if there was a price increase from yesterday to today.
  - If there was, `prices[i] - prices[i - 1]` calculates that positive gain, and we add it to our running total. This is conceptually the same as buying yesterday and selling today.

## Step-by-Step Execution Trace

### Example: `prices = [7, 1, 5, 3, 6, 4]`

| `i` | `prices[i-1]` | `prices[i]` | `prices[i] > prices[i-1]`? | `profit_added` | `total_profit` |
| :-- | :--- | :--- | :--- | :--- | :--- |
| **1** | 7 | 1 | False | 0 | 0 |
| **2** | 1 | 5 | True | `5 - 1 = 4` | **4** |
| **3** | 5 | 3 | False | 0 | 4 |
| **4** | 3 | 6 | True | `6 - 3 = 3` | **7** |
| **5** | 6 | 4 | False | 0 | 7 |

  - The loop finishes. The function returns the final `total_profit`, which is **7**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of elements in the `prices` list. We iterate through the list exactly once.

### Space Complexity: O(1)

  - We only use a single variable (`total_profit`). The space required is constant and does not grow with the size of the input list.

## Why the Greedy Approach Works

The greedy strategy of summing all positive daily gains is optimal because of the problem's rules. Since you can buy and sell on the same day, you can capture the profit from `Day A` to `Day B` and then immediately "re-buy" at `Day B`'s price to capture the profit to `Day C`. This is the same as just capturing the total profit from `Day A` to `Day C`.

  - `(price_B - price_A) + (price_C - price_B) = price_C - price_A`
    Because all the intermediate buy/sell points cancel out, summing the small gains is equivalent to buying at the start of an upward trend and selling at the end.

## Key Learning Points

  - Recognizing when a complex-sounding problem has a very simple, greedy solution.
  - The power of focusing on local changes (day-to-day) to solve a global optimization problem (total maximum profit).
  - This problem highlights how changing a single rule (allowing multiple transactions) can completely change the optimal strategy compared to the version where only one transaction is allowed.

## Common Pitfalls Avoided

  - **Overcomplicating the problem**: A common mistake is to try to find all the "valleys" (low points to buy) and "peaks" (high points to sell). While this works, it's much more complex to implement than simply summing the daily gains, and it yields the exact same result.
  - **Applying the wrong strategy**: Trying to use the solution from "Best Time to Buy and Sell Stock I" (finding a single min-buy-price and max-sell-price) will not work here.