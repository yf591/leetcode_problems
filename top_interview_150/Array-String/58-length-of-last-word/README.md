# 58. Length of Last Word - Solution Explanation

## Problem Overview
Given a string `s` consisting of words and spaces, return the length of the **last word** in the string.

A **word** is a maximal substring consisting of non-space characters only.

**Examples:**
- `s = "Hello World"` → `5` (length of "World")
- `s = "   fly me   to   the moon  "` → `4` (length of "moon")
- `s = "luffy is still joyboy"` → `6` (length of "joyboy")

**Constraints:**
- 1 ≤ s.length ≤ 10⁴
- `s` consists of only English letters and spaces `' '`
- There is **at least one word** in `s`

## Understanding the Problem

### Key Challenges
1. **Leading/trailing spaces**: Input may have extra whitespace
2. **Multiple consecutive spaces**: Words may be separated by multiple spaces
3. **Word identification**: Need to correctly identify word boundaries
4. **Last word extraction**: Must find the final word regardless of trailing spaces

### Visual Example
```
Input: "   fly me   to   the moon  "
                                ↑
                            Last word

Processing:
1. Remove leading/trailing: "fly me   to   the moon"
2. Split by spaces: ["fly", "me", "to", "the", "moon"]
3. Get last element: "moon"
4. Calculate length: 4
```

## Solution Approach

Our solution uses **Python's built-in string methods** for an elegant one-line solution:

```python
def lengthOfLastWord(self, s: str) -> int:
    return len(s.strip().split()[-1])
```

**Strategy:**
1. **Normalize** the string by removing leading/trailing whitespace
2. **Split** into individual words
3. **Extract** the last word
4. **Calculate** its length

## Step-by-Step Breakdown

### Step 1: strip() - Remove Leading/Trailing Whitespace
```python
s.strip()
```

**Purpose**: Clean the string by removing unnecessary whitespace at the beginning and end

**Transformation Examples:**
```python
"Hello World".strip()          → "Hello World"     # No change needed
"  Hello World  ".strip()      → "Hello World"     # Spaces removed
"   fly me to moon  ".strip()  → "fly me to moon"  # Clean boundaries
```

**Why is strip() important?**
```python
# Without strip(), trailing spaces could cause issues in other approaches
# strip() ensures clean word boundaries for reliable processing
```

### Step 2: split() - Tokenize into Words
```python
.split()
```

**Purpose**: Break the string into a list of individual words

**Key Features of split() without arguments:**
- Splits on **any whitespace** (spaces, tabs, newlines)
- **Consecutive whitespace** treated as single delimiter
- **No empty strings** in result
- **Automatic trimming** of whitespace

**Transformation Examples:**
```python
"Hello World".split()           → ["Hello", "World"]
"fly me   to   the moon".split() → ["fly", "me", "to", "the", "moon"]
"a  b    c".split()             → ["a", "b", "c"]  # Multiple spaces handled
```

**split() vs split(" ") comparison:**
```python
"a  b   c".split()     → ["a", "b", "c"]           # ✅ Clean result
"a  b   c".split(" ")  → ["a", "", "b", "", "", "c"] # ❌ Empty strings included
```

### Step 3: [-1] - Access Last Element
```python
.split()[-1]
```

**Purpose**: Retrieve the last word from the list of words

**Python Negative Indexing:**
```python
words = ["fly", "me", "to", "the", "moon"]
words[-1]  → "moon"     # Last element
words[-2]  → "the"      # Second to last
words[0]   → "fly"      # First element
```

**Why [-1] is reliable:**
- Always gets the last element regardless of list length
- Works with single-word strings: `["hello"][-1] → "hello"`
- Pythonic and readable

### Step 4: len() - Calculate String Length
```python
len(...)
```

**Purpose**: Count the number of characters in the last word

**Final Calculation:**
```python
len("moon")    → 4
len("joyboy")  → 6
len("World")   → 5
```

## Detailed Execution Traces

### Example 1: "Hello World"
```python
Input: s = "Hello World"

Step 1: s.strip()
"Hello World".strip() → "Hello World"  # No leading/trailing spaces

Step 2: .split()
"Hello World".split() → ["Hello", "World"]  # Split into 2 words

Step 3: [-1]
["Hello", "World"][-1] → "World"  # Get last word

Step 4: len()
len("World") → 5  # Count characters

Result: 5
```

### Example 2: "   fly me   to   the moon  "
```python
Input: s = "   fly me   to   the moon  "

Step 1: s.strip()
"   fly me   to   the moon  ".strip() → "fly me   to   the moon"
# Leading and trailing spaces removed

Step 2: .split()
"fly me   to   the moon".split() → ["fly", "me", "to", "the", "moon"]
# Multiple spaces between words handled automatically

Step 3: [-1]
["fly", "me", "to", "the", "moon"][-1] → "moon"
# Extract last word

Step 4: len()
len("moon") → 4
# Calculate length

Result: 4
```

### Example 3: "luffy is still joyboy"
```python
Input: s = "luffy is still joyboy"

Step 1: s.strip()
"luffy is still joyboy".strip() → "luffy is still joyboy"
# No change needed

Step 2: .split()
"luffy is still joyboy".split() → ["luffy", "is", "still", "joyboy"]
# Split into 4 words

Step 3: [-1]
["luffy", "is", "still", "joyboy"][-1] → "joyboy"
# Get last word

Step 4: len()
len("joyboy") → 6
# Count characters

Result: 6
```

## Edge Cases Handling

### Edge Case 1: Single Word
```python
Input: "hello"
Trace:
- strip(): "hello"
- split(): ["hello"]
- [-1]: "hello"
- len(): 5
Result: 5 ✓
```

### Edge Case 2: Single Word with Spaces
```python
Input: "  hello  "
Trace:
- strip(): "hello"
- split(): ["hello"]
- [-1]: "hello"
- len(): 5
Result: 5 ✓
```

### Edge Case 3: Multiple Consecutive Spaces
```python
Input: "hello    world"
Trace:
- strip(): "hello    world"
- split(): ["hello", "world"]  # Multiple spaces handled
- [-1]: "world"
- len(): 5
Result: 5 ✓
```

### Edge Case 4: Very Long Last Word
```python
Input: "a supercalifragilisticexpialidocious"
Trace:
- strip(): "a supercalifragilisticexpialidocious"
- split(): ["a", "supercalifragilisticexpialidocious"]
- [-1]: "supercalifragilisticexpialidocious"
- len(): 34
Result: 34 ✓
```

## Alternative Solutions Comparison

### Solution 1: Reverse Iteration (Space Optimal)
```python
def lengthOfLastWord(self, s: str) -> int:
    i = len(s) - 1
    
    # Skip trailing spaces
    while i >= 0 and s[i] == ' ':
        i -= 1
    
    # Count characters of last word
    length = 0
    while i >= 0 and s[i] != ' ':
        length += 1
        i -= 1
    
    return length
```

**Analysis:**
- ✅ **Space efficient**: O(1) space complexity
- ✅ **Early termination**: Stops when last word is found
- ❌ **More complex**: Multiple loops and conditions
- ❌ **Less readable**: Intent not immediately clear

### Solution 2: Regular Expressions
```python
import re

def lengthOfLastWord(self, s: str) -> int:
    words = re.findall(r'\S+', s)
    return len(words[-1]) if words else 0
```

**Analysis:**
- ✅ **Flexible**: Handles various whitespace patterns
- ✅ **Powerful**: Regex can handle complex cases
- ❌ **Import required**: Additional dependency
- ❌ **Overkill**: Regex unnecessary for this simple problem

### Solution 3: Manual Parsing
```python
def lengthOfLastWord(self, s: str) -> int:
    words = []
    current_word = ""
    
    for char in s:
        if char == ' ':
            if current_word:
                words.append(current_word)
                current_word = ""
        else:
            current_word += char
    
    if current_word:
        words.append(current_word)
    
    return len(words[-1]) if words else 0
```

**Analysis:**
- ✅ **Full control**: Complete control over parsing logic
- ✅ **Educational**: Shows manual string processing
- ❌ **Verbose**: Much more code required
- ❌ **Error-prone**: More opportunities for bugs

### Solution 4: Built-in rsplit()
```python
def lengthOfLastWord(self, s: str) -> int:
    return len(s.strip().rsplit()[-1])
```

**Analysis:**
- ✅ **Similar approach**: Using built-in methods
- ✅ **Functionally identical**: Same result as our solution
- ≈ **Performance**: Similar performance characteristics

## Why Our Solution is Optimal

### 1. **Pythonic Design**
```python
# Leverages Python's strengths
s.strip().split()[-1]
# Method chaining, built-in functions, negative indexing
```

### 2. **Readability Excellence**
```python
# Self-documenting code
# The operations clearly express the intent:
# "clean → split → get last → measure"
```

### 3. **Robust Error Handling**
```python
# Built-in methods handle edge cases automatically
# No need for manual null checks or boundary conditions
```

### 4. **Optimal Complexity for Use Case**
```python
# Time: O(n) - must examine entire string
# Space: O(n) - in practice, much less than n
# This is optimal for the given constraints
```

## Performance Analysis

### Time Complexity: O(n)
```python
s.strip()    # O(n) - scan entire string
.split()     # O(n) - process entire string  
[-1]         # O(1) - list access
len(...)     # O(1) - string length lookup
# Overall: O(n) where n = string length
```

### Space Complexity: O(w)
```python
.split()  # O(w) where w = number of words
# In practice: w << n (words much fewer than characters)
# Worst case: O(n) if every character is a single-character word
```

### Real-world Performance
```python
# For typical sentences (average word length ~5 characters):
# Space usage ≈ O(n/5) ≈ O(n) but with much better constant factor
# Memory efficiency is quite good in practice
```

### Benchmark Comparison
```python
# Our solution vs. reverse iteration:
# Time: Similar O(n) performance
# Space: Our solution uses more memory but provides better readability
# For LeetCode constraints (≤10⁴ characters), difference is negligible
```

## Key Programming Concepts Demonstrated

### 1. **Method Chaining**
```python
s.strip().split()[-1]
# Fluent interface pattern
# Each method returns a value that the next method can operate on
```

### 2. **Built-in Function Utilization**
```python
# strip(): String cleaning
# split(): Tokenization  
# [-1]: Negative indexing
# len(): Length calculation
```

### 3. **Functional Programming Style**
```python
# Immutable operations
# No side effects
# Composable transformations
```

### 4. **Problem Decomposition**
```python
# Break complex problem into simple steps:
# 1. Clean input
# 2. Extract structure
# 3. Select target
# 4. Compute result
```

## Real-World Applications

### 1. **Text Processing**
- **Log analysis**: Extract last component from file paths
- **Data cleaning**: Process user input with inconsistent spacing
- **Content management**: Parse article titles and headers

### 2. **Natural Language Processing**
- **Tokenization**: Preprocessing step for NLP pipelines
- **Feature extraction**: Last word analysis for sentiment analysis
- **Text normalization**: Clean text data for machine learning

### 3. **System Administration**
- **Command parsing**: Extract last argument from command lines
- **Path manipulation**: Get filename from full file paths
- **Configuration parsing**: Process space-separated configuration values

### 4. **Data Validation**
- **Input sanitization**: Clean user-provided text data
- **Format validation**: Ensure text meets expected patterns
- **Quality assurance**: Verify data consistency in text fields

## Best Practices Demonstrated

### 1. **Leverage Standard Library**
```python
# Use built-in functions when available
# They are optimized, tested, and reliable
```

### 2. **Write Self-Documenting Code**
```python
# Method names clearly indicate purpose
# Operation sequence tells a story
```

### 3. **Handle Edge Cases Gracefully**
```python
# strip() handles leading/trailing spaces
# split() handles multiple consecutive spaces
# Built-in robustness
```

### 4. **Optimize for Readability**
```python
# Code is read more than written
# Clear intent trumps micro-optimizations
# Maintainable solutions preferred
```

### 5. **Choose Appropriate Abstractions**
```python
# String methods abstract away low-level character manipulation
# Focus on problem logic rather than implementation details
```

## Common Pitfalls and How Our Solution Avoids Them

### Pitfall 1: Not Handling Multiple Spaces
```python
# ❌ Problem: split(' ') creates empty strings
"a  b".split(' ')  → ["a", "", "b"]

# ✅ Our solution: split() handles multiple spaces
"a  b".split()     → ["a", "b"]
```

### Pitfall 2: Forgetting Leading/Trailing Spaces
```python
# ❌ Problem: Trailing spaces affect parsing
"hello world  ".split()[-1]  → "world" (still works, but strip is cleaner)

# ✅ Our solution: strip() ensures clean boundaries
"hello world  ".strip().split()[-1]  → "world"
```

### Pitfall 3: Index Out of Bounds
```python
# ❌ Problem: Empty input could cause errors
# Our solution: Problem constraints guarantee at least one word

# ✅ Built-in robustness: split() always returns non-empty list for valid input
```

### Pitfall 4: Manual Character-by-Character Processing
```python
# ❌ Verbose and error-prone manual approach
# ✅ Our solution: Leverage tested built-in functions
```

This solution exemplifies excellent Python programming practices by combining simplicity, readability, and efficiency. The one-line implementation demonstrates mastery of Python's string manipulation capabilities while handling all edge cases robustly and elegantly.