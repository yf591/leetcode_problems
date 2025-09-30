# 128\. Longest Consecutive Sequence - Solution Explanation

## Problem Overview

You are given an **unsorted** array of integers `nums`. The task is to find the length of the longest sequence of consecutive elements.

**Key Definitions:**

  - **Consecutive Sequence**: A sequence of numbers that follow each other without gaps, like `[1, 2, 3, 4]`.
  - **The Goal**: The final answer is just the *length* of this longest sequence, not the sequence itself.

**Key Constraint:**

  - You must write an algorithm that runs in **`O(n)` time**.

**Examples:**

```python
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive sequence is [1, 2, 3, 4].

Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9
Explanation: The longest consecutive sequence is [0, 1, 2, 3, 4, 5, 6, 7, 8].
```

## Key Insights

### The `O(n log n)` Trap

The most intuitive approach is to first **sort** the array. For `[100,4,200,1,3,2]`, this would give `[1,2,3,4,100,200]`. After sorting, you could easily iterate through this new array in `O(n)` time to find the longest consecutive run. However, the sorting step itself takes `O(n log n)` time, which violates the problem's strict `O(n)` requirement.

### The `O(n)` Insight: Hash Set and Sequence Starts

To achieve `O(n)` time, we need a way to check if a number exists in the input in `O(1)` (constant) time. A **hash set** is the perfect data structure for this.

1.  **Fast Lookups**: By first putting all the numbers into a `set`, we can later check `if some_number in my_set` almost instantly.
2.  **The "Sequence Start" Optimization**: If we iterate through our set and start counting a sequence from every single number, we will do a lot of redundant work. For the sequence `[1, 2, 3, 4]`, we don't want to start counting at 2, 3, and 4, because they are part of a sequence we already found starting at 1. The key insight is to **only start counting when we find the true beginning of a sequence**.
      - How do we know if a number `num` is the start of a sequence? It's a start if the number `num - 1` is **not** present in our set.

## Solution Approach

This solution uses a hash set to enable fast lookups and an intelligent check to ensure we only count each consecutive sequence once, starting from its beginning.

```python
from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # Step 1: Create a set for O(1) lookups and to handle duplicates.
        num_set = set(nums)
        max_length = 0
        
        # Step 2: Iterate through each unique number.
        for num in num_set:
            # Step 3: Check if it's the start of a sequence.
            if (num - 1) not in num_set:
                # This number is a starting point. Let's count its sequence.
                current_length = 1
                current_num = num
                
                # Step 4: Count the length of the sequence.
                while current_num + 1 in num_set:
                    current_length += 1
                    current_num += 1
                
                # Step 5: Update the maximum length found.
                max_length = max(max_length, current_length)
                
        return max_length
```

## Deep Dive: The Power of Python's `set()`

  * **What is a Set?** 🗃️
    A `set` is a data structure, like a list, but it's an **unordered** collection of **unique** items. Think of it as a bag of unique marbles—you can't have two of the exact same marble, and there's no defined order.

    ```python
    my_list = [100, 4, 200, 1, 3, 2, 4] # Has a duplicate 4
    my_set = set(my_list) # my_set is now {1, 2, 3, 4, 100, 200}
    ```

  * **Why is it so Fast? (The Magic of Hashing)**
    The most important feature of a set is its speed. It is implemented using a **hash table**. This means that to check if an item exists, it doesn't scan through all the items like a list does. Instead, it converts the item into a "hash" which points it directly to the location where the item should be.

      - `item in my_list`: This is an `O(n)` operation. The computer might have to look at every single item.
      - `item in my_set`: This is an `O(1)` (constant time) operation on average. It's almost instantaneous, no matter how large the set is.

This speed is what allows our solution to meet the `O(n)` time constraint.

## Detailed Code Analysis

### Step 1: Initialization

```python
num_set = set(nums)
max_length = 0
```

  - `num_set = set(nums)`: This is our crucial pre-processing step. We convert the entire input list into a set. This takes `O(n)` time. Now, any check like `if x in num_set:` will be super fast.
  - `max_length = 0`: We initialize our answer variable.

### Step 2: The Main Loop

```python
for num in num_set:
```

  - We iterate through each unique number from the input.

### Step 3: The "Sequence Start" Check

```python
if (num - 1) not in num_set:
```

  - This is the most important optimization. Before we start a potentially long counting process, we do one quick `O(1)` check.
  - We ask, "Does the number just before this one exist?" If it does, then our current `num` is not the start of a sequence, so we can ignore it and move to the next number in the `for` loop. This check prevents us from recounting the same sequence multiple times.

### Step 4: Counting the Sequence

```python
current_length = 1
current_num = num
while current_num + 1 in num_set:
    current_length += 1
    current_num += 1
```

  - This block of code only ever runs if we've confirmed that `num` is a true starting point.
  - The `while` loop checks for the next number in the sequence (`current_num + 1`). Because `in num_set` is so fast, this loop can quickly count the length of the entire consecutive run.

### Step 5: Updating the Maximum

```python
max_length = max(max_length, current_length)
```

  - After a sequence has been fully counted, we compare its length to the maximum length we've found so far and update it if the new one is longer.

## Step-by-Step Execution Trace

Let's trace the algorithm with `nums = [100, 4, 200, 1, 3, 2]` with extreme detail.

1.  **Initialization**:

      * `num_set` = `{100, 4, 200, 1, 3, 2}`
      * `max_length = 0`

2.  **The Loop**: The `for` loop will iterate through the numbers in the set (the order is not guaranteed, but the result is the same).

| `num` | `(num - 1)` in `num_set`? | Action | `current_length` | `max_length` |
| :--- | :--- | :--- | :--- | :--- |
| **100**| `99 not in num_set` -\> **True** | It's a start. `while 101 in num_set?` -\> No. | 1 | `max(0, 1) = 1` |
| **4** | `3 in num_set` -\> **True** | Not a start. Skip. | - | 1 |
| **200**| `199 not in num_set` -\> **True** | It's a start. `while 201 in num_set?` -\> No. | 1 | `max(1, 1) = 1` |
| **1** | `0 not in num_set` -\> **True** | **It's a start.**<br>- `while 2 in num_set?` Yes. `len=2`.<br>- `while 3 in num_set?` Yes. `len=3`.<br>- `while 4 in num_set?` Yes. `len=4`.<br>- `while 5 in num_set?` No. Loop ends. | 4 | `max(1, 4) = 4` |
| **3** | `2 in num_set` -\> **True** | Not a start. Skip. | - | 4 |
| **2** | `1 in num_set` -\> **True** | Not a start. Skip. | - | 4 |

3.  **Final Step**: The `for` loop finishes.

<!-- end list -->

  - The function returns the final `max_length`, which is **4**.

## Performance Analysis

### Time Complexity: O(n)

  - Building the initial `num_set` takes `O(n)` time.
  - The main `for` loop iterates through `k` unique numbers (`k <= n`).
  - Although there is a nested `while` loop, its body only executes `n` times in total across the entire run of the algorithm. This is because we only enter the `while` loop for the starting number of a sequence. Every number is visited at most twice (once by the `for` loop and once by the `while` loop).
  - Therefore, the total complexity is `O(n) + O(n) = O(n)`.

### Space Complexity: O(n)

  - In the worst case (if all numbers in `nums` are unique), the `num_set` will store `n` elements. The space required is proportional to the input size.