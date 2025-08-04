# 14. Longest Common Prefix - Solution Explanation

## Problem Overview
Find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string.

Examples:
- `["flower","flow","flight"]` → `"fl"`
- `["dog","racecar","car"]` → `""` (no common prefix)
- `["interspecies","interstellar","interstate"]` → `"inters"`

## Algorithm Explanation

### Step 1: Handle Empty Input
```python
if not strs:
    return ""
```
If the input list is empty, there's no possible common prefix, so return an empty string.

### Step 2: Use `zip(*strs)` Magic ✨
```python
for char_tuple in zip(*strs):
```

**How `zip(*strs)` works:**
- `zip(*strs)` unpacks the list and groups characters at the same position
- For `["flower", "flow", "flight"]`, it creates:
  - `('f', 'f', 'f')` - 1st characters from all strings
  - `('l', 'l', 'l')` - 2nd characters from all strings  
  - `('o', 'o', 'i')` - 3rd characters from all strings
  - `('w', 'w', 'g')` - 4th characters from all strings
  - ...

### Step 3: Check Character Consistency
```python
if len(set(char_tuple)) == 1:
    prefix.append(char_tuple[0])
else:
    break
```

**Using `set()` for comparison:**
- `set(char_tuple)` removes duplicates
- If all characters are the same → set size = 1
- If any character differs → set size > 1

**Examples:**
- `set(('f', 'f', 'f'))` → `{'f'}` (length = 1, all same)
- `set(('o', 'o', 'i'))` → `{'o', 'i'}` (length = 2, different chars)

### Step 4: Build Result
```python
return "".join(prefix)
```
Join all collected common characters into a single string.

## Example Walkthrough
Input: `["flower", "flow", "flight"]`

| Round | char_tuple | set(char_tuple) | len(set) | Action | prefix |
|-------|------------|-----------------|----------|---------|--------|
| 1 | ('f', 'f', 'f') | {'f'} | 1 | Add 'f' | ['f'] |
| 2 | ('l', 'l', 'l') | {'l'} | 1 | Add 'l' | ['f', 'l'] |
| 3 | ('o', 'o', 'i') | {'o', 'i'} | 2 | Break | ['f', 'l'] |

**Result:** `"fl"`

## Alternative Approach (Vertical Scanning)
```python
def longestCommonPrefix(self, strs: List[str]) -> str:
    if not strs:
        return ""
    
    # Use first string as reference
    for i in range(len(strs[0])):
        char = strs[0][i]
        # Check if this character exists in all other strings at position i
        for j in range(1, len(strs)):
            if i >= len(strs[j]) or strs[j][i] != char:
                return strs[0][:i]
    
    return strs[0]
```

## Alternative Approach (Horizontal Scanning)
```python
def longestCommonPrefix(self, strs: List[str]) -> str:
    if not strs:
        return ""
    
    prefix = strs[0]  # Start with first string as prefix
    
    for s in strs[1:]:
        # Keep reducing prefix until it matches start of current string
        while prefix and not s.startswith(prefix):
            prefix = prefix[:-1]  # Remove last character
    
    return prefix
```

## Algorithm Comparison

### Current Solution (Zip + Set)
- ✅ **Pythonic**: Uses Python's built-in functions elegantly
- ✅ **Readable**: Clear intent with `zip(*strs)` and `set()`
- ✅ **Early termination**: Stops immediately when difference found
- ❌ **Memory**: Creates tuples for each position

### Vertical Scanning
- ✅ **Efficient**: Direct character comparison
- ✅ **Memory efficient**: No extra data structures
- ❌ **More code**: Requires nested loops

### Horizontal Scanning
- ✅ **Intuitive**: Easy to understand logic
- ✅ **Simple**: Uses string methods
- ❌ **Potentially slower**: May scan same characters multiple times

## Time & Space Complexity

### Current Solution
- **Time Complexity**: O(S) - where S is the sum of all characters in all strings
- **Space Complexity**: O(m) - where m is the length of the common prefix

### Key Insights
- `zip()` automatically stops when the shortest string is exhausted
- `set()` provides O(1) uniqueness check for small character sets
- Early termination makes this very efficient for strings with short common prefixes

## Edge Cases Handled
- Empty input list: Returns `""`
- Single string: Returns the string itself
- No common prefix: Returns `""` after first difference
- Strings of different lengths: `zip()` handles gracefully