# 739\. Daily Temperatures - Solution Explanation

## Problem Overview

You are given a list of daily `temperatures`. The task is to return a new list, `answer`, where `answer[i]` is the number of days you would have to wait, starting from day `i`, to get a warmer temperature. If no warmer day exists in the future, the answer for that day should be `0`.

**Examples:**

```python
Input: temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
Output: [1, 1, 4, 2, 1, 1, 0, 0]

Explanation:
- On day 0 (73), you wait 1 day to get 74.
- On day 1 (74), you wait 1 day to get 75.
- On day 2 (75), you wait 4 days to get 76.
- On day 3 (71), you wait 2 days to get 72.
- ...and so on.
```

## Key Insights

### 1\. The Inefficient Brute-Force Approach

The most obvious solution is to use nested loops. For each day `i`, you loop forward with a second pointer `j` until you find a day `j` where `temperatures[j] > temperatures[i]`.

  - **The Problem**: This is an `O(n²)` solution. Given the constraint `n <= 10^5`, an `n²` solution would be far too slow and would time out. We need a solution that runs in `O(n)` time.

### 2\. The "Waiting List" -\> The Stack

To get an `O(n)` solution, we need to iterate through the array only once. Let's think about the problem from a different perspective. As we iterate through the days, each day's temperature might be the *answer* for previous days that are still "waiting" for a warmer day.

  - Imagine a "waiting list" of days that haven't found their warmer day yet.
  - When we process a new day, `current_day`, we check if its temperature, `current_temp`, can resolve any of the days on our waiting list.
  - Which days can it resolve? It can resolve all the days on the list that were cooler than `current_temp`.
  - What is the order of this list? If we have a sequence like `[75, 71, 69]`, all three are waiting. When `72` arrives, it first checks against `69`, then `71`. It's a **Last-In, First-Out (LIFO)** process.
  - This "waiting list" is a **stack**.

### 3\. The Monotonic Stack

The stack will store the **indices** of the days we are processing. As we push new day-indices onto the stack, we will ensure that the temperatures corresponding to these indices are always **decreasing**. This is called a **Monotonic Decreasing Stack**.

  - **Why?** If our stack has `[75, 71]` and the next day is `72`, the `72` is warmer than `71`, so we've found the answer for `71`. We can pop `71`. Then we check `72` against `75`. It's not warmer, so we stop. The stack now holds `[75]`, and we add `72`. The stack becomes `[75, 72]`, which is still decreasing.
  - This ensures that any new temperature only needs to check the top of the stack.

## Solution Approach

This solution iterates through the `temperatures` array once. It uses a stack to store the *indices* of days that are waiting for a warmer temperature. When a warmer day arrives, it pops all cooler days from the stack and calculates their wait time.

```python
from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        
        # 1. Initialize the answer array with all 0s. This is the default
        #    value for days that never find a warmer day.
        answer = [0] * n
        
        # 2. The stack will store the *indices* of the days.
        stack = [] 

        # 3. Iterate through the array once, with both index and temperature
        for current_day, current_temp in enumerate(temperatures):
            
            # 4. Check if this day is the answer for any day on the stack.
            #    This loop runs as long as the stack is not empty AND
            #    the current temperature is warmer than the temperature
            #    of the day at the top of the stack.
            while stack and current_temp > temperatures[stack[-1]]:
                # 5. We found a warmer day!
                prev_day_index = stack.pop()
                
                # 6. Calculate the wait time and store it in the answer.
                answer[prev_day_index] = current_day - prev_day_index
            
            # 7. Add the current day's index to the stack, as it is now
            #    waiting for a warmer day.
            stack.append(current_day)
            
        # 8. Any indices left on the stack never found a warmer day.
        #    Their answer is already 0, so we are done.
        return answer
```

## Detailed Code Analysis

### Step 1: Initialization

```python
answer = [0] * n
stack = []
```

  - `answer = [0] * n`: We create our result array, pre-filled with `0`. This is perfect because any index left on the stack at the end should have an answer of `0`, so we don't need to do any extra work.
  - `stack = []`: We initialize an empty list to use as our stack.

### Step 2: The Main Loop

```python
for current_day, current_temp in enumerate(temperatures):
```

  - We use `enumerate` to get both the index (`current_day`) and the value (`current_temp`) in a single, clean loop.

### Step 3: The Core "while" Loop (The Monotonic Logic)

```python
while stack and current_temp > temperatures[stack[-1]]:
```

  - This is the heart of the algorithm. It runs *before* we add the new day to the stack.
  - `stack`: First, we check if the stack is not empty. If it is, there are no days "waiting" for an answer, so we can skip this.
  - `current_temp > temperatures[stack[-1]]`: This is the main comparison. `stack[-1]` gives us the index at the top of the stack (the most recent day we added). We use that index to get its temperature and compare it to the `current_temp`.

### Step 4: Processing a "Waiting" Day

```python
prev_day_index = stack.pop()
answer[prev_day_index] = current_day - prev_day_index
```

  - If the `while` loop condition is true (the current day is warmer):
  - `prev_day_index = stack.pop()`: We pop the index of the waiting day from the stack.
  - `answer[prev_day_index] = ...`: We calculate the wait time, `current_day - prev_day_index`, and store it in the `answer` array at the correct position.
  - The `while` loop continues. This is crucial: a single hot day (like 76 in the example) can resolve *multiple* cooler days that were waiting on the stack (e.g., 72, 71, 69, 75).

### Step 5: Adding the Current Day

```python
stack.append(current_day)
```

  - After the `while` loop finishes (either because the stack became empty or the new temp was not warmer than the top), we add the `current_day`'s index to the stack. It now becomes a "waiting" day, hoping for a warmer day in the future.

## Step-by-Step Execution Trace

Let's trace `temperatures = [73, 74, 75, 71, 69, 72, 76, 73]` with extreme detail.

### **Initial State:**

  - `answer = [0, 0, 0, 0, 0, 0, 0, 0]`
  - `stack = []`

| `i` (Day) | `temp` (Temp)| `stack` (Start) | `while` loop: `temp > temp_at_top`? | Action in `while` | `stack` (End) | `answer` (End) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0** | **73** | `[]` | No (stack empty) | - | `[0]` | `[0,0,0,0,0,0,0,0]` |
| **1** | **74** | `[0]` | `74 > 73` -\> **True** | `i=0` popped. `ans[0]=1-0=1` | `[1]` | `[1,0,0,0,0,0,0,0]` |
| **2** | **75** | `[1]` | `75 > 74` -\> **True** | `i=1` popped. `ans[1]=2-1=1` | `[2]` | `[1,1,0,0,0,0,0,0]` |
| **3** | **71** | `[2]` | `71 > 75` -\> False | - | `[2, 3]` | `[1,1,0,0,0,0,0,0]` |
| **4** | **69** | `[2, 3]` | `69 > 71` -\> False | - | `[2, 3, 4]` | `[1,1,0,0,0,0,0,0]` |
| **5** | **72** | `[2,3,4]` | `72 > 69` -\> **True** | `i=4` popped. `ans[4]=5-4=1` | `[2, 3]` | `[1,1,0,0,1,0,0,0]` |
| | | `[2, 3]` | `72 > 71` -\> **True** | `i=3` popped. `ans[3]=5-3=2` | `[2]` | `[1,1,0,2,1,0,0,0]` |
| | | `[2]` | `72 > 75` -\> False | - | `[2, 5]` | `[1,1,0,2,1,0,0,0]` |
| **6** | **76** | `[2, 5]` | `76 > 72` -\> **True** | `i=5` popped. `ans[5]=6-5=1` | `[2]` | `[1,1,0,2,1,1,0,0]` |
| | | `[2]` | `76 > 75` -\> **True** | `i=2` popped. `ans[2]=6-2=4` | `[]` | `[1,1,4,2,1,1,0,0]` |
| | | `[]` | No (stack empty) | - | `[6]` | `[1,1,4,2,1,1,0,0]` |
| **7** | **73** | `[6]` | `73 > 76` -\> False | - | `[6, 7]` | `[1,1,4,2,1,1,0,0]` |

  - **Final Step**: The loop finishes. `stack` is `[6, 7]`. `answer` is `[1,1,4,2,1,1,0,0]`. The `0`s for indices 6 and 7 are the correct default.
  - The function returns **`[1,1,4,2,1,1,0,0]`**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the number of temperatures. This is the main advantage of this solution.
  - Although there is a nested `while` loop inside the `for` loop, its behavior is **amortized `O(1)`**.
  - This is because each index (`current_day`) is pushed onto the stack exactly once and popped from the stack at most once. Therefore, the total number of stack operations (push and pop) across the *entire* run of the algorithm is at most `2n`. This gives a total time complexity of `O(n)`.

### Space Complexity: O(n)

  - The space is determined by the size of the `stack`.
  - In the worst-case scenario, if the temperatures are strictly decreasing (e.g., `[90, 80, 70, 60]`), every index will be pushed onto the stack and none will be popped until the end.
  - Therefore, the stack can grow to a size of `n`, resulting in `O(n)` space complexity.