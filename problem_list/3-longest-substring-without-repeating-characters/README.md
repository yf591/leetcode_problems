# 3\. Longest Substring Without Repeating Characters - Solution Explanation

## Problem Overview

You are given a string `s`. The task is to find the length of the **longest substring** that does not contain any repeating characters.

**Key Definitions:**

  - **Substring**: A *contiguous* sequence of characters within a string. For `s = "pwwkew"`, `"wke"` is a substring, but `"pwke"` is a subsequence and not a valid answer.
  - **Without Repeating Characters**: All characters within the substring must be unique.

**Examples:**

```python
Input: s = "abcabcbb"
Output: 3
Explanation: The longest substring without repeating characters is "abc", with a length of 3.

Input: s = "bbbbb"
Output: 1
Explanation: The longest substring is "b", with a length of 1.

Input: s = "pwwkew"
Output: 3
Explanation: The longest substring is "wke", with a length of 3.
```

## Key Insights

### The Sliding Window Technique

A brute-force approach, where you check every possible substring for uniqueness, would be very slow (`O(n³)` or `O(n²)`). The key insight for an efficient `O(n)` solution is the **sliding window** technique.

We can think of a "window" that slides across the string. This window represents the current substring we are examining.

1.  **Expand**: We expand the window by moving its `right` boundary to the right.
2.  **Maintain Validity**: A window is "valid" as long as it contains no duplicate characters.
3.  **Shrink**: If expanding the window makes it invalid (because we added a character that was already inside), we must shrink the window from the `left` until it becomes valid again.

To do this efficiently, we need a way to instantly check if a character is already in our window. A **hash set** is the perfect data structure for this.

## Solution Approach

This solution implements the variable-size sliding window pattern. It uses a `set` to store the characters within the current window. A `right` pointer expands the window, and a `left` pointer shrinks it when necessary.

```python
from typing import List

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # A set to store the unique characters in the current window.
        char_set = set()
        # The left pointer of our sliding window.
        left = 0
        # The variable to store the maximum length found so far.
        max_length = 0
        
        # The 'right' pointer iterates through the string, expanding the window.
        for right in range(len(s)):
            # If the new character is a duplicate, shrink the window from the left
            # until the duplicate is removed.
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            
            # Add the new character to our window's set.
            char_set.add(s[right])
            
            # The current window is now valid. Update the maximum length.
            current_length = right - left + 1
            max_length = max(max_length, current_length)
            
        return max_length
```

## Detailed Code Analysis

### Step 1: Initialization

```python
char_set = set()
left = 0
max_length = 0
```

  - `char_set`: An empty set that will store the unique characters of our current valid substring (the "window").
  - `left`: A pointer representing the left boundary of our window. It starts at index 0.
  - `max_length`: Our final answer. We initialize it to 0.

### Step 2: The Expansion Loop

```python
for right in range(len(s)):
```

  - This `for` loop drives the algorithm. The `right` pointer iterates from the beginning to the end of the string. In each iteration, `s[right]` is the new character we are trying to add to our window.

### Step 3: The Shrinking Loop (Maintaining a Valid Window)

```python
while s[right] in char_set:
    char_set.remove(s[left])
    left += 1
```

  - This is the most critical part of the logic.
  - **`while s[right] in char_set:`**: Before adding the new character `s[right]`, we check if it's already in our `char_set`. If it is, we have a duplicate, and our window is invalid.
  - **`char_set.remove(s[left])`**: To fix the window, we must remove the character at the far left of our window.
  - **`left += 1`**: We then shrink the window by moving our `left` pointer one step to the right.
  - This `while` loop continues until the original duplicate of `s[right]` has been removed from the window, making it valid again.

### Step 4: Expanding and Updating

```python
char_set.add(s[right])
max_length = max(max_length, right - left + 1)
```

  - **`char_set.add(s[right])`**: Now that the window is guaranteed to be valid, we add the new character from the `right` pointer into our set.
  - **`max_length = max(...)`**: The length of the current valid window is `right - left + 1`. We compare this to the `max_length` we've seen so far and keep the larger value.

## Deep Dive: Python's `set()`

  * **What is a Set?** 🗃️
    A `set` is a data structure, like a list, but it only stores **unique** items. The items inside are also **unordered**. Think of it as a bag of marbles where you can't have two marbles of the exact same color.

    ```python
    my_list = [1, 2, 2, 3]
    my_set = set(my_list) # my_set is now {1, 2, 3}
    ```

  * **Why is it so useful here?**
    The most important feature of a set is its **speed**. Checking for an item's existence (`item in my_set`), adding an item (`my_set.add(item)`), and removing an item (`my_set.remove(item)`) are all extremely fast operations, taking **O(1)** (constant) time on average. This makes it the perfect tool for our sliding window, where we need to constantly check for duplicates and update the window's contents.

## Deep Dive: `.add()` (for Sets) vs. `.append()` (for Lists)

This is a common point of confusion. The method you use depends on the data structure.

  * **`.append()` is for Lists**: A list is an ordered sequence. `.append()` **always** adds an item to the very **end** of the list. It can contain duplicates.

    ```python
    my_list = ['a', 'b']
    my_list.append('b') # my_list is now ['a', 'b', 'b']
    ```

  * **`.add()` is for Sets**: A set is an unordered collection of unique items. `.add()` adds an item to the set. If the item is **already present**, the set **does not change**.

    ```python
    my_set = {'a', 'b'}
    my_set.add('b') # my_set is still {'a', 'b'}
    ```

For this problem, since we need to track a collection of *unique* characters, a `set` with its `.add()` and `.remove()` methods is the correct choice.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `s = "pwwkew"` with extreme detail.

| `right` | `s[right]` | `char_set` (start) | `while` loop runs? | `char_set` & `left` (after `while`) | Action & `max_length` (after update) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Start**| - | `{}` | - | `{}`, `left=0` | **0** |
| **0** | 'p' | `{}` | `'p' in {}` -\> No | `{}`, `left=0`| `add('p')`. `max(0, 0-0+1=1)` -\> **1** |
| **1** | 'w' | `{'p'}` | `'w' in {'p'}` -\> No | `{'p'}`, `left=0`| `add('w')`. `max(1, 1-0+1=2)` -\> **2** |
| **2** | 'w' | `{'p','w'}` | `'w' in {'p','w'}` -\> **Yes** | 1. `remove('p')`, `left=1`. `set={'w'}`<br>2. `remove('w')`, `left=2`. `set={}`| `add('w')`. `max(2, 2-2+1=1)` -\> **2** |
| **3** | 'k' | `{'w'}` | `'k' in {'w'}` -\> No | `{'w'}`, `left=2`| `add('k')`. `max(2, 3-2+1=2)` -\> **2** |
| **4** | 'e' | `{'w','k'}` | `'e' in {'w','k'}` -\> No | `{'w','k'}`, `left=2`| `add('e')`. `max(2, 4-2+1=3)` -\> **3** |
| **5** | 'w' | `{'w','k','e'}`| `'w' in {'w','k','e'}` -\> **Yes** | `remove('w')`, `left=3`. `set={'k','e'}`| `add('w')`. `max(3, 5-3+1=3)` -\> **3** |

  - The main loop finishes.
  - The function returns the final `max_length`, which is **3**.

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the length of the string `s`. This is an `O(n)` solution because, in the worst case, each character will be visited at most twice: once by the `right` pointer and once by the `left` pointer.

### Space Complexity: O(k)

  - Where `k` is the number of unique characters in the character set (e.g., 26 for lowercase English letters). The space is determined by the maximum size of the `char_set`. In the worst case, the set could hold `k` unique characters.