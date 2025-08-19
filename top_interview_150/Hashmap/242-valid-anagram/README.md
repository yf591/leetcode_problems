# 242\. Valid Anagram - Solution Explanation

## Problem Overview

Given two strings, `s` and `t`, determine if `t` is an anagram of `s`.

**Anagram Definition:**
An anagram is a word or phrase formed by rearranging the letters of another, using all the original letters exactly once. The core idea is that both strings must have the **exact same characters with the exact same frequencies**.

**Examples**

```python
Input: s = "anagram", t = "nagaram"
Output: true
# Both strings have: three 'a's, one 'n', one 'g', one 'r', and one 'm'.

Input: s = "rat", t = "car"
Output: false
# The character counts do not match.
```

## Key Insights

### Character Frequency is Everything

The order of characters does not matter in an anagram, but their counts are critical. This means the problem isn't about string comparison in the usual sense, but about comparing the "inventory" of characters in each string.

### Hash Maps for Counting

The best data structure for tracking the frequency of items is a **hash map** (in Python, this is a `dict`). We can create a frequency map for each string and then simply compare the maps. If the maps are identical, the strings are anagrams. Python's `collections.Counter` is a specialized hash map designed for exactly this purpose.

## Solution Approach

This solution uses `collections.Counter` to efficiently create a frequency map for each string and then compares the two maps.

```python
import collections
from typing import List

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Step 1: Check if lengths are equal. If not, they can't be anagrams.
        if len(s) != len(t):
            return False
        
        # Step 2: Create a frequency map for each string.
        s_counts = collections.Counter(s)
        t_counts = collections.Counter(t)
        
        # Step 3: Compare the frequency maps.
        return s_counts == t_counts
```

**Strategy**

1.  **Early Exit**: Perform a quick length check. If the strings have different lengths, they can't possibly be anagrams. This is a simple and important optimization.
2.  **Count Frequencies**: Use `collections.Counter` to create a hash map for `s` and another for `t`. Each map will store the characters as keys and their frequencies as values.
3.  **Compare Maps**: The equality operator (`==`) for `Counter` objects checks if they have the exact same keys with the exact same counts. This single comparison tells us if the strings are anagrams.

## Detailed Code Analysis

### Step 1: Length Check

```python
if len(s) != len(t):
    return False
```

  - This is the first and fastest check. Anagrams must be made of the same letters, so they must have the same length.

### Step 2: Frequency Mapping

```python
s_counts = collections.Counter(s)
t_counts = collections.Counter(t)
```

  - `collections.Counter(s)` iterates through the string `s` and returns a `Counter` object (which works like a dictionary) that holds the frequency of each character.
  - For `s = "anagram"`, `s_counts` becomes `Counter({'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1})`.

### Step 3: Comparison

```python
return s_counts == t_counts
```

  - This is a powerful feature of the `Counter` class. It directly compares the two frequency maps. The expression is `True` only if both maps contain the exact same items with the exact same counts, which is the definition of an anagram.

## Deep Dive: `collections.Counter`

  * **What is `collections`?**
    It's a built-in Python module that provides specialized, high-performance container datatypes. Think of them as powerful alternatives to the standard `dict`, `list`, `set`, and `tuple`.

  * **What is `Counter`?** 🧮
    A `Counter` is a special kind of dictionary that's optimized for counting things.

      * **Creation**: You can create it easily from any sequence (like a string or a list)
        ```python
        # Creates Counter({'a': 3, 'b': 2, 'c': 1})
        c = collections.Counter("aabbbac")
        ```
      * **Missing Keys**: Unlike a regular dictionary, if you try to access a key that doesn't exist, it doesn't raise an error; it just returns `0`. This is very convenient.
      * **Equality**: As seen in the solution, you can directly compare two `Counter` objects with `==`.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the length of the strings. Creating each `Counter` requires iterating through the string once. The final comparison also takes, on average, time proportional to the number of unique characters.

### Space Complexity: O(1)

  - The space required for the `Counter` depends on the number of unique characters. Since the problem states the strings consist of lowercase English letters, there are at most 26 unique characters. Therefore, the space is constant.

## Alternative Approaches Comparison

### Approach 1: Hash Map / Counter (Our Solution)

  - ✅ **Time: O(n)**, **Space: O(1)** (for a fixed alphabet).
  - ✅ The most efficient and idiomatic Python solution.

### Approach 2: Sorting

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        return sorted(s) == sorted(t)
```

  - ✅ Very concise and easy to read.
  - ❌ Less performant. The time complexity is dominated by the sorting algorithm, which is **O(n log n)**.

## Key Learning Points

  - The definition of an anagram is fundamentally about character frequency.
  - Hash maps (`dict` and especially `collections.Counter`) are the ideal data structure for frequency counting problems.
  - Leveraging built-in, specialized data structures often leads to cleaner and more efficient code.