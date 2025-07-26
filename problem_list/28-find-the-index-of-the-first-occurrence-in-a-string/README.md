# 28. Find the Index of the First Occurrence in a String - Solution Explanation

## Problem Overview
Given two strings `needle` and `haystack`, return the index of the first occurrence of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`.

**Examples:**
- `haystack = "sadbutsad"`, `needle = "sad"` → `0`
- `haystack = "leetcode"`, `needle = "leeto"` → `-1`
- `haystack = "hello"`, `needle = ""` → `0`

**Constraints:**
- 1 ≤ haystack.length, needle.length ≤ 10⁴
- `haystack` and `needle` consist of only lowercase English characters

## Understanding the Problem

### What We're Looking For
We need to find the **first position** where the substring `needle` appears in the string `haystack`.

**Key Points:**
- Return the **index** (0-based position), not the substring itself
- Return `-1` if not found
- Empty `needle` should return `0` (by convention)

### Visual Example
```
haystack: "sadbutsad"
needle:   "sad"

Position: 0123456789
String:   "sadbutsad"
          ^^^
          Found at index 0

haystack: "sadbutsad"  
needle:   "but"

Position: 0123456789
String:   "sadbutsad"
             ^^^
             Found at index 3
```

## Solution Approaches

### Approach 1: Built-in Method (Pythonic)
```python
def strStr(self, haystack: str, needle: str) -> int:
    return haystack.find(needle)
```

**Advantages:**
- ✅ **Concise**: Single line solution
- ✅ **Efficient**: Uses optimized built-in implementation
- ✅ **Reliable**: Well-tested standard library function
- ✅ **Readable**: Clear intent

**Disadvantages:**
- ❌ **Interview perspective**: Doesn't demonstrate algorithmic thinking
- ❌ **Language-specific**: Not portable to other languages
- ❌ **Learning value**: Doesn't teach underlying concepts

### Approach 2: Manual Implementation (Current Solution)
```python
def strStr(self, haystack: str, needle: str) -> int:
    if not needle:
        return 0
    
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i:i + len(needle)] == needle:
            return i
    
    return -1
```

This is our **recommended approach** for interviews as it demonstrates understanding of the algorithm.

## Step-by-Step Algorithm Breakdown

### Step 1: Handle Edge Case
```python
if not needle:
    return 0
```
**Purpose**: Handle empty needle string
**Convention**: Empty substring is considered to be found at position 0

### Step 2: Calculate Search Range
```python
for i in range(len(haystack) - len(needle) + 1):
```
**Logic**: We only need to check positions where `needle` can fully fit
**Range calculation**:
- `haystack` length: n
- `needle` length: m  
- Valid starting positions: 0 to (n - m)
- Range: `len(haystack) - len(needle) + 1`

**Example:**
```
haystack = "abcde" (length 5)
needle = "cd" (length 2)
Valid positions: 0, 1, 2, 3 (positions 4 would go out of bounds)
Range: 5 - 2 + 1 = 4 positions
```

### Step 3: Check Substring Match
```python
if haystack[i:i + len(needle)] == needle:
    return i
```
**String slicing**: `haystack[i:i + len(needle)]` extracts substring of needle's length
**Comparison**: Direct string comparison for match
**Early return**: Return immediately when first match found

### Step 4: Return Not Found
```python
return -1
```
**Purpose**: Return -1 if no match found after checking all positions

## Detailed Example Walkthrough

**Input:** `haystack = "sadbutsad"`, `needle = "sad"`

### Initial Setup
```
haystack = "sadbutsad" (length 9)
needle = "sad" (length 3)
Search range: 9 - 3 + 1 = 7 positions (0 to 6)
```

### Iteration by Iteration

#### i=0: Check position 0
```
haystack[0:3] = "sad"
needle = "sad"
"sad" == "sad" → Match found!
Return 0
```

**Result**: Function returns `0` immediately (early termination)

### Another Example: Not Found Case

**Input:** `haystack = "leetcode"`, `needle = "leeto"`

#### Setup
```
haystack = "leetcode" (length 8)
needle = "leeto" (length 5)
Search range: 8 - 5 + 1 = 4 positions (0 to 3)
```

#### Step-by-Step Search
| i | Substring | Match? | Action |
|---|-----------|--------|---------|
| 0 | "leetc" | ❌ No | Continue |
| 1 | "eetco" | ❌ No | Continue |
| 2 | "etcod" | ❌ No | Continue |
| 3 | "tcode" | ❌ No | Continue |

**Result**: No matches found, return `-1`

## Alternative Implementation: Character-by-Character

### More Explicit Approach
```python
def strStr(self, haystack: str, needle: str) -> int:
    if not needle:
        return 0
    
    for i in range(len(haystack) - len(needle) + 1):
        # Check character by character
        match = True
        for j in range(len(needle)):
            if haystack[i + j] != needle[j]:
                match = False
                break
        
        if match:
            return i
    
    return -1
```

**Advantages:**
- More explicit about the matching process
- Easier to optimize (early termination on mismatch)
- Better for understanding the algorithm

**Current approach advantages:**
- More concise and readable
- Leverages Python's efficient string comparison
- Less prone to index errors

## Advanced Algorithms (For Reference)

### KMP (Knuth-Morris-Pratt) Algorithm
```python
def strStr(self, haystack: str, needle: str) -> int:
    if not needle:
        return 0
    
    # Build partial match table (failure function)
    def build_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    lps = build_lps(needle)
    i = j = 0
    
    while i < len(haystack):
        if haystack[i] == needle[j]:
            i += 1
            j += 1
        
        if j == len(needle):
            return i - j
        elif i < len(haystack) and haystack[i] != needle[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return -1
```

**Time Complexity**: O(n + m)
**Use case**: When you need optimal performance for large strings

### Rabin-Karp Algorithm (Rolling Hash)
```python
def strStr(self, haystack: str, needle: str) -> int:
    if not needle:
        return 0
    
    base = 256
    mod = 101
    
    needle_hash = 0
    window_hash = 0
    h = 1
    
    # Calculate hash value for needle and first window
    for i in range(len(needle)):
        needle_hash = (needle_hash * base + ord(needle[i])) % mod
        window_hash = (window_hash * base + ord(haystack[i])) % mod
        if i < len(needle) - 1:
            h = (h * base) % mod
    
    # Slide the window
    for i in range(len(haystack) - len(needle) + 1):
        if needle_hash == window_hash:
            # Hash match, verify character by character
            if haystack[i:i + len(needle)] == needle:
                return i
        
        # Calculate hash for next window
        if i < len(haystack) - len(needle):
            window_hash = (base * (window_hash - ord(haystack[i]) * h) + ord(haystack[i + len(needle)])) % mod
            if window_hash < 0:
                window_hash += mod
    
    return -1
```

**Average Time Complexity**: O(n + m)
**Use case**: Good for multiple pattern searching

## Time & Space Complexity Analysis

### Current Solution (Substring Comparison)
- **Time Complexity**: **O(n × m)** where n = haystack length, m = needle length
  - Outer loop: O(n - m + 1) ≈ O(n)
  - String comparison: O(m) in worst case
  - Total: O(n × m)

- **Space Complexity**: **O(1)** - constant extra space
  - Only uses loop variables
  - String slicing in Python creates temporary strings, but this is implementation detail

### Complexity Comparison
| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| **Brute Force (current)** | **O(n×m)** | **O(1)** | **Simple and effective** |
| Built-in find() | Varies | O(1) | Usually optimized |
| KMP | O(n+m) | O(m) | Optimal time, extra space |
| Rabin-Karp | O(n+m) avg | O(1) | Good for multiple patterns |

## Edge Cases Handled

### Empty Needle
```python
haystack = "abc", needle = ""
# Result: 0 (empty string found at position 0)
```

### Needle Longer than Haystack
```python
haystack = "a", needle = "aa"
# Range: 1 - 2 + 1 = 0 (no iterations)
# Result: -1
```

### Single Character
```python
haystack = "a", needle = "a"
# Result: 0

haystack = "a", needle = "b"  
# Result: -1
```

### Identical Strings
```python
haystack = "hello", needle = "hello"
# Result: 0
```

### Multiple Occurrences
```python
haystack = "ababab", needle = "ab"
# Result: 0 (first occurrence)
```

## Common Pitfalls and Tips

### 1. Incorrect Range Calculation
```python
# ❌ Wrong: Allows out-of-bounds access
for i in range(len(haystack)):
    if haystack[i:i + len(needle)] == needle:  # May go past end

# ✅ Correct: Proper boundary check
for i in range(len(haystack) - len(needle) + 1):
    if haystack[i:i + len(needle)] == needle:
```

### 2. Forgetting Empty Needle Case
```python
# ❌ Incomplete: Missing edge case
def strStr(self, haystack, needle):
    for i in range(len(haystack) - len(needle) + 1):
        # What if needle is empty?

# ✅ Complete: Handle empty needle
def strStr(self, haystack, needle):
    if not needle:
        return 0
    # ... rest of algorithm
```

### 3. Wrong Return Value
```python
# ❌ Wrong: Returning boolean or substring
if haystack[i:i + len(needle)] == needle:
    return True  # Should return index

# ✅ Correct: Return index
if haystack[i:i + len(needle)] == needle:
    return i
```

### 4. Off-by-One Errors
```python
# ❌ Wrong: Missing +1 in range
for i in range(len(haystack) - len(needle)):  # Misses last valid position

# ✅ Correct: Include +1
for i in range(len(haystack) - len(needle) + 1):
```

## Interview Strategy

### 1. Start with Built-in Solution
```python
# "The most straightforward approach would be:"
return haystack.find(needle)
# "But let me implement it manually to show my understanding."
```

### 2. Implement Manual Solution
```python
# Current approach - clear and correct
def strStr(self, haystack: str, needle: str) -> int:
    if not needle:
        return 0
    
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i:i + len(needle)] == needle:
            return i
    
    return -1
```

### 3. Discuss Optimizations
- "For better time complexity, we could use KMP algorithm"
- "For multiple pattern matching, Rabin-Karp might be better"
- "The current solution is O(n×m) but simple and readable"

### 4. Consider Follow-up Questions
- What if we need to find all occurrences?
- What about case-insensitive matching?
- How would you handle Unicode strings?

## Real-World Applications

1. **Text Search**: Finding words in documents
2. **DNA Sequence Analysis**: Finding genetic patterns
3. **Log Analysis**: Searching for specific patterns in logs
4. **Autocomplete**: Substring matching for suggestions
5. **Plagiarism Detection**: Finding copied text segments
6. **Web Scraping**: Extracting specific content patterns

## Key Programming Concepts Demonstrated

1. **String Manipulation**: Substring extraction and comparison
2. **Loop Optimization**: Calculating proper iteration bounds
3. **Edge Case Handling**: Managing empty inputs
4. **Early Termination**: Returning as soon as result found
5. **Algorithm Trade-offs**: Balancing simplicity vs. performance

This algorithm demonstrates a fundamental string searching technique with clear, readable code that handles all edge cases while maintaining reasonable performance for most practical applications.