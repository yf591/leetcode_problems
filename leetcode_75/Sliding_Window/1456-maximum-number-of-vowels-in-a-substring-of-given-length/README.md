# 1456\. Maximum Number of Vowels in a Substring of Given Length - Solution Explanation

## Problem Overview

You are given a string `s` and an integer `k`. The task is to find the **maximum number of vowels** contained in any **contiguous substring** of `s` that has a length of exactly `k`.

**Key Definitions:**

  - **Vowels**: The letters 'a', 'e', 'i', 'o', 'u'.
  - **Substring**: A continuous sequence of characters within a string.
  - **Substring of length k**: A "slice" of the string that is `k` characters long.

**Examples:**

```python
Input: s = "abciiidef", k = 3
Output: 3
Explanation: The substring "iii" contains 3 vowels, which is the maximum possible.

Input: s = "leetcode", k = 3
Output: 2
Explanation: Substrings like "lee", "eet", and "ode" contain 2 vowels. No substring of length 3 has more than 2 vowels.
```

## Key Insights

### The Inefficient Brute-Force Approach

A naive way to solve this would be to check every single possible substring of length `k`. You would start at index 0, count the vowels in `s[0:k]`, then move to index 1, count the vowels in `s[1:k+1]`, and so on. This involves a lot of redundant work, as you would be re-counting the same characters in the overlapping parts of the substrings. This approach would be too slow, with a time complexity of roughly `O(n * k)`.

### The "Sliding Window" Technique

The key to a highly efficient `O(n)` solution is the **sliding window** technique. Instead of creating and re-scanning new substrings, we can maintain a single "window" of size `k` and slide it across the string one character at a time.

The crucial insight is that when we slide the window, we don't need to recount all `k` characters. The change in the vowel count is determined by only two characters:

1.  The **new character** that just entered the window on the right.
2.  The **old character** that just left the window on the left.

By only considering these two characters at each step, we can update our vowel count in constant `O(1)` time.

## Solution Approach

This solution implements the sliding window technique. It first calculates the vowel count for the initial window. Then, it iterates through the rest of the string, sliding the window one position at a time and efficiently updating the vowel count, while keeping track of the maximum count seen.

```python
from typing import List

class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowels = {'a', 'e', 'i', 'o', 'u'}
        
        # --- Step 1: Initialize the window ---
        # Calculate the vowel count for the first window of size 'k'.
        current_vowel_count = 0
        for i in range(k):
            if s[i] in vowels:
                current_vowel_count += 1
        
        # The max count so far is the count from this first window.
        max_vowel_count = current_vowel_count
        
        # --- Step 2: Slide the window across the rest of the string ---
        for i in range(k, len(s)):
            # Step 2a: Account for the new character entering the window.
            if s[i] in vowels:
                current_vowel_count += 1
            
            # Step 2b: Account for the old character leaving the window.
            char_leaving = s[i - k]
            if char_leaving in vowels:
                current_vowel_count -= 1
            
            # Step 2c: Update the overall maximum.
            max_vowel_count = max(max_vowel_count, current_vowel_count)
            
        return max_vowel_count
```

## Detailed Code Analysis

### Step 1: Initialization

```python
vowels = {'a', 'e', 'i', 'o', 'u'}
current_vowel_count = 0
for i in range(k):
    if s[i] in vowels:
        current_vowel_count += 1
max_vowel_count = current_vowel_count
```

  - **`vowels = {'a', 'e', 'i', 'o', 'u'}`**: We define the vowels in a `set`. A set provides extremely fast O(1) average time complexity for checking if a character is present (`char in vowels`), which is much faster than checking against a list.
  - **`for i in range(k): ...`**: This loop calculates the vowel count for the very first window (`s[0]` to `s[k-1]`). This is our starting point.
  - **`max_vowel_count = current_vowel_count`**: We initialize our overall maximum to the count from this first window.

### Step 2: The Sliding Loop

```python
for i in range(k, len(s)):
```

  - This loop handles the "sliding" motion.
  - It starts at index `k`, because `s[k]` is the first character to enter our window after the initial setup. The loop continues until `i` has processed the last character of the string.

### Step 3: The `O(1)` Window Update

This is the core of the sliding window algorithm.

```python
# Add the effect of the new character entering from the right
if s[i] in vowels:
    current_vowel_count += 1

# Subtract the effect of the old character leaving from the left
char_leaving = s[i - k]
if char_leaving in vowels:
    current_vowel_count -= 1
```

  - `s[i]` is the new character. If it's a vowel, we increment our `current_vowel_count`.
  - `s[i - k]` is the character that is now outside the window on the left. If it was a vowel, we must decrement our `current_vowel_count`.

### Step 4: Tracking the Maximum

```python
max_vowel_count = max(max_vowel_count, current_vowel_count)
```

  - After each slide and update, the `current_vowel_count` holds the vowel count for the current window. We compare it with our overall `max_vowel_count` and update the max if the current window is better.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `s = "abciiidef"` and `k = 3` with extreme detail.

1.  **Initialization**:

      * `vowels = {'a', 'e', 'i', 'o', 'u'}`
      * The first window is `s[0:3]`, which is `"abc"`.
      * The initialization loop runs:
          * `s[0]` ('a') is a vowel. `current_vowel_count` becomes 1.
          * `s[1]` ('b') is not.
          * `s[2]` ('c') is not.
      * `current_vowel_count` is **1**.
      * `max_vowel_count` is set to **1**.
      * The main sliding loop will run for `i` from `3` to `8`.

2.  **The Sliding Loop**:

| `i` | Current Window | `s[i]` (Entering) | `s[i-k]` (Leaving) | `current_vowel_count` (before) | Update Action | `current_vowel_count` (after) | `max_vowel_count` |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Start** | `"abc"` | - | - | 1 | - | 1 | **1** |
| **3** | `"bci"` | 'i' (vowel) | 'a' (vowel) | 1 | `+1` then `-1` | 1 | `max(1, 1) = 1` |
| **4** | `"cii"` | 'i' (vowel) | 'b' (not vowel)| 1 | `+1` | 2 | `max(1, 2) = 2` |
| **5** | `"iii"` | 'i' (vowel) | 'c' (not vowel)| 2 | `+1` | 3 | `max(2, 3) = 3` |
| **6** | `"iid"` | 'd' (not vowel)| 'i' (vowel) | 3 | `-1` | 2 | `max(3, 2) = 3` |
| **7** | `"ide"` | 'e' (vowel) | 'i' (vowel) | 2 | `+1` then `-1` | 2 | `max(3, 2) = 3` |
| **8** | `"def"` | 'f' (not vowel)| 'i' (vowel) | 2 | `-1` | 1 | `max(3, 1) = 3` |

3.  **Final Step**:
      * The loop finishes.
      * The function returns the final `max_vowel_count`, which is **3**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the length of the string `s`.
  - We have an initial loop that runs `k` times and a main loop that runs `n - k` times.
  - The total time complexity is `O(k + (n - k))`, which simplifies to `O(n)`. We make a single pass over the array.

### Space Complexity: O(1)

  - The space used for the `vowels` set is constant (it only ever holds 5 characters).
  - We only use a few variables to store our state (`current_vowel_count`, `max_vowel_count`, `i`). The space required is constant and does not grow with the size of the input string.