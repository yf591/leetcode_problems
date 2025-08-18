# 205\. Isomorphic Strings - Solution Explanation

## Problem Overview

Given two strings, `s` and `t`, determine if they are isomorphic.

**Isomorphic Definition**
Two strings are isomorphic if a one-to-one mapping can be established between their characters to transform `s` into `t`. This means

1.  Every occurrence of a character in `s` must be replaced with the *same* character in `t`.
2.  No two different characters in `s` can be mapped to the *same* character in `t`.
3.  A character can map to itself.

**Examples**

  - `s = "egg", t = "add"` -\> **True** (`e` -\> `a`, `g` -\> `d`).
  - `s = "foo", t = "bar"` -\> **False** (`o` tries to map to `a` and `r`).
  - `s = "ab", t = "aa"` -\> **False** (`a` and `b` both try to map to `a`).

## Key Insights

### Two-Way One-to-One Mapping

The core of this problem is to verify a consistent **one-to-one mapping**. A simple mapping from `s` to `t` is not enough. For example, in `s = "ab", t = "aa"`, the forward mapping seems fine at first (`a`-\>`a`), but then `b` also tries to map to `a`, which is not allowed.

This means we must enforce the mapping in **both directions**

1.  From `s` to `t`: `s_char` must always map to the same `t_char`.
2.  From `t` to `s`: `t_char` must only ever be mapped to by the same `s_char`.

**Hash maps** (dictionaries in Python) are the perfect data structure for tracking these character mappings.

## Solution Approach

This solution iterates through both strings in parallel, using two hash maps to check for mapping consistency in both directions.

```python
class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        # Map characters from s to t and from t to s
        map_s_to_t = {}
        map_t_to_s = {}

        for char_s, char_t in zip(s, t):
            # Check for mapping conflicts
            if ((char_s in map_s_to_t and map_s_to_t[char_s] != char_t) or
                (char_t in map_t_to_s and map_t_to_s[char_t] != char_s)):
                return False
            
            # If no conflict, establish the new mapping
            map_s_to_t[char_s] = char_t
            map_t_to_s[char_t] = char_s
            
        return True
```

**Strategy**

1.  **Initialize Maps**: Create two maps, `map_s_to_t` and `map_t_to_s`.
2.  **Parallel Iteration**: Use `zip` to loop through pairs of characters from `s` and `t`.
3.  **Check for Conflicts**: For each pair, check if either of the two isomorphism rules is violated using the maps. If so, return `False` immediately.
4.  **Record Mapping**: If no conflicts exist, record the new valid mapping in both maps.
5.  **Success**: If the loop completes without finding conflicts, the strings are isomorphic; return `True`.

## Detailed Code Analysis

### Step 1: Initialization

```python
map_s_to_t = {}
map_t_to_s = {}
```

  - `map_s_to_t` will store the forward mapping (`s` characters to `t` characters).
  - `map_t_to_s` will store the backward mapping (`t` characters to `s` characters).

### Step 2: Parallel Iteration

```python
for char_s, char_t in zip(s, t):
```

  - `zip(s, t)` is a Pythonic way to create an iterator that yields pairs of characters, `(s[0], t[0])`, `(s[1], t[1])`, etc.

### Step 3: Conflict Detection

```python
if ((char_s in map_s_to_t and map_s_to_t[char_s] != char_t) or
    (char_t in map_t_to_s and map_t_to_s[char_t] != char_s)):
    return False
```

This is the core logic, combined into a single `if` statement for conciseness. Let's break it down:

  - **`char_s in map_s_to_t and map_s_to_t[char_s] != char_t`**: This checks for a **forward conflict**. It asks: "Have we seen `char_s` before, and if so, did it map to something different than the current `char_t`?" (e.g., `foo` -\> `bar`, where `o` first maps to `a`, then tries to map to `r`).
  - **`char_t in map_t_to_s and map_t_to_s[char_t] != char_s`**: This checks for a **backward conflict**. It asks: "Have we seen `char_t` before, and if so, was it mapped from a different `char_s`?" (e.g., `ab` -\> `aa`, where `a` is first mapped from `a`, then `a` tries to be mapped from `b`). Note: The `!= char_s` part is redundant because if `char_s` was not in `map_s_to_t`, it must be a different character.

### Step 4: Recording the Mapping

```python
map_s_to_t[char_s] = char_t
map_t_to_s[char_t] = char_s
```

  - If no conflicts are found, we record the valid mapping in both directions.

## Step-by-Step Execution Trace

### Example: `s = "badc"`, `t = "baba"` (Should be False)

| `(char_s, char_t)` | Condition Check | `map_s_to_t` | `map_t_to_s` | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Start** | | `{}` | `{}` | |
| **('b', 'b')** | No conflicts | `{'b': 'b'}` | `{'b': 'b'}` | Record mapping |
| **('a', 'a')** | No conflicts | `{'b': 'b', 'a': 'a'}` | `{'b': 'b', 'a': 'a'}` | Record mapping |
| **('d', 'b')** | Backward conflict\! `char_s` ('d') is new, but `char_t` ('b') is already in `map_t_to_s`. | ... | ... | **Return `False`** |

## Performance Analysis

### Time Complexity: O(n)

  - Where `n` is the length of the strings. We iterate through the strings exactly once. Dictionary lookups and insertions are O(1) on average.

### Space Complexity: O(k)

  - Where `k` is the number of unique characters. In the worst case, the space used by the hashmaps is proportional to the size of the character set (e.g., 26 for lowercase English letters, up to 128 for ASCII).

## Why Two Maps Matter

The two maps are essential to enforce the **bijective (one-to-one)** nature of the mapping.

  - `map_s_to_t` ensures that the mapping is a valid **function** (every input `s` has only one output `t`).
  - `map_t_to_s` ensures that the mapping is **injective** (no two inputs `s` map to the same output `t`).

Together, they guarantee a true isomorphic relationship.

## Key Learning Points

  - Using hash maps to track character mappings is a powerful technique.
  - Problems involving "consistent mapping" often require checking the mapping in both directions.
  - The `zip()` function provides a clean way to iterate over multiple sequences in parallel.

## Real-World Applications

  - **Cryptography**: Simple substitution ciphers rely on an isomorphic mapping between the alphabet and the cipher alphabet.
  - **Data Obfuscation**: Replacing sensitive data (like names or IDs) with consistently generated fake data while preserving relationships.
  - **Pattern Matching**: Verifying if two different data streams follow the same underlying pattern or structure.