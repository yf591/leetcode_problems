# 49\. Group Anagrams - Solution Explanation

## Problem Overview

You are given an array of strings `strs`. The task is to group all the strings that are **anagrams** of each other together.

**Anagram Definition:**
An anagram is a word or phrase formed by rearranging the letters of another, using all the original letters exactly once. The core idea is that both strings must have the **exact same characters with the exact same frequencies**.

**Examples:**

```python
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
# The groups are formed by words that can be rearranged into each other.

Input: strs = [""]
Output: [[""]]
```

## Key Insights

### Finding a Unique "Signature" for Anagrams

The main challenge is to identify which strings belong to the same anagram group. How can we tell that `"eat"`, `"tea"`, and `"ate"` are all related? We need to find a **canonical representation** or a unique "signature" that is the same for all of them.

The key insight is that if you **sort the characters** of an anagram, the result is always the same.

  - `sorted("eat")` -\> `['a', 'e', 't']` -\> `"aet"`
  - `sorted("tea")` -\> `['a', 'e', 't']` -\> `"aet"`
  - `sorted("ate")` -\> `['a', 'e', 't']` -\> `"aet"`

This sorted string `"aet"` can act as a unique key for this group of anagrams.

### Grouping with a Hash Map

Once we have a way to generate a unique key for each anagram group, we can use a **hash map** (a `dict` in Python) to group the words.

  - The **keys** of our map will be the sorted-character signatures (e.g., `"aet"`).
  - The **values** of our map will be lists of the original words that produce that signature (e.g., `["eat", "tea", "ate"]`).

## Solution Approach

This solution iterates through the input list of strings. For each string, it creates a sorted key. It then uses a `defaultdict` (a special kind of dictionary) to append the original string to a list associated with its key.

```python
import collections
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # A hash map to store the groups.
        anagram_map = collections.defaultdict(list)
        
        # Iterate through each word in the input list.
        for word in strs:
            # Create the canonical key by sorting the word's characters.
            sorted_key = "".join(sorted(word))
            
            # Append the original word to the list associated with its sorted key.
            anagram_map[sorted_key].append(word)
            
        # The values of the map are the lists of grouped anagrams.
        return list(anagram_map.values())
```

## Deep Dive: `collections.defaultdict(list)`

A `defaultdict` is a special type of dictionary provided by Python's `collections` module. It's a fantastic tool that simplifies the logic for grouping items.

**The Problem with a Regular `dict`:**
When you group items with a regular dictionary, you have to constantly check if a key already exists before you can append to its list. The code would look like this:

```python
# The long way with a regular dict
anagram_map = {}
for word in strs:
    sorted_key = "".join(sorted(word))
    if sorted_key not in anagram_map:
        # If the key is new, you must create an empty list first
        anagram_map[sorted_key] = []
    # Then you can append
    anagram_map[sorted_key].append(word)
```

**How `defaultdict` is Better:**
A `defaultdict` automates this process. When you create it with `collections.defaultdict(list)`, you are telling it:

> "If I ever try to access or modify a key that doesn't exist, don't raise an error. Instead, automatically create a new entry for me by calling the function I provided (`list()` in this case) and use its result as the default value."

Since `list()` creates an empty list `[]`, the first time we see a new key, `defaultdict` automatically creates an empty list for it. This allows us to simply `append` in one step.

```python
# The short, clean way with defaultdict
anagram_map = collections.defaultdict(list)
for word in strs:
    sorted_key = "".join(sorted(word))
    # No 'if' check needed! If the key is new, an empty list is created automatically.
    anagram_map[sorted_key].append(word)
```

## Detailed Code Analysis

### Step 1: Initialization

```python
anagram_map = collections.defaultdict(list)
```

  - We create our `defaultdict`. It will store our anagram groups.

### Step 2: The Loop

```python
for word in strs:
```

  - This loop iterates through every single `word` in the input list `strs`.

### Step 3: Key Generation

```python
sorted_key = "".join(sorted(word))
```

  - This is the most important line inside the loop. It creates the unique signature for each word.
  - **`sorted(word)`**: This function takes a string (e.g., `"tea"`) and returns a sorted **list** of its characters (e.g., `['a', 'e', 't']`).
  - **`"".join(...)`**: This method takes the list of characters and joins them back together into a **string**, with an empty string `""` as the separator. The result is our key (e.g., `"aet"`).

### Step 4: Appending to the Group

```python
anagram_map[sorted_key].append(word)
```

  - This line uses the `sorted_key` to access our map.
  - Because we are using a `defaultdict`, if `sorted_key` is new, an empty list is automatically created.
  - The original `word` is then appended to the list corresponding to its key.

### Step 5: Returning the Result

```python
return list(anagram_map.values())
```

  - After the loop, our `anagram_map` is fully populated.
  - `.values()` returns a collection of all the values (our lists of anagrams) from the map.
  - `list(...)` converts this collection into the final list-of-lists format required by the problem.

## Step-by-Step Execution Trace

Let's trace the algorithm with the example `strs = ["eat", "tea", "tan"]` with extreme detail.

| `word` | `sorted(word)` | `sorted_key` | `anagram_map` State (after append) |
| :--- | :--- | :--- | :--- |
| **Start** | - | - | `{}` (empty defaultdict) |
| **"eat"** | `['a', 'e', 't']`| `"aet"` | `{'aet': ['eat']}` |
| **"tea"** | `['a', 'e', 't']`| `"aet"` | `{'aet': ['eat', 'tea']}` |
| **"tan"** | `['a', 'n', 't']`| `"ant"` | `{'aet': ['eat', 'tea'], 'ant': ['tan']}` |

  - **Final Step**: The `for` loop finishes. The function returns `list(anagram_map.values())`, which is `[['eat', 'tea'], ['tan']]` (the order of the groups doesn't matter).

## Performance Analysis

### Time Complexity: O(N \* K log K)

  - Where `N` is the number of strings in the `strs` list, and `K` is the maximum length of a string in the list.
  - We loop through `N` strings. Inside the loop, the most expensive operation is sorting each string, which takes `O(K log K)` time.

### Space Complexity: O(N \* K)

  - In the worst case (if all strings are unique anagrams), the hash map will store all `N` strings. The total space required is proportional to the total number of characters in the input list.

## Key Learning Points

  - **Canonical Representation**: Many grouping problems can be solved by finding a "canonical" or "standard" representation for items that belong in the same group (like a sorted string for anagrams).
  - **Hash Maps for Grouping**: A hash map is the go-to data structure for grouping items based on a key.
  - **`collections.defaultdict`**: This is a powerful Python tool that simplifies the code for grouping by automatically handling the creation of new groups.