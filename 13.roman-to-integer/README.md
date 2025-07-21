# 13. Roman to Integer - Solution Explanation

## Problem Overview
Convert a Roman numeral string to an integer. Roman numerals are represented by seven different symbols:

- I = 1
- V = 5  
- X = 10
- L = 50
- C = 100
- D = 500
- M = 1000

## Key Rules
1. Roman numerals are usually written largest to smallest from left to right
2. When a smaller numeral appears before a larger one, it represents subtraction:
   - IV = 4 (5-1)
   - IX = 9 (10-1)
   - XL = 40 (50-10)
   - XC = 90 (100-10)
   - CD = 400 (500-100)
   - CM = 900 (1000-100)

## Algorithm Explanation

### Step 1: Create Mapping
```python
roman_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
```
Maps each Roman numeral to its integer value.

### Step 2: Iterate Through String
```python
for i in range(len(s)):
```
Loop through each character in the Roman numeral string.

### Step 3: Check for Subtraction Cases
```python
if i + 1 < len(s) and roman_map[s[i]] < roman_map[s[i + 1]]:
    total -= roman_map[s[i]]
```
- Check if there's a next character
- If current value < next value, it's a subtraction case
- Subtract current value from total

### Step 4: Addition Cases
```python
else:
    total += roman_map[s[i]]
```
For normal cases, add the current value to total.

## Example Walkthrough
Input: "XIV" (14)

| i | s[i] | s[i+1] | Current Value | Next Value | Action | Total |
|---|------|--------|---------------|------------|---------|-------|
| 0 | X    | I      | 10           | 1          | Add 10  | 10    |
| 1 | I    | V      | 1            | 5          | Sub 1   | 9     |
| 2 | V    | -      | 5            | -          | Add 5   | 14    |

Final result: 14

## Time & Space Complexity
- **Time Complexity**: O(n) - single pass through the string
- **Space Complexity**: O(1) - constant space for the mapping dictionary