# 875\. Koko Eating Bananas - Solution Explanation

## Problem Overview

You are given `n` piles of bananas, `piles[i]`, and a time limit, `h` hours. Koko can eat at a speed of `k` bananas per hour. If a pile has fewer than `k` bananas, she eats them all in one hour and waits for the rest of the hour.

The goal is to find the **minimum integer eating speed `k`** such that Koko can eat all the bananas within `h` hours.

**Examples:**

```python
Input: piles = [3,6,7,11], h = 8
Output: 4
Explanation:
- If k=1, time = 3+6+7+11 = 27 (too slow).
- If k=3, time = ceil(3/3)+ceil(6/3)+ceil(7/3)+ceil(11/3) = 1+2+3+4 = 10 (too slow).
- If k=4, time = ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4) = 1+2+2+3 = 8 (just in time!).
k=4 is the minimum possible speed.

Input: piles = [30,11,23,4,20], h = 5
Output: 30
Explanation: h = 5, which is the same as the number of piles. Koko must eat one pile per hour. To do this, her speed must be at least as high as the largest pile, which is 30.
```

## Deep Dive: What is Binary Search? 🧠

**Binary Search** is a an extremely fast search algorithm that operates on a **sorted** search space. Its time complexity is `O(log n)`.

**Analogy (The Dictionary):**
Imagine finding the word "Koko" in a 1000-page dictionary.

1.  **Naive (Linear) Search (Slow: `O(n)`):** You start at page 1 and read every page until you find "Koko".
2.  **Binary Search (Fast: `O(log n)`):**
    a.  You open the dictionary to the middle, (page 500). You see words starting with 'M'.
    b.  You know 'K' comes *before* 'M', so you **discard the entire second half** of the book (pages 500-1000).
    c.  You repeat the process on the remaining first half (pages 1-499), opening to its middle (page 250). You see 'G'.
    d.  You know 'K' comes *after* 'G', so you **discard the entire first half** of this new section (pages 1-250).

By repeatedly cutting the search space in half, you find the word in a tiny number of steps.

### Binary Search on the Answer

This problem has a special twist. We are not searching for a value *inside* the `piles` array. We are searching for the **answer** itself. The "search space" is the range of *all possible speeds `k`*.

This works because the problem has a **monotonic property**:

  - As the speed `k` **increases**, the total hours required **decreases**.
  - This means the "search space of answers" is *implicitly sorted*. We can search on it\!

## Key Insights for This Problem

### 1\. Identifying the Search Space for `k`

We need to find the `low` and `high` bounds for our binary search.

  - **Lowest possible speed**: Koko must eat at least one banana per hour. So, `left = 1`.
  - **Highest possible speed**: What's the *fastest* Koko would ever *need* to go? The problem guarantees `h` is at least as large as the number of piles. This means the slowest valid solution is to eat one pile per hour. To do that, her speed must be equal to the largest pile. `right = max(piles)`.

Our search space for the answer `k` is the range `[1, max(piles)]`.

### 2\. The "Check" Function

For binary search to work, we need a way to test a `mid` value from our search space.

  - **Question**: If Koko's speed is `k`, can she finish in `h` hours?
  - **Logic**: We can write a function `can_finish(k)`:
    1.  `total_hours = 0`
    2.  For each `pile` in `piles`:
          - Time for this pile = `math.ceil(pile / k)`
          - `total_hours += time_for_this_pile`
    3.  `return total_hours <= h`

### 3\. The `ceil()` Trick (Integer Math)

Calculating `math.ceil(a / b)` using floating-point math can be slow and sometimes has precision issues. There is a "magic formula" using only integer arithmetic to get the same result:
`ceil(a / b)` is equivalent to `(a + b - 1) // b`

  - **Example `7 / 3`**:
      - `math.ceil(7 / 3)` -\> `math.ceil(2.33)` -\> `3`
      - `(7 + 3 - 1) // 3` -\> `9 // 3` -\> `3` (Correct\!)
  - **Example `6 / 3`**:
      - `math.ceil(6 / 3)` -\> `math.ceil(2.0)` -\> `2`
      - `(6 + 3 - 1) // 3` -\> `8 // 3` -\> `2` (Correct\!)

This integer-only formula is much faster.

## Solution Approach

This solution implements a **Binary Search on the Answer**. It searches for the smallest `k` in the range `[1, max(piles)]`. For each `k` it tests, it calculates the total hours using the integer-based `ceil` formula.

```python
import math
from typing import List

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        
        # --- Step 1: Define the search space for the speed 'k' ---
        
        # The slowest possible speed is 1.
        left = 1
        # The fastest *necessary* speed is eating the largest pile in one hour.
        right = max(piles)
        
        # This will store the minimum valid speed we've found so far.
        # We can initialize it to the max possible speed.
        min_speed = right
        
        # --- Step 2: Perform binary search on the answer (speed 'k') ---
        while left <= right:
            # Get the middle speed to test.
            speed = (left + right) // 2
            
            # --- Step 3: Check if this 'speed' is valid (our "Check" function) ---
            total_hours = 0
            for pile in piles:
                # Calculate hours for this pile using the fast integer 'ceil' formula.
                total_hours += (pile + speed - 1) // speed
            
            # --- Step 4: Adjust the search space based on the check ---
            if total_hours <= h:
                # This speed is valid (Koko can finish in time).
                # This is a potential answer, so we save it.
                min_speed = speed
                
                # Now, we try to find an even *slower* speed.
                # We discard the right half.
                right = speed - 1
            else:
                # This speed is too slow (total_hours > h).
                # Koko cannot finish. We must search for a *faster* speed.
                # We discard the left half.
                left = speed + 1
                
        # After the loop, 'min_speed' holds the smallest 'k' that worked.
        return min_speed
```

## Detailed Code Analysis

### Step 1: Search Space

```python
left = 1
right = max(piles)
min_speed = right
```

  - `left` is the absolute minimum speed.
  - `right` is the absolute maximum *necessary* speed. We know `k = max(piles)` is a guaranteed solution (since `h >= len(piles)`), so our answer must be in the range `[1, right]`.
  - `min_speed = right`: We initialize our answer to a *known valid speed*. The binary search will then work to find a *better* (smaller) valid speed.

### Step 2: The Binary Search Loop

```python
while left <= right:
```

  - This is a standard binary search loop. It continues as long as our search space (`left` to `right`) is valid.

### Step 3: The Check Function

```python
speed = (left + right) // 2
total_hours = 0
for pile in piles:
    total_hours += (pile + speed - 1) // speed
```

  - `speed = (left + right) // 2`: We pick the midpoint of our current search range to test.
  - `total_hours = 0`: We initialize an accumulator for the hours.
  - The `for` loop sums the time needed for each pile, using the `(pile + speed - 1) // speed` formula to calculate the ceiling of the division.

### Step 4: Adjusting the Search Space

```python
if total_hours <= h:
    min_speed = speed
    right = speed - 1
else:
    left = speed + 1
```

  - This is the core logic of the binary search.
  - **`if total_hours <= h:`**: The `speed` we tested is **valid**. It's a possible answer.
      - `min_speed = speed`: We record this valid speed as our *new best answer*.
      - `right = speed - 1`: We are looking for the *minimum* speed, so we must try to find an even smaller one. We "discard" the current speed and the entire right half of the search space, and continue searching in the left half `[left, speed - 1]`.
  - **`else:`** (`total_hours > h`): The `speed` we tested is **invalid** (too slow).
      - This speed, and all speeds *smaller* than it, are invalid.
      - We must search for a faster speed. We "discard" the current speed and the entire left half, and continue searching in the right half `[speed + 1, right]`.

### Step 5: The Final Return

```python
return min_speed
```

  - When the `while` loop finishes (`left > right`), `min_speed` will hold the last valid speed we recorded. Because we *always* search to the left (`right = speed - 1`) after finding a valid speed, this is guaranteed to be the *minimum* valid speed.

## Step-by-Step Execution Trace

Let's trace `piles = [3, 6, 7, 11]`, `h = 8`.

### **Initial State:**

  - `left = 1`
  - `right = max(piles) = 11`
  - `min_speed = 11`

-----

### **Loop 1:**

  - `speed = (1 + 11) // 2 = 6`
  - Check `k=6`:
      - `total_hours = (3+6-1)//6 + (6+6-1)//6 + (7+6-1)//6 + (11+6-1)//6`
      - `total_hours = (8//6) + (11//6) + (12//6) + (16//6)`
      - `total_hours = 1 + 1 + 2 + 2 = 6`
  - Check: `6 <= 8`? **True**.
  - `min_speed` becomes `6`.
  - `right = speed - 1` -\> `right = 5`.

### **Loop 2:**

  - `speed = (1 + 5) // 2 = 3`
  - Check `k=3`:
      - `total_hours = (3+3-1)//3 + (6+3-1)//3 + (7+3-1)//3 + (11+3-1)//3`
      - `total_hours = (5//3) + (8//3) + (9//3) + (13//3)`
      - `total_hours = 1 + 2 + 3 + 4 = 10`
  - Check: `10 <= 8`? **False**.
  - `left = speed + 1` -\> `left = 4`.

### **Loop 3:**

  - `speed = (4 + 5) // 2 = 4`
  - Check `k=4`:
      - `total_hours = (3+4-1)//4 + (6+4-1)//4 + (7+4-1)//4 + (11+4-1)//4`
      - `total_hours = (6//4) + (9//4) + (10//4) + (14//4)`
      - `total_hours = 1 + 2 + 2 + 3 = 8`
  - Check: `8 <= 8`? **True**.
  - `min_speed` becomes `4`.
  - `right = speed - 1` -\> `right = 3`.

### **Loop 4:**

  - `speed = (4 + 3) // 2 = 3` (Wait, `left=4, right=3`)
  - The loop condition `while left <= right` (`4 <= 3`) is **False**. The loop terminates.

### **Final Result:**

  - The function returns the last value stored in `min_speed`.
  - Return **4**.

## Performance Analysis

### Time Complexity: O(n \* log(m))

  - Where `n` is the number of piles (`len(piles)`) and `m` is the maximum value in `piles`.
  - The binary search on the answer space runs `O(log m)` times.
  - Inside each step of the binary search, we have a "check" function that iterates through all `n` piles. This takes `O(n)` time.
  - Total Time = `O(n * log m)`.

### Space Complexity: O(1)

  - We only use a few variables to store our state (`left`, `right`, `min_speed`, `speed`, `total_hours`). The space required is constant.