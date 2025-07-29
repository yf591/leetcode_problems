# 69. Sqrt(x) - Solution Explanation

## Problem Overview
Given a non-negative integer `x`, return the square root of `x` rounded down to the nearest integer.

The returned integer should be **non-negative** as well.

You **must not use** any built-in exponent function or operator, such as `pow(x, 0.5)` or `x ** 0.5`.

**Examples:**
- `x = 4` → `2` (√4 = 2.0 → 2)
- `x = 8` → `2` (√8 = 2.828... → 2)
- `x = 1` → `1` (√1 = 1.0 → 1)
- `x = 0` → `0` (√0 = 0.0 → 0)

**Constraints:**
- 0 ≤ x ≤ 2³¹ - 1

## Understanding the Mathematical Problem

### Square Root Definition
The square root of a number `x` is a value `y` such that `y² = x`.

### Floor Operation Requirement
Since we need to **round down**, we're looking for:
```
floor(√x) = max{k ∈ ℤ | k² ≤ x}
```

**Translation**: Find the largest integer whose square doesn't exceed `x`.

### Examples of Floor Operation
```
√4 = 2.0 → floor(2.0) = 2
√8 = 2.828... → floor(2.828...) = 2
√15 = 3.872... → floor(3.872...) = 3
√16 = 4.0 → floor(4.0) = 4
```

### Key Insight: Monotonic Property
For any integers `a` and `b` where `a < b`:
- If `a² ≤ x`, then `a` is a candidate for the answer
- If `b² > x`, then `b` (and all larger values) are too large

This **monotonic property** makes binary search applicable.

## Solution Approach

Our solution uses **Binary Search** to efficiently find the largest integer whose square doesn't exceed `x`:

```python
def mySqrt(self, x: int) -> int:
    # Handle the edge case for x = 0.
    if x == 0:
        return 0

    # Set up the search range for binary search.
    low, high = 1, x
    result = 0

    while low <= high:
        # Calculate the middle of the current range.
        mid = low + (high - low) // 2

        # Check if mid*mid is the square root.
        # To avoid potential overflow with mid*mid, we can use division.
        # If mid == x / mid, but it's safer to just check if mid*mid <= x.
        if mid * mid <= x:
            # mid could be our answer (since we round down).
            # Store it and try to find a larger integer square root.
            result = mid
            low = mid + 1
        else:
            # mid is too large, so we search in the left half.
            high = mid - 1

    return result
```

**Strategy:**
1. **Edge case handling**: Special treatment for x = 0
2. **Search space setup**: Binary search from 1 to x
3. **Candidate tracking**: Store the best valid answer found so far
4. **Binary search**: Efficiently narrow down to the optimal answer

## Step-by-Step Breakdown

### Step 1: Handle Edge Case
```python
if x == 0:
    return 0
```

**Purpose**: Handle the special case where x = 0

**Why Separate Handling?**
```python
# Mathematical: √0 = 0
# Algorithm: Our binary search starts from low = 1
# Since 0 is not in the search range [1, x], we handle it explicitly
```

### Step 2: Initialize Search Range
```python
low, high = 1, x
result = 0
```

**Search Range Logic:**
```python
# For x ≥ 1, the mathematical bounds are: 1 ≤ √x ≤ x
# Examples:
# x = 1: 1 ≤ √1 = 1 ≤ 1
# x = 4: 1 ≤ √4 = 2 ≤ 4  
# x = 16: 1 ≤ √16 = 4 ≤ 16
# x = 100: 1 ≤ √100 = 10 ≤ 100
```

**Result Variable**: Tracks the largest valid candidate found so far

### Step 3: Binary Search Loop
```python
while low <= high:
    mid = low + (high - low) // 2
```

#### Overflow-Safe Midpoint Calculation

**Standard approach:**
```python
mid = (low + high) // 2
```

**Our approach:**
```python
mid = low + (high - low) // 2
```

**Why the difference?**
```python
# Prevents integer overflow in languages with fixed-size integers
# Example with 32-bit integers:
# low = 2^30, high = 2^30
# (low + high) = 2^31 → overflow!
# low + (high - low) // 2 = low + 0 = 2^30 → safe

# In Python: No integer overflow, but good programming practice
```

### Step 4: Square Comparison and Range Update
```python
if mid * mid <= x:
    result = mid
    low = mid + 1
else:
    high = mid - 1
```

#### Case 1: `mid * mid ≤ x` (Valid Candidate)
```python
result = mid      # Store as potential answer
low = mid + 1     # Search for potentially larger valid answer
```

**Logic:**
- `mid` is a valid candidate (its square doesn't exceed x)
- There might be a larger valid candidate, so search the right half
- Always store the candidate because it might be the final answer

#### Case 2: `mid * mid > x` (Too Large)
```python
high = mid - 1    # Search for smaller values
```

**Logic:**
- `mid` is too large (its square exceeds x)
- All values larger than `mid` are also too large
- Search the left half for valid candidates

## Detailed Execution Traces

### Example 1: x = 8 → 2 (√8 = 2.828...)
```python
Input: x = 8
Initial: low = 1, high = 8, result = 0

Iteration 1:
mid = 1 + (8-1)//2 = 1 + 3 = 4
Check: 4 * 4 = 16
16 ≤ 8? No (16 > 8)
Action: high = 4 - 1 = 3
State: low=1, high=3, result=0

Iteration 2:
mid = 1 + (3-1)//2 = 1 + 1 = 2
Check: 2 * 2 = 4  
4 ≤ 8? Yes
Action: result = 2, low = 2 + 1 = 3
State: low=3, high=3, result=2

Iteration 3:
mid = 3 + (3-3)//2 = 3 + 0 = 3
Check: 3 * 3 = 9
9 ≤ 8? No (9 > 8)
Action: high = 3 - 1 = 2
State: low=3, high=2, result=2

Loop condition: low ≤ high? → 3 ≤ 2? No
Exit loop, return result = 2 ✓

Verification: √8 = 2.828..., floor(2.828...) = 2 ✓
```

### Example 2: x = 4 → 2 (Perfect Square)
```python
Input: x = 4  
Initial: low = 1, high = 4, result = 0

Iteration 1:
mid = 1 + (4-1)//2 = 1 + 1 = 2
Check: 2 * 2 = 4
4 ≤ 4? Yes
Action: result = 2, low = 2 + 1 = 3
State: low=3, high=4, result=2

Iteration 2:
mid = 3 + (4-3)//2 = 3 + 0 = 3
Check: 3 * 3 = 9
9 ≤ 4? No (9 > 4)
Action: high = 3 - 1 = 2
State: low=3, high=2, result=2

Loop condition: low ≤ high? → 3 ≤ 2? No
Exit loop, return result = 2 ✓

Verification: √4 = 2.0, floor(2.0) = 2 ✓
```

### Example 3: x = 1 → 1 (Minimum Case)
```python
Input: x = 1
Initial: low = 1, high = 1, result = 0

Iteration 1:
mid = 1 + (1-1)//2 = 1 + 0 = 1
Check: 1 * 1 = 1
1 ≤ 1? Yes
Action: result = 1, low = 1 + 1 = 2
State: low=2, high=1, result=1

Loop condition: low ≤ high? → 2 ≤ 1? No
Exit loop, return result = 1 ✓

Verification: √1 = 1.0, floor(1.0) = 1 ✓
```

### Example 4: x = 15 → 3 (Non-Perfect Square)
```python
Input: x = 15
Initial: low = 1, high = 15, result = 0

Iteration 1:
mid = 1 + (15-1)//2 = 1 + 7 = 8
Check: 8 * 8 = 64
64 ≤ 15? No (64 > 15)
Action: high = 8 - 1 = 7
State: low=1, high=7, result=0

Iteration 2:
mid = 1 + (7-1)//2 = 1 + 3 = 4
Check: 4 * 4 = 16
16 ≤ 15? No (16 > 15)
Action: high = 4 - 1 = 3
State: low=1, high=3, result=0

Iteration 3:
mid = 1 + (3-1)//2 = 1 + 1 = 2
Check: 2 * 2 = 4
4 ≤ 15? Yes
Action: result = 2, low = 2 + 1 = 3
State: low=3, high=3, result=2

Iteration 4:
mid = 3 + (3-3)//2 = 3 + 0 = 3
Check: 3 * 3 = 9
9 ≤ 15? Yes
Action: result = 3, low = 3 + 1 = 4
State: low=4, high=3, result=3

Loop condition: low ≤ high? → 4 ≤ 3? No
Exit loop, return result = 3 ✓

Verification: √15 = 3.872..., floor(3.872...) = 3 ✓
```

## Algorithm Correctness Analysis

### Invariant Maintenance
Throughout the binary search, we maintain these invariants:

1. **Range Invariant**: `low ≤ target ≤ high` (where target is the answer)
2. **Result Invariant**: `result` contains the largest valid candidate found so far
3. **Monotonicity**: All values in `[low, high]` are potential candidates

### Termination Guarantee
```python
# Each iteration reduces the search space by at least half
# Search space: [low, high] with size (high - low + 1)
# After k iterations: size ≤ x / 2^k
# When size becomes 0: low > high, loop terminates
```

### Correctness Proof
```python
# At termination:
# 1. result contains the largest integer where result² ≤ x
# 2. (result + 1)² > x (if result + 1 was tested)
# 3. Therefore: result = floor(√x)
```

## Edge Cases and Robustness

### Edge Case 1: Perfect Squares
```python
# x = 1, 4, 9, 16, 25, 36, ...
# Algorithm correctly identifies exact square roots
x = 16 → result = 4 (since 4² = 16 ≤ 16)
x = 25 → result = 5 (since 5² = 25 ≤ 25)
```

### Edge Case 2: Non-Perfect Squares  
```python
# x = 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, ...
# Algorithm correctly floors the square root
x = 8 → result = 2 (since 2² = 4 ≤ 8 but 3² = 9 > 8)
x = 15 → result = 3 (since 3² = 9 ≤ 15 but 4² = 16 > 15)
```

### Edge Case 3: Boundary Values
```python
x = 0 → 0 (handled explicitly)
x = 1 → 1 (smallest positive case)
x = 2^31 - 1 → 46340 (largest constraint case)
```

### Edge Case 4: Large Numbers
```python
# For very large x, binary search remains efficient
x = 1000000 → 1000 (binary search takes ~20 iterations)
x = 2^31 - 1 → 46340 (binary search takes ~31 iterations)
```

## Alternative Solutions Comparison

### Solution 1: Linear Search (Brute Force)
```python
def mySqrt(self, x: int) -> int:
    if x == 0:
        return 0
    
    i = 1
    while i * i <= x:
        i += 1
    return i - 1
```

**Analysis:**
- ✅ **Simple to understand**: Straightforward incremental approach
- ✅ **Easy to implement**: No complex logic required
- ❌ **Poor time complexity**: O(√x) - very slow for large inputs
- ❌ **Impractical**: Takes 46,340 iterations for x = 2^31 - 1

### Solution 2: Newton's Method (Newton-Raphson)
```python
def mySqrt(self, x: int) -> int:
    if x == 0:
        return 0
    
    r = x
    while r * r > x:
        r = (r + x // r) // 2
    return r
```

**Analysis:**
- ✅ **Very fast convergence**: Quadratic convergence rate
- ✅ **Mathematically elegant**: Based on calculus and approximation theory
- ❌ **Complex to understand**: Requires knowledge of numerical methods
- ❌ **Implementation subtleties**: Integer arithmetic requires careful handling
- ✅ **Excellent performance**: Often faster than binary search in practice

### Solution 3: Built-in Functions (Not Allowed)
```python
import math

def mySqrt(self, x: int) -> int:
    return int(math.sqrt(x))
```

**Analysis:**
- ✅ **Extremely simple**: One-liner solution
- ✅ **Highly optimized**: Uses hardware-optimized implementations
- ❌ **Violates constraints**: Problem explicitly forbids built-in functions
- ❌ **No learning value**: Doesn't demonstrate algorithmic thinking

### Solution 4: Bit Manipulation Approach
```python
def mySqrt(self, x: int) -> int:
    if x == 0:
        return 0
    
    # Find the most significant bit
    msb = 0
    temp = x
    while temp:
        msb += 1
        temp >>= 1
    
    # Binary search using bit manipulation
    result = 0
    for i in range((msb + 1) // 2, -1, -1):
        candidate = result | (1 << i)
        if candidate * candidate <= x:
            result = candidate
    
    return result
```

**Analysis:**
- ✅ **Bit-level efficiency**: Works directly with binary representation
- ✅ **Good performance**: Similar to binary search
- ❌ **Complex logic**: Harder to understand and implement correctly
- ❌ **Error-prone**: Bit manipulation is easy to get wrong

## Why Our Binary Search Solution is Optimal

### 1. **Optimal Time Complexity: O(log x)**
```python
# Exponential reduction in search space
# For x = 2^31 - 1: maximum 31 iterations
# Much better than O(√x) linear search
```

### 2. **Minimal Space Complexity: O(1)**
```python
# Uses only a constant number of variables
# No recursion, no additional data structures
```

### 3. **Clear and Maintainable Code**
```python
# Easy to understand binary search template
# Well-commented and logically structured
# Standard algorithm that other programmers recognize
```

### 4. **Robust Error Handling**
```python
# Handles all edge cases correctly
# Overflow-safe midpoint calculation
# Explicit handling of x = 0
```

### 5. **Interview-Friendly**
```python
# Demonstrates understanding of:
# - Binary search principles
# - Edge case handling
# - Time/space complexity analysis
# - Clean code practices
```

## Performance Analysis

### Time Complexity: O(log x)
```python
# Binary search halves the search space each iteration
# Maximum iterations: ⌈log₂(x)⌉
# Examples:
# x = 1,000: ~10 iterations
# x = 1,000,000: ~20 iterations  
# x = 2^31 - 1: ~31 iterations
```

### Space Complexity: O(1)
```python
# Fixed number of variables: low, high, mid, result
# No additional memory allocation
# No recursion stack
```

### Practical Performance
```python
# Very fast for all practical inputs
# Constant factors are small
# Cache-friendly (no random memory access)
# Branch prediction friendly (simple conditional logic)
```

## Key Programming Concepts Demonstrated

### 1. **Binary Search Template**
```python
while low <= high:
    mid = low + (high - low) // 2
    if condition(mid):
        # Update result and search right
        result = mid
        low = mid + 1
    else:
        # Search left
        high = mid - 1
```

### 2. **Overflow Prevention**
```python
# Safe midpoint calculation
mid = low + (high - low) // 2  # vs. (low + high) // 2
```

### 3. **Candidate Tracking**
```python
# Store best answer found so far
# Essential for "find maximum/minimum satisfying condition" problems
```

### 4. **Mathematical Problem Transformation**
```python
# Transform: "find floor(√x)"
# Into: "find max k where k² ≤ x"
# Enables binary search application
```

## Real-World Applications

### 1. **Computer Graphics**
- **Distance calculations**: 2D/3D distance computations
- **Circle/sphere rendering**: Radius calculations for rendering
- **Collision detection**: Distance-based collision algorithms

### 2. **Scientific Computing**
- **Numerical analysis**: Root finding in mathematical software
- **Physics simulations**: Velocity and acceleration calculations
- **Engineering**: Structural analysis and fluid dynamics

### 3. **Algorithms and Data Structures**
- **Geometric algorithms**: Computational geometry problems
- **Search algorithms**: Distance-based search optimizations
- **Machine learning**: Euclidean distance in clustering algorithms

### 4. **Embedded Systems**
- **Sensor data processing**: Magnitude calculations from accelerometer data
- **Digital signal processing**: RMS (Root Mean Square) calculations
- **Control systems**: PID controller implementations

## Best Practices Demonstrated

### 1. **Handle Edge Cases First**
```python
if x == 0:
    return 0
# Explicit handling prevents bugs in main algorithm
```

### 2. **Use Proven Algorithm Templates**
```python
# Standard binary search pattern
# Well-understood and debugged approach
```

### 3. **Prevent Numerical Issues**
```python
# Overflow-safe midpoint calculation
# Careful integer arithmetic
```

### 4. **Track Best Solution**
```python
# Always maintain the best valid answer found
# Essential for optimization problems
```

### 5. **Write Self-Documenting Code**
```python
# Clear variable names: low, high, mid, result
# Comprehensive comments explaining logic
# Logical code structure
```

This solution demonstrates an optimal approach to computing integer square roots using binary search. The algorithm efficiently handles all edge cases while maintaining O(log x) time complexity and O(1) space complexity, making it both theoretically sound and practically efficient.