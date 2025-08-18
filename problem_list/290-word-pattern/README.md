# 290\. Word Pattern - Solution Explanation

## Problem Overview

Given a `pattern` string of letters and a string `s` of words, determine if `s` follows the `pattern`.

**"Follows" Definition**
This means there is a perfect one-to-one mapping (**bijection**) between the letters in `pattern` and the words in `s`.

1.  Every letter in `pattern` must map to the exact same word every time it appears.
2.  No two different letters in `pattern` can map to the same word.

**Examples**

  - `pattern = "abba"`, `s = "dog cat cat dog"` -\> **True**. The mapping is `a` -\> `"dog"`, `b` -\> `"cat"`. This is a consistent one-to-one mapping.
  - `pattern = "abba"`, `s = "dog cat cat fish"` -\> **False**. The second `'a'` in the pattern should map to `"dog"`, but it corresponds to `"fish"`. The forward mapping is inconsistent.
  - `pattern = "aaaa"`, `s = "dog cat cat dog"` -\> **False**. The letter `'a'` tries to map to both `"dog"` and `"cat"`.

## Key Insights

### Isomorphic Relationship

This problem is fundamentally the same as "Isomorphic Strings," but instead of mapping characters to characters, we are mapping **characters to words**. The core logic of verifying a consistent, two-way, one-to-one mapping remains the same.

### Input Preparation

The `pattern` is already a sequence of characters, but the string `s` is a sentence. Before we can compare them, we must convert `s` into a sequence of words. The `s.split(' ')` method is the perfect tool for this.

## Solution Approach

This solution first prepares the input by splitting the sentence into words. Then, it iterates through the pattern and the words in parallel, using two hash maps to ensure the one-to-one mapping is valid in both directions.

```python
class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split(' ')

        if len(pattern) != len(words):
            return False

        map_pattern_to_word = {}
        map_word_to_pattern = {}

        for char, word in zip(pattern, words):
            # Forward check: char has been seen, but maps to a different word
            if char in map_pattern_to_word:
                if map_pattern_to_word[char] != word:
                    return False
            # Backward check: char is new, but its target word is already taken
            elif word in map_word_to_pattern:
                return False
            # This is a new, valid mapping
            else:
                map_pattern_to_word[char] = word
                map_word_to_pattern[word] = char

        return True
```

**Strategy**

1.  **Split `s`**: Convert the input string `s` into a list of `words`.
2.  **Check Lengths**: Compare the length of the `pattern` and the `words` list. If they are not equal, a match is impossible.
3.  **Initialize Maps**: Create two maps to track the mapping from pattern-to-word and word-to-pattern.
4.  **Iterate & Verify**: Loop through the `(char, word)` pairs. For each pair, check for conflicts using the two maps. If a conflict is found, return `False`.
5.  **Record Mapping**: If no conflicts exist, record the new mapping in both directions.
6.  **Success**: If the loop completes, the pattern is valid; return `True`.

## Detailed Code Analysis

### Step 1: Input Preparation & Length Check

```python
words = s.split(' ')
if len(pattern) != len(words):
    return False
```

  - This is a crucial first step. We convert the sentence `s` into a list of words.
  - The length check is an important and efficient way to fail early if a match is structurally impossible.

### Step 2: Map Initialization and Iteration

```python
map_pattern_to_word = {}
map_word_to_pattern = {}
for char, word in zip(pattern, words):
    # ...
```

  - We initialize two dictionaries to track the mapping in both directions.
  - `zip()` allows us to conveniently iterate over the character from the `pattern` and the `word` from the `words` list at the same index simultaneously.

### Step 3: The `if/elif/else` Logic

This block is the heart of the validation. It checks for the two ways a mapping can be invalid.

```python
# Forward check
if char in map_pattern_to_word:
    if map_pattern_to_word[char] != word:
        return False
```

  - This checks if we've seen this `char` before. If we have, it *must* map to the same `word` it did previously. If not, the pattern is broken.

<!-- end list -->

```python
# Backward check
elif word in map_word_to_pattern:
    return False
```

  - This `elif` block only runs if the `char` is new. It checks if the `word` it's trying to map to has *already been taken* by a different character. If so, it violates the one-to-one rule.

<!-- end list -->

```python
# New, valid mapping
else:
    map_pattern_to_word[char] = word
    map_word_to_pattern[word] = char
```

  - If both checks pass, we have a new, valid pair. We record the mapping in both dictionaries for future checks.

## Step-by-Step Execution Trace

### Example: `pattern = "abba"`, `s = "dog cat cat fish"`

1.  `words` becomes `['dog', 'cat', 'cat', 'fish']`. Lengths match (4).
2.  Maps are empty.

| `(char, word)` | Condition Check | `map_pattern_to_word` | `map_word_to_pattern` | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Start** | | `{}` | `{}` | |
| **('a', 'dog')** | `else` block | `{'a': 'dog'}` | `{'dog': 'a'}` | New mapping |
| **('b', 'cat')** | `else` block | `{'a':'dog', 'b':'cat'}` | `{'dog':'a', 'cat':'b'}` | New mapping |
| **('b', 'cat')** | `if` block: `map['b'] == 'cat'`. OK. | (no change) | (no change) | No action |
| **('a', 'fish')** | `if` block: `map['a']` is `'dog'`, which `!=` `'fish'`. Conflict\! | (no change) | (no change) | **Return `False`** |

## Performance Analysis

### Time Complexity: O(N + M)

  - Where `N` is the length of `pattern` and `M` is the length of `s`.
  - `s.split()` takes O(M) time. The `zip` loop runs `N` times.

### Space Complexity: O(W + C)

  - Where `W` is the number of unique words and `C` is the number of unique characters. This is the space required for the dictionaries and the `words` list.

## Key Learning Points

  - Recognizing that this is an isomorphism problem, similar to mapping characters to characters.
  - The importance of pre-processing input (`s.split()`) before applying the core algorithm.
  - The necessity of a two-way check (using two maps or a map and a set) to enforce a true one-to-one mapping.

## Common Pitfalls Avoided

  - Forgetting to split `s` into words and trying to map characters to characters.
  - Only checking the forward mapping (`pattern` -\> `s`), which fails on inputs like `pattern = "ab", s = "dog dog"`.
  - Forgetting to check if the lengths of the pattern and the word list are equal.