# 9. Palindrome Number - Solution Explanation

## Problem Overview
Determine whether an integer is a palindrome. A palindrome reads the same backward as forward.

Examples:
- 121 → True (reads as 121 both ways)
- -121 → False (reads as 121- backward)
- 10 → False (reads as 01 backward, which is 1)

## Algorithm Explanation

### Step 1: Handle Negative Numbers
```python
if x < 0:
    return False
```
Negative numbers cannot be palindromes because the minus sign only appears at the beginning.

### Step 2: Convert to String and Compare
```python
return str(x) == str(x)[::-1]
```

This line does three things:
1. `str(x)` - converts integer to string
2. `str(x)[::-1]` - reverses the string using Python slice notation
3. Compares original string with reversed string

## Understanding `[::-1]`
The slice notation `[::-1]` means:
- `start`: empty (defaults to beginning)
- `stop`: empty (defaults to end)
- `step`: -1 (move backwards)

## Example Walkthrough

### Example 1: x = 121
1. `str(121)` → `"121"`
2. `str(121)[::-1]` → `"121"`
3. `"121" == "121"` → `True`

### Example 2: x = -121
1. Negative check: `x < 0` → `True`
2. Return `False` immediately

### Example 3: x = 123
1. `str(123)` → `"123"`
2. `str(123)[::-1]` → `"321"`
3. `"123" == "321"` → `False`

## Alternative Approach (Mathematical)
You could also reverse the number mathematically without string conversion:

```python
def isPalindrome(self, x: int) -> bool:
    if x < 0:
        return False
    
    original = x
    reversed_num = 0
    
    while x > 0:
        reversed_num = reversed_num * 10 + x % 10
        x //= 10
    
    return original == reversed_num
```

## Time & Space Complexity

### String Approach (Current Solution)
- **Time Complexity**: O(log n) - where n is the input number (digits count)
- **Space Complexity**: O(log n) - for string storage

### Mathematical Approach
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1) - constant space

## Pros and Cons

### String Approach
- ✅ Simple and readable
- ✅ Easy to understand
- ❌ Uses extra space for string conversion

### Mathematical Approach  
- ✅ No extra space needed
- ✅ More efficient
- ❌ More complex logic
- ❌ Need to handle integer overflow in other languages