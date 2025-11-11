# 2300\. Successful Pairs of Spells and Potions - Solution Explanation

## Problem Overview

You are given two arrays of positive integers: `spells` and `potions`, and a target integer `success`.

**The Goal:**
For each spell in the `spells` array, you need to count how many potions in the `potions` array can form a "successful pair."

**Success Condition:**
A pair `(spell, potion)` is successful if:
$$\text{spell} \times \text{potion} \ge \text{success}$$

**Output:**
An array where the $i$-th element is the count of successful potions for the $i$-th spell.

**Example:**

```python
Input: spells = [5, 1, 3], potions = [1, 2, 3, 4, 5], success = 7
Output: [4, 0, 3]
Explanation:
- Spell 5: Needs potion >= 1.4. Potions [2,3,4,5] work (4 pairs).
- Spell 1: Needs potion >= 7. No potions work (0 pairs).
- Spell 3: Needs potion >= 2.33. Potions [3,4,5] work (3 pairs).
```

-----

## Deep Dive: Binary Search & The `bisect` Module 📚

Before we solve the specific problem, we must understand the tools we are using.

### 1\. What is Binary Search? 🔍

Binary Search is an algorithm used to find a specific element or position in a **sorted** array. Unlike a linear scan that checks every element one by one ($O(N)$), Binary Search divides the search space in half at every step ($O(\log N)$).

**Analogy:** Imagine looking for a word in a physical dictionary. You don't read every page from the start. You open the book in the middle. If the word you want is alphabetically *after* the page you opened, you ignore the first half of the book and repeat the process with the second half.

### 2\. What is Python's `bisect` module?

Python provides a built-in module called `bisect` that implements optimized binary search algorithms. It assumes the list you are searching is **already sorted**.

### 3\. What is `bisect_left()`?

The function `bisect.bisect_left(a, x)` finds the **first insertion point** for element `x` in array `a` to maintain sorted order.

  * **Parameters:**
      * `a`: The sorted list.
      * `x`: The value we are looking for (or looking for the spot to insert).
  * **Return Value:** An integer index `i`.
      * All elements to the left of `i` (i.e., `a[:i]`) are **strictly less than** `x`.
      * All elements from `i` onwards (i.e., `a[i:]`) are **greater than or equal to** `x`.

**Example:**

```python
arr = [10, 20, 30, 40]
target = 25
index = bisect_left(arr, target)
# index is 2. (25 should go between 20 and 30).
# arr[2] is 30, which is >= 25.
```

-----

## Key Insights

### 1\. The Brute Force Bottleneck

A naive approach would be: "For every spell, loop through every potion."

  * If `spells` has length $N$ and `potions` has length $M$, this takes $O(N \times M)$.
  * With constraints up to $10^5$, $N \times M$ results in $10^{10}$ operations, which is far too slow (Time Limit Exceeded).

### 2\. Math Transformation

Instead of checking `spell * potion >= success`, we can rearrange the equation to find exactly what strength of potion we need:
$$\text{potion} \ge \frac{\text{success}}{\text{spell}}$$

### 3\. Optimizing with Sorting and Binary Search

If the `potions` array is **sorted**, we don't need to check every potion.

1.  We calculate the **minimum potion strength** required.
2.  We use **Binary Search** (`bisect_left`) to find the *first* potion in the sorted list that meets this requirement.
3.  Because the list is sorted, *every* potion after that index is also valid. We can calculate the count instantly using subtraction.

## Solution Approach

```python
import bisect
from typing import List

class Solution:
    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        
        # Step 1: Sort the potions.
        # This is crucial for Binary Search to work.
        # Time: O(M log M)
        potions.sort()
        
        m = len(potions)
        answer = []
        
        # Step 2: Iterate through each spell.
        # Time: O(N) loops
        for spell in spells:
            
            # Step 3: Calculate the minimum target potion strength.
            # We use floating point division.
            target = success / spell
            
            # Step 4: Find the index of the first valid potion.
            # bisect_left finds the first index where potion >= target.
            # Time: O(log M)
            index = bisect.bisect_left(potions, target)
            
            # Step 5: Calculate the count.
            # Since 'index' is the start of valid potions, and 'm' is the total length,
            # the number of valid potions is m - index.
            count = m - index
            answer.append(count)
            
        return answer
```

## Detailed Code Analysis

### Step 1: Sorting

```python
potions.sort()
```

  - We assume the spells come in random order, but to search efficiently, our search space (the potions) must be ordered.
  - `[1, 5, 2, 4, 3]` becomes `[1, 2, 3, 4, 5]`.

### Step 2: The Loop

```python
for spell in spells:
```

  - We process each spell one by one. Note that we do **not** sort `spells`, because the problem requires the output array to correspond to the original order of `spells`.

### Step 3: The Target Calculation

```python
target = success / spell
```

  - We derive the threshold.
  - Example: If `success = 7` and `spell = 5`:
      - `target = 7 / 5 = 1.4`.
      - We need a potion with strength $\ge 1.4$.

### Step 4: Binary Search (`bisect_left`)

```python
index = bisect.bisect_left(potions, target)
```

  - We search for `1.4` in `[1, 2, 3, 4, 5]`.
  - `bisect_left` sees that `1` is too small, but `2` is big enough.
  - It returns index **1** (the index of value `2`).
  - **Why `bisect_left` and not `bisect_right`?**
      - `bisect_right` would find the insertion point *after* any existing equal values.
      - If we needed $\ge 3$ and used `bisect_right` on `[1, 3, 5]`, it would return index 2 (after the 3). That would incorrectly exclude the 3.
      - `bisect_left` returns the index *before* the 3, correctly including it in the "valid" range to the right.

### Step 5: Calculation

```python
count = m - index
```

  - `m` (total length) is 5. `index` found is 1.
  - `count = 5 - 1 = 4`.
  - This means indices `1, 2, 3, 4` (values `2, 3, 4, 5`) are all valid.

## Step-by-Step Execution Trace

**Example:**
`spells = [5, 1, 3]`
`potions = [1, 2, 3, 4, 5]` (Sorted)
`success = 7`
`m = 5`

| Spell Value | Target (`7 / spell`) | Binary Search (`bisect_left`) on `[1, 2, 3, 4, 5]` | Index Found | Calculation (`m - index`) | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **5** | `1.4` | Find insertion for 1.4. `1` \< 1.4 \< `2`. | **1** (points to value 2) | `5 - 1 = 4` | `[4]` |
| **1** | `7.0` | Find insertion for 7.0. 7.0 \> `5` (all items). | **5** (points to end) | `5 - 5 = 0` | `[4, 0]` |
| **3** | `2.33` | Find insertion for 2.33. `2` \< 2.33 \< `3`. | **2** (points to value 3) | `5 - 2 = 3` | `[4, 0, 3]` |

**Final Output:** `[4, 0, 3]`

## Performance Analysis

### Time Complexity: O(M log M + N log M)

1.  **Sorting Potions:** `O(M log M)`.
2.  **Looping Spells:** `O(N)`.
3.  **Binary Search:** Inside the loop, we perform `bisect`, which takes `O(log M)`.
      - Total for loop: `O(N * log M)`.
4.  **Total:** `O(M log M + N log M)`.
      - Given $N, M \le 10^5$, this is extremely fast compared to the naive $O(N \cdot M)$.

### Space Complexity: O(1) or O(N)

  - **Auxiliary Space:** We use `O(1)` extra space for variables (ignoring the space for the output array `answer`).
  - **Sorting Space:** Python's Timsort uses `O(M)` space.
  - **Output Space:** `O(N)` to store the result.