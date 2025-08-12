# 383. Ransom Note - Solution Explanation

## Problem Overview

Given two strings `ransomNote` and `magazine`, determine if `ransomNote` can be constructed using letters from `magazine`.  
**Each letter in magazine can only be used once.**

**Examples:**
- `ransomNote = "a"`, `magazine = "b"` → `false`
- `ransomNote = "aa"`, `magazine = "ab"` → `false`
- `ransomNote = "aa"`, `magazine = "aab"` → `true`

**Constraints:**
- 1 ≤ ransomNote.length, magazine.length ≤ 10⁵
- Both strings consist of lowercase English letters

## Understanding the Problem

### What We're Looking For
We need to check if every character in `ransomNote` can be "taken" from `magazine`, **using each magazine letter at most once**.

### Key Insight: Inventory Management
Treat `magazine` as an inventory of letters.  
For each letter needed in `ransomNote`, check if it is available in the inventory.  
If yes, use it (decrement the count). If not, return `false`.

## Algorithm: Frequency Counter (Hash Map)

The most efficient solution uses a **frequency counter** (hash map) to track available letters in `magazine`.

**Core Strategy:**
1. Count the frequency of each letter in `magazine`
2. For each letter in `ransomNote`, check if it exists in the inventory
3. If available, use one (decrement count)
4. If not available, return `false`
5. If all letters are available, return `true`

## Step-by-Step Algorithm Breakdown

### Step 1: Build Inventory with Counter
```python
from collections import Counter
magazine_counts = Counter(magazine)
```
**Purpose**: Store `{letter: count}` for all magazine letters  
**Example**: `"aab"` → `{'a': 2, 'b': 1}`

### Step 2: Iterate Through ransomNote
```python
for char in ransomNote:
```
**Logic**: For each letter needed, check inventory

### Step 3: Check and Use Inventory
```python
if magazine_counts[char] > 0:
    magazine_counts[char] -= 1
else:
    return False
```
**Check**: Is the letter available?  
**Use**: Decrement count if available  
**Fail**: Return `False` if not enough letters

### Step 4: Return True if All Letters Used Successfully
```python
return True
```
**Success**: All letters found in inventory

## Detailed Example Walkthrough

**Input:** `ransomNote = "aa"`, `magazine = "aab"`

### Initial State
```
ransomNote: "aa"
magazine: "aab"
magazine_counts: {'a': 2, 'b': 1}
```

### Iteration 1: char = 'a'
```
magazine_counts['a'] = 2 > 0 → use one
magazine_counts['a'] -= 1 → now 1
```

### Iteration 2: char = 'a'
```
magazine_counts['a'] = 1 > 0 → use one
magazine_counts['a'] -= 1 → now 0
```

### All letters used successfully → return True

## More Examples

**Input:** `ransomNote = "aa"`, `magazine = "ab"`
```
magazine_counts: {'a': 1, 'b': 1}
First 'a': available, use one → now 0
Second 'a': not available (count is 0) → return False
```

**Input:** `ransomNote = "a"`, `magazine = "b"`
```
magazine_counts: {'b': 1}
'a' not available → return False
```

## Edge Case: Extra Letters in Magazine

**Input:** `ransomNote = "abc"`, `magazine = "aabbccdd"`
```
magazine_counts: {'a': 2, 'b': 2, 'c': 2, 'd': 2}
Each letter needed is available → return True
```

## Alternative Approaches Comparison

### Approach 1: Brute Force (Inefficient)
```python
def canConstruct(ransomNote, magazine):
    for char in ransomNote:
        if char in magazine:
            magazine = magazine.replace(char, '', 1)
        else:
            return False
    return True
```
- ❌ **Time: O(m * n)** (slow for large inputs)
- ❌ **Space: O(n)** (creates new strings repeatedly)
- ✅ **Simple but not scalable**

### Approach 2: Counter Subtraction (Pythonic)
```python
from collections import Counter
def canConstruct(ransomNote, magazine):
    return not (Counter(ransomNote) - Counter(magazine))
```
- ✅ **Time: O(m + n)**
- ✅ **Space: O(1) extra (if using built-in Counter)**
- ✅ **Very concise**
- ❌ **Less explicit for beginners**

## Current Solution Advantages

### Approach 3: Frequency Counter (Our Solution)
```python
from collections import Counter
def canConstruct(ransomNote, magazine):
    magazine_counts = Counter(magazine)
    for char in ransomNote:
        if magazine_counts[char] > 0:
            magazine_counts[char] -= 1
        else:
            return False
    return True
```
- ✅ **Time: O(m + n)** (m = ransomNote length, n = magazine length)
- ✅ **Space: O(1) extra (alphabet size is fixed)**
- ✅ **Easy to understand and debug**
- ✅ **Efficient for large inputs**

## Time & Space Complexity Analysis

- **Time Complexity**: **O(m + n)**
  - Build Counter: O(n)
  - Iterate ransomNote: O(m)
- **Space Complexity**: **O(1)** (since only lowercase letters, max 26 keys)

## Hash Map Deep Dive

### Why Counter Works Here
- **Fast Lookup**: O(1) for each letter
- **Inventory Management**: Tracks available letters and usage
- **Handles Duplicates**: Correctly manages multiple occurrences

### Counter Operations
```python
magazine_counts = Counter(magazine)  # Build inventory
magazine_counts[char]                # Check availability
magazine_counts[char] -= 1           # Use letter
```

## Edge Cases and Special Scenarios

### Case 1: Not Enough Letters
```python
ransomNote = "aaa", magazine = "aa"
# Only two 'a's available, need three → return False
```

### Case 2: Letters Not Present
```python
ransomNote = "abc", magazine = "def"
# None of the needed letters available → return False
```

### Case 3: Magazine Has Extra Letters
```python
ransomNote = "abc", magazine = "aabbccdd"
# All needed letters available → return True
```

### Case 4: Empty ransomNote
```python
ransomNote = "", magazine = "anything"
# No letters needed → return True
```

### Case 5: Empty magazine
```python
ransomNote = "a", magazine = ""
# No letters available → return False
```

## Common Pitfalls and Tips

### 1. Not Managing Inventory Correctly
```python
# ❌ Forgetting to decrement count after use
# May allow using same letter multiple times
```

### 2. Not Checking for Zero Count
```python
# ❌ Only checking if letter exists, not if enough copies
# magazine_counts[char] > 0 is essential
```

### 3. Inefficient String Operations
```python
# ❌ Using magazine.replace() repeatedly is slow for large strings
```

## Key Programming Concepts Demonstrated

1. **Hash Map Usage**: Efficient frequency counting and lookup
2. **Inventory Management**: Tracking available resources
3. **Single-Pass Algorithm**: Processing data efficiently
4. **Early Termination**: Stopping as soon as failure detected
5. **Space-Time Tradeoff**: Using extra space for speed

## Practice Tips

1. **Trace through examples**: Watch how counts change step by step
2. **Test edge cases**: Not enough letters, missing letters, empty strings
3. **Understand Counter behavior**: How it handles missing keys (returns 0)
4. **Remember to decrement**: Always reduce count after use

## Real-World Applications

1. **Resource Allocation**: Checking if requirements can be met from inventory
2. **Text Analysis**: Letter frequency matching
3. **Game Mechanics**: Crafting systems with limited resources
4. **Scheduling**: Assigning tasks with limited slots

## Why This Solution is Optimal

1. **Minimal Time Complexity**: O(m + n) is the best possible
2. **Practical Efficiency**: Counter operations are very fast
3. **Early Termination**: Stops immediately if impossible
4. **Clean Code**: Simple, readable, and maintainable
5. **Handles All Cases**: Works with duplicates, missing letters, and all edge cases

This algorithm demonstrates the power of hash maps for efficient resource tracking and constraint satisfaction in string manipulation problems.