# 1207\. Unique Number of Occurrences - Solution Explanation

## Problem Overview

You are given an array of integers `arr`. The task is to determine if the **number of occurrences** (the frequency) of each distinct value in the array is itself unique.

**The Question in Simple Terms:**
First, count how many times each number appears. Then, look at those counts. Are all of those counts different from each other?

**Examples:**

```python
Input: arr = [1,2,2,1,1,3]
Output: true
Explanation:
- The number 1 appears 3 times.
- The number 2 appears 2 times.
- The number 3 appears 1 time.
The list of occurrences is [3, 2, 1]. All these counts are unique.

Input: arr = [1,2]
Output: false
Explanation:
- The number 1 appears 1 time.
- The number 2 appears 1 time.
The list of occurrences is [1, 1]. The count '1' is repeated, so it's not unique.
```

## Key Insights

### A Two-Step Process

The problem can be broken down into two clear, sequential steps:

1.  **Count Frequencies**: First, we need to go through the input array and count the occurrences of each number. For `[1,2,2,1,1,3]`, we need to generate the counts: `1 -> 3 times`, `2 -> 2 times`, `3 -> 1 time`.
2.  **Check Uniqueness of Counts**: Second, we take the list of counts we just generated (`[3, 2, 1]`) and check if all the values *in that list* are unique.

### Data Structures for Each Step

  - **For Step 1 (Counting)**: The best tool for counting item frequencies is a **hash map** (a `dict` in Python). Python's specialized `collections.Counter` is even better, as it's designed for this exact purpose.
  - **For Step 2 (Checking Uniqueness)**: The best tool for checking if a collection of items is unique is a **hash set** (a `set` in Python). Sets, by definition, only store unique items.

## Solution Approach

This solution directly implements the two-step process. It uses `collections.Counter` to get the frequencies, and then compares the number of frequencies to the number of *unique* frequencies to see if they match.

```python
import collections
from typing import List

class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        # Step 1: Count the occurrences of each number in the array.
        counts = collections.Counter(arr)
        
        # Step 2: Get a list of just the occurrence counts.
        occurrences = counts.values()
        
        # Step 3: Check if all the counts in the 'occurrences' list are unique.
        return len(occurrences) == len(set(occurrences))
```

## Detailed Code Analysis

### Step 1: Counting Frequencies

```python
counts = collections.Counter(arr)
```

  - `collections.Counter()` is a powerful tool that takes an iterable (like our list `arr`) and instantly produces a dictionary-like object that maps each unique item to its frequency.
  - **Example**: If `arr = [1,2,2,1,1,3]`, then after this line, `counts` will be `Counter({1: 3, 2: 2, 3: 1})`.

### Step 2: Extracting the Counts

```python
occurrences = counts.values()
```

  - We only care about the counts, not the original numbers they correspond to. The `.values()` method gives us a collection of just the values from our `counts` map.
  - **Example**: For `counts = {1: 3, 2: 2, 3: 1}`, `occurrences` will be a view object representing the values `[3, 2, 1]`.

### Step 3: The Uniqueness Check

```python
return len(occurrences) == len(set(occurrences))
```

  - This is the clever and concise final step.
  - `len(occurrences)`: This gives us the total number of frequency counts we have. For `[3, 2, 1]`, this is `3`.
  - `set(occurrences)`: This converts the list of frequencies into a set. A set, by definition, automatically discards any duplicates.
  - `len(set(occurrences))`: This gives us the number of *unique* frequency counts.
  - By comparing the two lengths, we can determine if any duplicates were present.
      - If `len(list) == len(set)`: No elements were discarded, so all counts were unique.
      - If `len(list) != len(set)`: Some elements were discarded, meaning there were duplicate counts.

## Why the `len(list) == len(set)` Trick Works

This is a beautiful Python idiom for checking if all elements in a list are unique.

  - A **`set`** is a container that, by its very nature, can only hold unique items.
  - When you create a set from a list, like `set(my_list)`, Python iterates through `my_list` and adds each item to the set. If an item is already in the set, it's simply ignored.

**Example A (Unique values):**

  - `my_list = [3, 2, 1]`
  - `len(my_list)` is **3**.
  - `set(my_list)` becomes `{1, 2, 3}`.
  - `len(set(my_list))` is **3**.
  - `3 == 3` is **True**.

**Example B (Duplicate values):**

  - `my_list = [1, 1, 2]`
  - `len(my_list)` is **3**.
  - `set(my_list)` becomes `{1, 2}`. The duplicate `1` was discarded.
  - `len(set(my_list))` is **2**.
  - `3 == 2` is **False**.

## Step-by-Step Execution Trace

### Example 1 (True case): `arr = [1, 2, 2, 1, 1, 3]`

| Step | Code | Value | Explanation |
| :--- | :--- | :--- | :--- |
| **1** | `counts = collections.Counter(arr)` | `{1: 3, 2: 2, 3: 1}` | A frequency map is created from the input array. |
| **2** | `occurrences = counts.values()` | `dict_values([3, 2, 1])` | We extract just the counts (the frequencies). |
| **3** | `len(occurrences)` | `3` | There are 3 different frequency counts in total. |
| **4** | `set(occurrences)` | `{1, 2, 3}` | We create a set from the counts, which removes duplicates. |
| **5** | `len(set(occurrences))` | `3` | The number of unique frequency counts is 3. |
| **6** | `return len(...) == len(set(...))`| `3 == 3` -\> **`True`** | Since the lengths are equal, all occurrences were unique. |

### Example 2 (False case): `arr = [1, 2]`

| Step | Code | Value | Explanation |
| :--- | :--- | :--- | :--- |
| **1** | `counts = collections.Counter(arr)` | `{1: 1, 2: 1}` | A frequency map is created. |
| **2** | `occurrences = counts.values()` | `dict_values([1, 1])` | We extract the counts. Notice the duplicate `1`. |
| **3** | `len(occurrences)` | `2` | There are 2 frequency counts in total. |
| **4** | `set(occurrences)` | `{1}` | The duplicate `1` is removed when creating the set. |
| **5** | `len(set(occurrences))` | `1` | The number of unique frequency counts is only 1. |
| **6** | `return len(...) == len(set(...))`| `2 == 1` -\> **`False`** | Since the lengths are not equal, the occurrences were not unique. |

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the length of the input `arr`.
  - `collections.Counter(arr)` takes `O(n)` time to iterate through the array once.
  - `.values()`, `set()`, and `len()` operations take time proportional to the number of *unique* elements in the array, which in the worst case is `O(n)`.

### Space Complexity: O(k)

  - Where `k` is the number of unique elements in `arr`. The `Counter` object will store `k` key-value pairs.