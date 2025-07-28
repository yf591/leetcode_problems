# 66. Plus One - Solution Explanation

## Problem Overview
You are given a **large integer** represented as an integer array `digits`, where each `digits[i]` is the ith digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading zero.

Increment the large integer by one and return the resulting array of digits.

**Examples:**
- `digits = [1,2,3]` → `[1,2,4]` (123 + 1 = 124)
- `digits = [4,3,2,1]` → `[4,3,2,2]` (4321 + 1 = 4322)
- `digits = [9]` → `[1,0]` (9 + 1 = 10)
- `digits = [9,9]` → `[1,0,0]` (99 + 1 = 100)

**Constraints:**
- 1 ≤ digits.length ≤ 100
- 0 ≤ digits[i] ≤ 9
- `digits` does not contain any leading zeros except for the number 0 itself

## Understanding the Problem

### Mathematical Foundation
Adding 1 to a number follows the same rules as manual arithmetic:
1. **Start from the rightmost digit** (least significant)
2. **Add 1 to that digit**
3. **Handle carry-over** if the result is ≥ 10
4. **Propagate carry** to the left until no more carry is needed

### Three Distinct Cases
1. **No carry needed**: Last digit < 9 → simply add 1 and finish
2. **Partial carry**: Some 9s become 0s, but we hit a non-9 digit
3. **Full carry**: All digits are 9s → need to add a new leading digit

### Visual Example
```
Case 1: [1,2,3] + 1
        [1,2,4] ← Simple addition, no carry

Case 2: [1,9,9] + 1  
        [1,9,9] → [1,9,0] → [1,0,0] → [2,0,0]
         ↑carry    ↑carry    ↑add 1

Case 3: [9,9] + 1
        [9,9] → [9,0] → [0,0] → [1,0,0]
         ↑carry  ↑carry  ↑new digit
```

## Solution Approach

Our solution uses **right-to-left iteration with carry propagation**:

```python
def plusOne(self, digits: List[int]) -> List[int]:
    n = len(digits)
    
    # Iterate through the digits from right to left
    for i in range(n - 1, -1, -1):
        # If the current digit is less than 9, we can just add one
        # and there's no need to 'carry over'. We can return immediately.
        if digits[i] < 9:
            digits[i] += 1
            return digits
        
        # If the digit is 9, it becomes 0, and the 'carry' will be
        # handled by adding one to the next digit in the loop.
        digits[i] = 0
    
    # If the loop completes, it means all digits were 9s(e.g., [9, 9]).
    # The array has become all 0s (e.g., [0, 0]). and we need to add a leading 1.
    return [1] + digits
```

**Strategy:**
1. **Right-to-left traversal**: Process digits in natural arithmetic order
2. **Early termination**: Return immediately when no carry is needed
3. **Carry propagation**: Convert 9s to 0s and continue
4. **Overflow handling**: Add leading 1 when all digits were 9s

## Step-by-Step Breakdown

### Step 1: Initialize Array Length
```python
n = len(digits)
```

**Purpose**: Store array length for the reverse iteration range

### Step 2: Right-to-Left Iteration
```python
for i in range(n - 1, -1, -1):
```

**Iteration Pattern:**
```python
# For digits = [1,2,3] (n=3):
range(2, -1, -1)  # Produces: 2, 1, 0
# Processing order: digits[2] → digits[1] → digits[0]
```

**Why Right-to-Left?**
- **Mathematical correctness**: Addition starts from least significant digit
- **Carry propagation**: Natural direction for overflow handling
- **Early termination**: Most additions don't require full array traversal

### Step 3: Case 1 - No Carry Needed
```python
if digits[i] < 9:
    digits[i] += 1
    return digits
```

**Condition**: Current digit is less than 9
**Action**: Add 1 and immediately return

**Why Immediate Return?**
- No carry is generated
- All higher-order digits remain unchanged
- Further processing is unnecessary

**Execution Examples:**
```python
# Example: [1,2,3]
i=2: digits[2]=3 < 9 → digits[2]=4, return [1,2,4]

# Example: [4,3,2,1]  
i=3: digits[3]=1 < 9 → digits[3]=2, return [4,3,2,2]

# Example: [5,6,7,8]
i=3: digits[3]=8 < 9 → digits[3]=9, return [5,6,7,9]
```

### Step 4: Case 2 - Carry Propagation
```python
digits[i] = 0
```

**Condition**: Current digit equals 9
**Action**: Set to 0 and continue to next iteration

**Carry Logic:**
- 9 + 1 = 10 → write 0, carry 1
- The "carry 1" is handled by the next loop iteration
- Continue until we find a non-9 digit or exhaust all digits

**Execution Example:**
```python
# Example: [1,9,9]
i=2: digits[2]=9 → digits[2]=0, continue  # [1,9,0]
i=1: digits[1]=9 → digits[1]=0, continue  # [1,0,0]  
i=0: digits[0]=1 < 9 → digits[0]=2, return [2,0,0]
```

### Step 5: Case 3 - All Digits Were 9s
```python
return [1] + digits
```

**Condition**: Loop completes without early return
**Meaning**: All original digits were 9s
**Result**: Array is now all 0s, prepend 1

**Why This Works:**
```python
# Original: [9,9,9]
# After loop: [0,0,0] (all 9s became 0s)
# Final result: [1] + [0,0,0] = [1,0,0,0]
# Represents: 1000 (which is 999 + 1)
```

## Detailed Execution Traces

### Example 1: [1,2,3] → [1,2,4] (No Carry)
```python
Input: digits = [1,2,3], n = 3

Loop: for i in range(2, -1, -1):  # i = 2, 1, 0

i=2: digits[2] = 3
     3 < 9? Yes
     → digits[2] = 3 + 1 = 4
     → return [1,2,4] ✓

Result: [1,2,4]
```

### Example 2: [1,9,9] → [2,0,0] (Partial Carry)
```python
Input: digits = [1,9,9], n = 3

Loop: for i in range(2, -1, -1):  # i = 2, 1, 0

i=2: digits[2] = 9
     9 < 9? No
     → digits[2] = 0
     → continue
     State: [1,9,0]

i=1: digits[1] = 9  
     9 < 9? No
     → digits[1] = 0
     → continue
     State: [1,0,0]

i=0: digits[0] = 1
     1 < 9? Yes
     → digits[0] = 1 + 1 = 2
     → return [2,0,0] ✓

Result: [2,0,0]
```

### Example 3: [9,9] → [1,0,0] (Full Carry)
```python
Input: digits = [9,9], n = 2

Loop: for i in range(1, -1, -1):  # i = 1, 0

i=1: digits[1] = 9
     9 < 9? No
     → digits[1] = 0
     → continue
     State: [9,0]

i=0: digits[0] = 9
     9 < 9? No  
     → digits[0] = 0
     → continue
     State: [0,0]

# Loop completes without return
return [1] + [0,0] = [1,0,0] ✓

Result: [1,0,0]
```

### Example 4: [9] → [1,0] (Single Digit Overflow)
```python
Input: digits = [9], n = 1

Loop: for i in range(0, -1, -1):  # i = 0

i=0: digits[0] = 9
     9 < 9? No
     → digits[0] = 0  
     → continue
     State: [0]

# Loop completes without return
return [1] + [0] = [1,0] ✓

Result: [1,0]
```

## Algorithm Efficiency Analysis

### Time Complexity: O(n) in worst case, O(1) on average

**Best Case: O(1)**
```python
# When last digit < 9 (90% of cases)
[1,2,3] → One operation, immediate return
```

**Average Case: O(1)**
```python
# Most real-world additions don't cause extensive carry
# Early termination handles majority of cases efficiently
```

**Worst Case: O(n)**
```python
# When all digits are 9s (rare)
[9,9,9,9] → Must process every digit
```

### Space Complexity: O(1) in best case, O(n) in worst case

**Best Case: O(1)**
```python
# In-place modification when no overflow
# No additional arrays created
```

**Worst Case: O(n)**
```python
# Only when creating [1] + digits for overflow case
# Still optimal as new digit is mathematically necessary
```

### Real-World Performance
```python
# Statistical distribution:
# ~90%: O(1) time, O(1) space (no carry)
# ~9%:  O(k) time, O(1) space (k consecutive 9s)  
# ~1%:  O(n) time, O(n) space (all 9s)
```

## Edge Cases and Robustness

### Edge Case 1: Single Digit (Non-9)
```python
Input: [5]
Process: 5 < 9 → 5+1 = 6
Output: [6] ✓
```

### Edge Case 2: Single Digit (9)
```python
Input: [9]
Process: 9 → 0, loop ends → [1] + [0]
Output: [1,0] ✓
```

### Edge Case 3: Leading Non-9 with Trailing 9s
```python
Input: [1,9,9,9]
Process: 9→0, 9→0, 9→0, 1→2
Output: [2,0,0,0] ✓
```

### Edge Case 4: Large Number of 9s
```python
Input: [9,9,9,9,9]
Process: All 9s → all 0s → prepend 1
Output: [1,0,0,0,0,0] ✓
```

### Edge Case 5: Mixed Digits with Internal 9s
```python
Input: [8,9,9,5]
Process: 5 < 9 → 5+1 = 6, immediate return
Output: [8,9,9,6] ✓
```

## Alternative Solutions Comparison

### Solution 1: Convert to Integer (Naive Approach)
```python
def plusOne(self, digits: List[int]) -> List[int]:
    # Convert array to integer
    num = int(''.join(map(str, digits)))
    # Add 1
    num += 1
    # Convert back to array
    return [int(d) for d in str(num)]
```

**Analysis:**
- ✅ **Simple to understand**: Straightforward conversion approach
- ❌ **Integer overflow**: Fails for very large numbers
- ❌ **Performance overhead**: String conversion costs
- ❌ **Memory inefficient**: Multiple temporary objects

### Solution 2: Recursive Approach
```python
def plusOne(self, digits: List[int]) -> List[int]:
    def add_one(arr, index):
        if index < 0:
            return [1] + arr
        
        if arr[index] < 9:
            arr[index] += 1
            return arr
        
        arr[index] = 0
        return add_one(arr, index - 1)
    
    return add_one(digits, len(digits) - 1)
```

**Analysis:**
- ✅ **Elegant recursion**: Clean functional approach
- ❌ **Stack overhead**: Function call costs
- ❌ **Stack overflow risk**: Deep recursion for many 9s
- ❌ **Less efficient**: Unnecessary function call overhead

### Solution 3: Explicit Carry Variable
```python
def plusOne(self, digits: List[int]) -> List[int]:
    carry = 1
    result = []
    
    for i in range(len(digits) - 1, -1, -1):
        total = digits[i] + carry
        result.append(total % 10)
        carry = total // 10
    
    if carry:
        result.append(carry)
    
    return result[::-1]
```

**Analysis:**
- ✅ **General purpose**: Works for adding any number
- ✅ **Clear carry logic**: Explicit carry handling
- ❌ **Extra space**: Creates new result array
- ❌ **Reverse operation**: Requires final array reversal
- ❌ **Overkill**: More complex than needed for +1 operation

## Why Our Solution is Optimal

### 1. **Optimal Time Complexity**
```python
# Best case: O(1) - immediate return for most cases
# Average case: O(1) - early termination dominates
# Worst case: O(n) - unavoidable for all-9s input
```

### 2. **Optimal Space Complexity**
```python
# In-place modification when possible
# Additional space only when mathematically necessary
```

### 3. **Early Termination Optimization**
```python
# 90% of cases resolve in first iteration
# Avoids unnecessary computation
```

### 4. **Clean Code Structure**
```python
# Single loop with clear logic paths
# No complex state management
# Readable and maintainable
```

## Key Algorithm Concepts Demonstrated

### 1. **Carry Propagation**
```python
# Mathematical concept: handling overflow in positional notation
# Implementation: convert 9s to 0s and continue
```

### 2. **Early Termination**
```python
# Optimization technique: exit as soon as result is determined
# Prevents unnecessary computation
```

### 3. **In-Place Modification**
```python
# Memory optimization: modify input array directly
# Reduces space complexity for common cases
```

### 4. **Edge Case Handling**
```python
# Comprehensive coverage: normal, partial carry, full carry
# Robust solution for all input patterns
```

## Real-World Applications

### 1. **Arbitrary Precision Arithmetic**
- **Cryptography**: Large number operations
- **Financial systems**: High-precision calculations
- **Scientific computing**: Extended precision requirements

### 2. **Digital Systems**
- **Processor design**: ALU increment operations
- **Counter circuits**: Digital counter implementation
- **Memory addressing**: Address increment operations

### 3. **Data Structures**
- **Big integer libraries**: Foundation for addition operations
- **Version numbering**: Increment version components
- **Sequence generation**: Numerical sequence operations

### 4. **Algorithm Building Blocks**
- **Addition algorithms**: Base for multi-digit addition
- **Increment operations**: General increment functionality
- **Overflow handling**: Template for carry propagation

## Best Practices Demonstrated

### 1. **Optimize for Common Cases**
```python
# 90% of additions don't require full array processing
# Early return optimization handles majority efficiently
```

### 2. **Handle Edge Cases Explicitly**
```python
# All-9s case requires special handling
# Clear separation of normal vs. overflow cases
```

### 3. **Use In-Place Operations When Safe**
```python
# Modify input array directly for memory efficiency
# Create new array only when necessary
```

### 4. **Write Self-Documenting Code**
```python
# Clear variable names and logical flow
# Comments explain the mathematical reasoning
```

### 5. **Design for Maintainability**
```python
# Simple loop structure
# Clear conditional logic
# Easy to understand and modify
```

This solution demonstrates excellent algorithm design by combining mathematical insight with practical optimization. The approach handles all edge cases efficiently while maintaining optimal time and space complexity for the vast majority of inputs.