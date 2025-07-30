# 70. Climbing Stairs - Solution Explanation

## Problem Overview
You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can either climb **1 or 2 steps**. In how many distinct ways can you climb to the top?

**Examples:**
- `n = 1` → `1` way: `[1]`
- `n = 2` → `2` ways: `[1,1]` or `[2]`
- `n = 3` → `3` ways: `[1,1,1]`, `[1,2]`, `[2,1]`
- `n = 4` → `5` ways: `[1,1,1,1]`, `[1,1,2]`, `[1,2,1]`, `[2,1,1]`, `[2,2]`

**Constraints:**
- 1 ≤ n ≤ 45

## Understanding the Pattern

### Pattern Recognition
Let's examine the sequence of results:
```
f(1) = 1
f(2) = 2  
f(3) = 3
f(4) = 5
f(5) = 8
f(6) = 13
...
```

**Key Discovery**: This is the **Fibonacci sequence**!

### Why Fibonacci?

#### Mathematical Insight
To reach step `n`, you can only arrive from:
1. **Step (n-1)** by taking 1 step → `f(n-1)` ways
2. **Step (n-2)** by taking 2 steps → `f(n-2)` ways

Since these are mutually exclusive and collectively exhaustive:
```
f(n) = f(n-1) + f(n-2)
```

#### Proof by Induction

**Base Cases:**
- `f(1) = 1` ✓ (only one way: take 1 step)
- `f(2) = 2` ✓ (two ways: [1,1] or [2])

**Inductive Step:**
- Assume `f(k) = f(k-1) + f(k-2)` holds for all `k < n`
- For step `n`: must arrive from step `(n-1)` or step `(n-2)`
- By inductive hypothesis: `f(n) = f(n-1) + f(n-2)` ✓

#### Visual Proof for n = 4
```
Ways to reach step 4:

From step 3 (take 1 step):
- [1,1,1] + [1] = [1,1,1,1]
- [1,2] + [1] = [1,2,1]  
- [2,1] + [1] = [2,1,1]
Total: 3 ways (= f(3))

From step 2 (take 2 steps):
- [1,1] + [2] = [1,1,2]
- [2] + [2] = [2,2]
Total: 2 ways (= f(2))

Total for f(4) = f(3) + f(2) = 3 + 2 = 5 ✓
```

## Solution Approach

Our solution uses **space-optimized dynamic programming** by recognizing the Fibonacci pattern:

```python
def climbStairs(self, n: int) -> int:
    if n <= 2:
        return n

    # This is a Fibonacci sequence. We only need the previous two values
    # to calculate the next one.
    # 'one_step_before' stores the ways to get to step (i-1).
    # 'two_steps_before' stores the ways to get to step (i-2).
    two_steps_before = 1  # Way to climb 1 step
    one_step_before = 2  # Way to climb 2 steps

    # Iterate from the 3rd step up to the n-th step.
    for i in range(3, n + 1):
        # The number of way to reach the current step is the sum of the ways
        # to reach the previous two steps.
        current_ways = one_step_before + two_steps_before

        # Update our pointers for the next iteration.
        two_steps_before = one_step_before
        one_step_before = current_ways

    # After the loop, 'one_step_before' holds the total ways for n steps.
    return one_step_before
```

**Strategy:**
1. **Handle base cases**: Direct return for n ≤ 2
2. **Initialize variables**: Track only the last two Fibonacci values
3. **Iterative calculation**: Build up the solution step by step
4. **Space optimization**: Use O(1) space instead of O(n) array

## Step-by-Step Breakdown

### Step 1: Base Case Handling
```python
if n <= 2:
    return n
```

**Purpose**: Handle trivial cases directly

**Logic:**
```python
# n = 1: Only one way [1]
# n = 2: Two ways [1,1] and [2]
# These match the direct value of n
```

### Step 2: Variable Initialization (Space Optimization)
```python
two_steps_before = 1  # Way to climb 1 step (f(1))
one_step_before = 2   # Way to climb 2 steps (f(2))
```

#### Standard vs. Optimized Approach

**Standard Fibonacci (O(n) space):**
```python
dp = [0] * (n + 1)
dp[1], dp[2] = 1, 2
for i in range(3, n + 1):
    dp[i] = dp[i-1] + dp[i-2]
return dp[n]
```

**Our Optimized Approach (O(1) space):**
```python
# Only track the two most recent values
# two_steps_before = f(i-2)
# one_step_before = f(i-1)
# current_ways = f(i) = f(i-1) + f(i-2)
```

### Step 3: Iterative Calculation
```python
for i in range(3, n + 1):
    current_ways = one_step_before + two_steps_before
    
    # Update our pointers for the next iteration.
    two_steps_before = one_step_before
    one_step_before = current_ways
```

#### Variable Update Mechanism

**Before each iteration:**
```python
two_steps_before = f(i-2)  # Ways to reach step (i-2)
one_step_before = f(i-1)   # Ways to reach step (i-1)
```

**Calculation:**
```python
current_ways = f(i-1) + f(i-2) = f(i)  # Ways to reach step i
```

**After update:**
```python
two_steps_before = f(i-1)  # Former one_step_before
one_step_before = f(i)     # New current_ways
```

This creates a "sliding window" effect moving through the Fibonacci sequence.

## Detailed Execution Trace

### Example: n = 5

#### Initial Setup
```python
n = 5
two_steps_before = 1  # f(1) = 1
one_step_before = 2   # f(2) = 2
```

#### Iteration 1: i = 3
```python
current_ways = 2 + 1 = 3  # f(3) = f(2) + f(1) = 3

# Update variables:
two_steps_before = 2  # f(2)
one_step_before = 3   # f(3)

# State: tracking f(2)=2, f(3)=3
```

#### Iteration 2: i = 4
```python
current_ways = 3 + 2 = 5  # f(4) = f(3) + f(2) = 5

# Update variables:
two_steps_before = 3  # f(3)
one_step_before = 5   # f(4)

# State: tracking f(3)=3, f(4)=5
```

#### Iteration 3: i = 5
```python
current_ways = 5 + 3 = 8  # f(5) = f(4) + f(3) = 8

# Update variables:
two_steps_before = 5  # f(4)
one_step_before = 8   # f(5)

# State: tracking f(4)=5, f(5)=8
```

#### Final Result
```python
return one_step_before = 8  # f(5) = 8 ways
```

### Verification: All 8 ways for n = 5
```python
1. [1,1,1,1,1]  # 5 steps of size 1
2. [1,1,1,2]    # 3 steps of size 1, 1 step of size 2
3. [1,1,2,1]    # Different ordering
4. [1,2,1,1]    # Different ordering  
5. [2,1,1,1]    # Different ordering
6. [1,2,2]      # 1 step of size 1, 2 steps of size 2
7. [2,1,2]      # Different ordering
8. [2,2,1]      # Different ordering
```

## Why Return `one_step_before` Instead of `current_ways`?

### Common Question: Both Values Are the Same at Loop End!

A frequent point of confusion is why we return `one_step_before` instead of `current_ways`, since both contain the same value after the loop completes.

#### Analyzing Loop Termination State

Let's examine what happens in the **final iteration** (when `i = n`):

```python
# Last iteration: i = n
current_ways = one_step_before + two_steps_before  # Calculates f(n)

# Variable updates:
two_steps_before = one_step_before  # Now holds f(n-1)
one_step_before = current_ways     # Now holds f(n) ← Our answer!

# After loop ends:
current_ways = f(n)      # Contains the answer
one_step_before = f(n)   # Also contains the answer (due to update)
```

#### Both Return Statements Work Correctly

```python
return current_ways     # ✅ Correct - last calculated f(n)
return one_step_before  # ✅ Correct - updated to f(n) after calculation
```

#### Why Choose `one_step_before`?

**1. Semantic Consistency**
```python
# Throughout the entire loop:
# one_step_before represents "the answer for the current step number"
# When i=3: one_step_before = f(3)
# When i=4: one_step_before = f(4)  
# When i=n: one_step_before = f(n) ← The final answer
```

**2. Variable Role Clarity**
```python
# current_ways: "temporary calculation in progress"
# one_step_before: "confirmed result ready for next iteration"
# More natural to return the "confirmed result" variable
```

**3. Algorithm Pattern Standard**
```python
# In space-optimized Fibonacci implementations:
# The "previous value" variable typically holds the final result
# This matches established coding patterns and educational materials
```

**4. Code Maintainability**
```python
# If you modify the loop structure, one_step_before will still be correct
# current_ways might become undefined outside the loop in some refactoring scenarios
```

#### Practical Verification

```python
def test_both_approaches():
    def version_current_ways(n):
        if n <= 2: return n
        two_steps_before, one_step_before = 1, 2
        for i in range(3, n + 1):
            current_ways = one_step_before + two_steps_before
            two_steps_before = one_step_before
            one_step_before = current_ways
        return current_ways  # This version
    
    def version_one_step_before(n):
        if n <= 2: return n
        two_steps_before, one_step_before = 1, 2
        for i in range(3, n + 1):
            current_ways = one_step_before + two_steps_before
            two_steps_before = one_step_before
            one_step_before = current_ways
        return one_step_before  # This version
    
    # Test both approaches
    for n in range(1, 10):
        v1 = version_current_ways(n)
        v2 = version_one_step_before(n)
        print(f"n={n}: current_ways={v1}, one_step_before={v2}, equal={v1==v2}")

# Output: All pairs are equal, confirming both approaches work
```

**Key Takeaway**: While both return statements produce correct results, `return one_step_before` is preferred for its semantic clarity, consistency with established patterns, and better maintainability. The choice demonstrates thoughtful algorithm design beyond just functional correctness.

## Alternative Solutions Comparison

### Solution 1: Naive Recursion
```python
def climbStairs(self, n: int) -> int:
    if n <= 2:
        return n
    return self.climbStairs(n-1) + self.climbStairs(n-2)
```

**Analysis:**
- ✅ **Intuitive**: Direct translation of mathematical recurrence
- ✅ **Simple**: Easy to understand and implement
- ❌ **Exponential time**: O(2^n) due to repeated subproblems
- ❌ **Stack overflow**: Deep recursion for large n

**Performance comparison:**
```python
# For n = 40:
# Naive recursion: ~1 second
# Our solution: < 1 millisecond
```

### Solution 2: Memoized Recursion (Top-Down DP)
```python
def climbStairs(self, n: int) -> int:
    memo = {}
    
    def helper(n):
        if n in memo:
            return memo[n]
        if n <= 2:
            return n
        
        memo[n] = helper(n-1) + helper(n-2)
        return memo[n]
    
    return helper(n)
```

**Analysis:**
- ✅ **Efficient**: O(n) time complexity
- ✅ **Intuitive**: Maintains recursive structure
- ❌ **Extra space**: O(n) for memoization table
- ❌ **Function call overhead**: Recursion stack usage

### Solution 3: Array-Based DP (Bottom-Up)
```python
def climbStairs(self, n: int) -> int:
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
```

**Analysis:**
- ✅ **Clear logic**: Easy to visualize DP table
- ✅ **Efficient**: O(n) time complexity
- ❌ **Extra space**: O(n) for DP array
- ❌ **Unnecessary storage**: Only need last two values

### Solution 4: Mathematical Formula (Golden Ratio)
```python
import math

def climbStairs(self, n: int) -> int:
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    psi = (1 - sqrt5) / 2
    
    return int((phi**(n+1) - psi**(n+1)) / sqrt5)
```

**Analysis:**
- ✅ **Theoretical elegance**: O(1) time complexity
- ✅ **Mathematical beauty**: Closed-form solution
- ❌ **Floating-point errors**: Precision issues for large n
- ❌ **Complex implementation**: Hard to understand and debug

## Why Our Solution is Optimal

### 1. **Optimal Time Complexity: O(n)**
```python
# Linear iteration from 3 to n
# Each iteration performs constant-time operations
# Cannot be improved since we need to compute all intermediate values
```

### 2. **Optimal Space Complexity: O(1)**
```python
# Uses only 3 variables regardless of input size
# Significant improvement over O(n) array solutions
# Matches the theoretical lower bound for this problem
```

### 3. **Numerical Stability**
```python
# Integer arithmetic only (no floating-point errors)
# No risk of precision loss for large n
# Handles all values within problem constraints perfectly
```

### 4. **Code Clarity and Maintainability**
```python
# Self-documenting variable names
# Clear comments explaining the logic
# Straightforward control flow
# Easy to understand and modify
```

### 5. **Interview-Friendly**
```python
# Demonstrates understanding of:
# - Dynamic programming principles
# - Space optimization techniques  
# - Pattern recognition skills
# - Clean coding practices
```

## Performance Analysis

### Time Complexity: O(n)
```python
# Single loop from 3 to n: (n-2) iterations
# Each iteration: constant time operations
# Total: O(n) time
```

### Space Complexity: O(1)
```python
# Fixed number of variables: two_steps_before, one_step_before, current_ways
# Space usage independent of input size
# Total: O(1) space
```

### Practical Performance
```python
# For n = 45 (constraint maximum):
# Execution time: < 1ms
# Memory usage: Few bytes
# Highly efficient for all practical purposes
```

## Dynamic Programming Insights

### Optimal Substructure
```python
# Problem: Find ways to climb n stairs
# Subproblems: Find ways to climb k stairs (k < n)
# Optimal solution for n can be constructed from optimal solutions for (n-1) and (n-2)
```

### Overlapping Subproblems
```python
# Computing f(5) requires f(4) and f(3)
# Computing f(4) requires f(3) and f(2)
# f(3) is computed multiple times → opportunity for optimization
```

### Bottom-Up vs. Top-Down
```python
# Bottom-up (our approach): Start from base cases, build up to solution
# Top-down: Start from problem, break down into subproblems
# Bottom-up often more space-efficient due to iterative nature
```

### Space Optimization Evolution
```python
# Stage 1: Naive recursion → O(2^n) time, O(n) stack space
# Stage 2: Memoization → O(n) time, O(n) memo space
# Stage 3: Array DP → O(n) time, O(n) array space
# Stage 4: Optimized DP → O(n) time, O(1) space (our solution)
```

## Real-World Applications

### Combinatorics Problems
```python
# Path counting in grids
# Sequence enumeration problems  
# Coding theory applications
```

### Algorithm Design Patterns
```python
# Template for space-optimized DP
# Fibonacci-like sequence computations
# Sliding window optimization techniques
```

### Interview Problem Categories
```python
# Classic DP introduction problem
# Space optimization demonstration
# Pattern recognition assessment
```

## Edge Cases and Robustness

### Edge Case 1: Minimum Input (n = 1)
```python
if n <= 2: return n  # Returns 1
# Only one way: [1]
# Handled correctly by base case
```

### Edge Case 2: Second Minimum (n = 2)
```python
if n <= 2: return n  # Returns 2  
# Two ways: [1,1] and [2]
# Handled correctly by base case
```

### Edge Case 3: Large Input (n = 45)
```python
# Result: 1,836,311,903 (fits in 32-bit integer)
# Algorithm handles efficiently without overflow
# Python's arbitrary precision integers eliminate overflow concerns
```

### Edge Case 4: Boundary Transition (n = 3)
```python
# First case that enters the loop
# Correctly computes f(3) = f(2) + f(1) = 2 + 1 = 3
# Verifies the transition from base case to iteration
```

## Mathematical Properties

### Fibonacci Sequence Properties
```python
# Growth rate: φ^n where φ = (1 + √5)/2 ≈ 1.618 (golden ratio)
# Ratio convergence: lim(n→∞) f(n+1)/f(n) = φ
# Binet's formula: f(n) = (φ^n - ψ^n)/√5 where ψ = (1-√5)/2
```

### Asymptotic Behavior
```python
# f(n) grows exponentially with base φ ≈ 1.618
# For large n: f(n) ≈ φ^n/√5
# This explains why the problem has constraint n ≤ 45 (manageable growth)
```

## Best Practices Demonstrated

### 1. **Pattern Recognition**
```python
# Identify underlying mathematical structure (Fibonacci)
# Transform problem into known algorithmic pattern
```

### 2. **Space Optimization**
```python
# Recognize that only recent values are needed
# Replace array storage with sliding variables
```

### 3. **Clear Variable Naming**
```python
# two_steps_before, one_step_before: self-explanatory
# current_ways: describes what's being computed
```

### 4. **Comprehensive Comments**
```python
# Explain the mathematical insight (Fibonacci connection)
# Document variable purposes and update logic
# Provide context for optimization decisions
```

### 5. **Efficient Base Case Handling**
```python
# Handle trivial cases early
# Avoid unnecessary computation for small inputs
```

This solution exemplifies the progression from recognizing a mathematical pattern to implementing an optimally efficient algorithm. It demonstrates how dynamic programming can be refined through space optimization while maintaining clarity and correctness. The approach showcases both algorithmic sophistication and practical engineering skills essential for competitive programming and technical interviews.