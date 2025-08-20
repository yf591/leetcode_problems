# 219\. Contains Duplicate II - Solution Explanation

## Problem Overview

Given an array of integers `nums` and an integer `k`, determine if there are two identical numbers in the array whose indices are at most `k` distance apart.

**Condition to Check:**
Find if there exists any pair of indices `i` and `j` such that:

1.  `nums[i] == nums[j]` (the numbers are the same)
2.  `i != j` (they are at different positions)
3.  `abs(i - j) <= k` (the distance between their indices is less than or equal to `k`)

**Examples:**

```python
Input: nums = [1,2,3,1], k = 3
Output: true
Explanation: The number 1 appears at index 0 and index 3. The distance is abs(3 - 0) = 3, which is <= k.

Input: nums = [1,2,3,1,2,3], k = 2
Output: false
Explanation: The duplicate 1s are at indices 0 and 3 (distance 3). The duplicate 2s are at indices 1 and 4 (distance 3). The duplicate 3s are at indices 2 and 5 (distance 3). All distances are > k.
```

## Key Insights

### Efficiently Tracking Past Information

A brute-force approach of checking every pair of elements would be too slow (O(n²)). The key to an efficient solution is to remember information as we iterate through the array. Specifically, for each number we encounter, we only need to know one thing: **"Where was the most recent place I saw this number?"**

A **hash map** (a dictionary in Python) is the perfect data structure for this. We can store each number as a key and its most recent index as the value. This allows us to look up the last-seen index of any number in O(1) average time.

## Solution Approach

This solution iterates through the `nums` array once, using a hash map to store the most recent index of each number encountered.

```python
from typing import List

class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        # Hash map to store the most recent index of each number.
        # Format: {number: index}
        seen_map = {}
        
        # enumerate() gives us both the index 'i' and the value 'num'.
        for i, num in enumerate(nums):
            # Check if we've seen this number before...
            if num in seen_map:
                # ...and if its last seen index is close enough to the current index.
                if i - seen_map[num] <= k:
                    return True
            
            # If the check fails, update the map with the current number's
            # most recent index.
            seen_map[num] = i
            
        # If the loop completes without finding a valid pair, none exists.
        return False
```

**Strategy:**

1.  **Initialize Map**: Create an empty hash map `seen_map`.
2.  **Iterate**: Loop through the `nums` array, getting both the index `i` and the number `num`.
3.  **Check Condition**: For each `num`, check if it's already a key in `seen_map`.
      * If it is, calculate the distance between the current index `i` and the stored index `seen_map[num]`. If this distance is `<= k`, we have found a valid pair and can return `True`.
4.  **Update Map**: If the condition is not met, update the map with the current index: `seen_map[num] = i`. This ensures we always have the most recent index for future comparisons.
5.  **Return False**: If the loop finishes, it means no valid pair was ever found.

## Detailed Code Analysis

### Step 1: Initialization

```python
seen_map = {}
```

  - We start with an empty dictionary. This will store our `{number: last_seen_index}` pairs.

### Step 2: Iteration

```python
for i, num in enumerate(nums):
```

  - `enumerate()` is a clean Python feature that lets us loop through an array and get both the index and the value at the same time, which is exactly what we need.

### Step 3: The `if` Condition

```python
if num in seen_map and i - seen_map[num] <= k:
    return True
```

  - This is the core logic. It's a single line, but it does two things:
    1.  `num in seen_map`: Checks if we have ever seen this number before. This is a fast O(1) lookup.
    2.  `i - seen_map[num] <= k`: If we have seen it, this retrieves its last known index from the map and calculates the distance to the current index `i`. It then checks if this distance is within the allowed range `k`.
  - If both parts are true, we've met the problem's conditions and can stop immediately.

### Step 4: Updating the Map

```python
seen_map[num] = i
```

  - This line is crucial. If the `if` condition was false, we update the map. This overwrites the old index for `num` with the new, more recent index `i`. This is important because we only care about the *most recent* occurrence to check the distance.

## Step-by-Step Execution Trace

### Example: `nums = [1, 2, 3, 1]`, `k = 3`

| `i` | `num` | `seen_map` (start of loop) | `num in seen_map`? | `i - seen_map[num] <= k`? | Action |
| :-- | :-- | :--- | :--- | :--- | :--- |
| **0** | **1** | `{}` | No | - | `seen_map` becomes `{1: 0}` |
| **1** | **2** | `{1: 0}` | No | - | `seen_map` becomes `{1: 0, 2: 1}` |
| **2** | **3** | `{1: 0, 2: 1}` | No | - | `seen_map` becomes `{1: 0, 2: 1, 3: 2}` |
| **3** | **1** | `{1: 0, 2: 1, 3: 2}` | Yes | `3 - 0 <= 3` -\> `3 <= 3` -\> **True** | **Return `True`** |

-----

## Commentary: `seen_map[num]` vs. `seen_map[i]`

This is a great question that gets to the core of how dictionaries (hash maps) work.

A dictionary stores information in **`{key: value}`** pairs. You use a `key` to look up its corresponding `value`.

In our solution, we designed the `seen_map` like this:

  * **Keys**: The numbers from the `nums` array (e.g., `1`, `2`, `3`).
  * **Values**: The most recent index where that number appeared (e.g., `0`, `1`, `2`).

So, our map looks like: `{number: index}`.

### `seen_map[num]` (Correct)

When the code sees `seen_map[num]`, it does the following:

1.  It takes the current number, `num`.
2.  It uses this `num` as a **key** to look up a value in the `seen_map`.
3.  The map returns the **index** that was stored for that number.
    **Example**: If `num` is `1`, `seen_map[1]` correctly returns its stored index, `0`.

### `seen_map[i]` (Incorrect)

If you were to write `seen_map[i]`, you would be telling Python to:

1.  Take the current index, `i`.
2.  Use this index `i` as a **key** to look up a value in the `seen_map`.
    This is not what we want. The keys in our map are the *numbers*, not their indices. Trying to use an index as a key would likely result in a `KeyError` because the map is not designed to be looked up that way.

**In short: We use `num` to find its last-seen `index`.**