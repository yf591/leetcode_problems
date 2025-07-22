# 20. Valid Parentheses - Solution Explanation

## Problem Overview
Given a string containing just the characters `'('`, `')'`, `'['`, `']'`, `'{'` and `'}'`, determine if the input string has valid parentheses.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets
2. Open brackets must be closed in the correct order
3. Every close bracket has a corresponding open bracket of the same type

**Examples:**
- `"()"` → `True` ✅ Opens and closes correctly
- `"()[]{}"` → `True` ✅ All brackets properly matched
- `"{[()]}"` → `True` ✅ Correctly nested
- `"([)]"` → `False` ❌ Crossed/wrong order
- `"((("` → `False` ❌ Unclosed brackets
- `")"` → `False` ❌ Closing without opening

## Understanding Stack (LIFO)

A **Stack** works like a pile of books - you can only add or remove from the top:

```
Stack visualization:
┌─────────┐ ← Last item added (top)
│  Book 3 │   First to be removed
├─────────┤
│  Book 2 │  
├─────────┤
│  Book 1 │ ← First item added (bottom)
└─────────┘   Last to be removed

This is called LIFO: Last In, First Out
```

In Python, we use a list as a stack:
```python
stack = []             # Empty stack
stack.append("Book1")  # Add → ["Book1"]
stack.append("Book2")  # Add → ["Book1", "Book2"]
top_book = stack.pop() # Remove → ["Book1"], returns "Book2"
```

## Why Stack Works for Parentheses?

**Key Insight**: Valid parentheses follow LIFO pattern - the most recently opened bracket should be the first to close.

```
Correct: {[()]}
Open order:    { [ ( )
Close order:       ) ] }
→ Last opened ( closes first ✅

Incorrect: ([)]
Open order:    ( [
Close order:    ) ]  
→ Last opened [ doesn't close first ❌
```

## Step-by-Step Algorithm Breakdown

### Step 1: Initialize Stack
```python
stack = []
```
**Purpose**: Create an empty container to track opening brackets
**Think of it as**: An empty box to store unmatched opening brackets

### Step 2: Create Bracket Mapping
```python
bracket_map = {")": "(", "]": "[", "}": "{"}
```
**Purpose**: Map each closing bracket to its corresponding opening bracket

| Closing Bracket | Corresponding Opening Bracket |
|------------------|-------------------------------|
| `)`             | `(`                          |
| `]`             | `[`                          |
| `}`             | `{`                          |

### Step 3: Process Each Character
```python
for char in s:
```
**Purpose**: Examine each character in the string from left to right

### Step 4: Handle Closing Brackets
```python
if char in bracket_map:  # This is a closing bracket
```
**How to identify**: Check if the character exists as a key in our mapping dictionary

#### Sub-step 4a: Validation Check
```python
if not stack or stack[-1] != bracket_map[char]:
    return False
```

**Breaking this down:**

**`if not stack`**: 
- **Meaning**: Is the stack empty?
- **Why check**: If we have a closing bracket but no opening bracket was stored, it's invalid
- **Example**: String `")"` - we see `)` but have no `(` stored

**`stack[-1] != bracket_map[char]`**:
- **`stack[-1]`**: The most recent (top) opening bracket
- **`bracket_map[char]`**: The required opening bracket for current closing bracket
- **Why check**: The most recent opening bracket must match the current closing bracket
- **Example**: Stack has `[` but we see `)` - they don't match!

#### Sub-step 4b: Remove Matched Bracket
```python
stack.pop()
```
**Purpose**: Remove the matched opening bracket since it's now properly closed

### Step 5: Handle Opening Brackets
```python
else:  # This is an opening bracket
    stack.append(char)
```
**Purpose**: Store the opening bracket for future matching with its closing counterpart

### Step 6: Final Validation
```python
return not stack
```
**Purpose**: Check if all brackets were properly matched
- **Empty stack (`[]`)** → `not []` → `True` ✅ All brackets matched
- **Non-empty stack (`['(']`)** → `not ['(']` → `False` ❌ Some brackets unclosed

## Detailed Example Walkthroughs

### Example 1: `"()"` ✅
| Step | Character | Type | Action | Stack After | Explanation |
|------|-----------|------|---------|-------------|-------------|
| 1 | `(` | Opening | `stack.append('(')` | `['(']` | Store opening bracket |
| 2 | `)` | Closing | Check & `stack.pop()` | `[]` | `(` matches `)`, remove it |
| Final | - | - | `return not []` | - | Empty stack → `True` |

### Example 2: `"{[()]}"` ✅
| Step | Character | Type | Action | Stack After | Explanation |
|------|-----------|------|---------|-------------|-------------|
| 1 | `{` | Opening | `stack.append('{')` | `['{']` | Store opening bracket |
| 2 | `[` | Opening | `stack.append('[')` | `['{', '[']` | Store opening bracket |
| 3 | `(` | Opening | `stack.append('(')` | `['{', '[', '(']` | Store opening bracket |
| 4 | `)` | Closing | Check `(` & `stack.pop()` | `['{', '[']` | `(` matches `)`, remove |
| 5 | `]` | Closing | Check `[` & `stack.pop()` | `['{']` | `[` matches `]`, remove |
| 6 | `}` | Closing | Check `{` & `stack.pop()` | `[]` | `{` matches `}`, remove |
| Final | - | - | `return not []` | - | Empty stack → `True` |

### Example 3: `"([)]"` ❌ (Crossed)
| Step | Character | Type | Action | Stack After | Explanation |
|------|-----------|------|---------|-------------|-------------|
| 1 | `(` | Opening | `stack.append('(')` | `['(']` | Store opening bracket |
| 2 | `[` | Opening | `stack.append('[')` | `['(', '[']` | Store opening bracket |
| 3 | `)` | Closing | Check `[` vs `(` | - | Top is `[` but `)` needs `(` |
| - | - | - | `return False` | - | Mismatch detected! |

### Example 4: `"((("` ❌ (Unclosed)
| Step | Character | Type | Action | Stack After | Explanation |
|------|-----------|------|---------|-------------|-------------|
| 1 | `(` | Opening | `stack.append('(')` | `['(']` | Store opening bracket |
| 2 | `(` | Opening | `stack.append('(')` | `['(', '(']` | Store opening bracket |
| 3 | `(` | Opening | `stack.append('(')` | `['(', '(', '(']` | Store opening bracket |
| Final | - | - | `return not ['(', '(', '(']` | - | Stack not empty → `False` |

## Why This Algorithm Works

### 1. LIFO Matches Bracket Behavior
- **Natural nesting**: Brackets form nested structures
- **Last opened, first closed**: Valid brackets follow this pattern
- **Stack enforces order**: LIFO ensures proper matching sequence

### 2. Efficient Detection of Invalid Cases
- **Empty stack + closing bracket**: No opening bracket to match
- **Wrong bracket type**: Stack top doesn't match closing bracket
- **Unclosed brackets**: Non-empty stack at the end

### 3. Early Termination
- **Immediate failure**: Returns `False` as soon as mismatch is detected
- **No unnecessary processing**: Doesn't continue checking after finding error

## Alternative Approaches (Less Efficient)

### Approach 1: Counter Method ❌
```python
def isValid(self, s: str) -> bool:
    count = {'(': 0, '[': 0, '{': 0}
    for char in s:
        if char in count:
            count[char] += 1
        elif char == ')':
            count['('] -= 1
        # ... similar for other brackets
    return all(c == 0 for c in count.values())
```
**Problem**: Cannot detect crossed brackets like `"([)]"` - counts are balanced but order is wrong!

### Approach 2: String Replace Method ❌
```python
def isValid(self, s: str) -> bool:
    while '()' in s or '[]' in s or '{}' in s:
        s = s.replace('()', '').replace('[]', '').replace('{}', '')
    return s == ''
```
**Problems**: 
- **Time complexity**: O(n²) - multiple passes through string
- **String immutability**: Creates new strings repeatedly in Python

## Time & Space Complexity Analysis

### Current Solution (Stack)
- **Time Complexity**: **O(n)** where n = length of string
  - Single pass through the string
  - Each character processed once
  - Stack operations (push/pop) are O(1)

- **Space Complexity**: **O(n)** in worst case
  - **Worst case**: All opening brackets `"(((((("`
  - **Best case**: O(1) when invalid bracket found early
  - **Average case**: O(n/2) for balanced strings

### Space Complexity Examples
```python
"((((((": O(n) - all brackets stored
"()()()": O(1) - brackets matched immediately  
"([)]":   O(1) - fails early, minimal storage
```

## Edge Cases Handled

| Input | Output | Reason |
|-------|--------|---------|
| `""` | `True` | Empty string is valid by definition |
| `"("` | `False` | Single opening bracket, unclosed |
| `")"` | `False` | Single closing bracket, no opening |
| `"())"` | `False` | Extra closing bracket |
| `"(()"` | `False` | Extra opening bracket |
| `"(]"` | `False` | Wrong bracket type |

## Key Programming Concepts Demonstrated

1. **Stack Data Structure**: LIFO principle for nested structures
2. **Dictionary Lookup**: O(1) bracket type checking
3. **Early Termination**: Efficient failure detection
4. **Boolean Logic**: `not stack` for emptiness check
5. **String Iteration**: Character-by-character processing

## Tips for Understanding
1. **Visualize the stack**: Draw it out as you trace through examples
2. **Think like matching parentheses**: Last opened must close first
3. **Practice with examples**: Try `"({[]})"` vs `"({[}])"`
4. **Remember LIFO**: Stack = pile of books, only touch the top!

This algorithm elegantly solves the parentheses validation problem by leveraging the natural LIFO behavior of stacks to match the required nesting structure of valid parentheses.