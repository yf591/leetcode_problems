# 209. Minimum Size Subarray Sum - Solution Explanation

## Problem Overview
Find the **minimum length** of a **contiguous subarray** whose sum is greater than or equal to `target`.

**Input Example:**
```
target = 7, nums = [2,3,1,2,4,3,1]
```

**Output Example:**
```
2
```

**Explanation:** The subarray `[4,3]` has sum 7 and length 2 (minimum).

## Algorithm: Sliding Window Technique

**Core Idea:**
- Use **two pointers** (left, right) to manage a window
- **Expand right** to increase sum
- **Shrink left** to find minimum length
- Solve efficiently in **O(n) time**

## Step-by-Step Solution Breakdown

### Step 1: Initialization
```python
left = 0                    # Window start position
current_sum = 0             # Current window sum
min_length = float("inf")   # Minimum length (initially infinity)
```

### Step 2: Expand Window with Right Pointer
```python
for right in range(len(nums)):
    current_sum += nums[right]  # Add new element to window
```

**What happens:**
- Right pointer moves from left to right through array
- Each step adds a new element to the window
- Window size gradually expands

### Step 3: Shrink Window When Condition is Met
```python
while current_sum >= target:
    current_length = right - left + 1  # Current window length
    min_length = min(min_length, current_length)  # Update minimum
    
    current_sum -= nums[left]  # Remove leftmost element
    left += 1                  # Move left pointer right
```

## Why `current_length = right - left + 1`?

### Understanding Index vs Length Relationship

#### Basic Concept: Array indices start from 0
```python
nums = [2, 3, 1, 2, 4, 3, 1]
index  0  1  2  3  4  5  6
```

#### Concrete Examples
```python
# Example 1: left=1, right=3
nums = [2, 3, 1, 2, 4, 3, 1]
       [   ▼  ▼  ▼      ]  # Indices 1,2,3
           3  1  2         # Actual elements

# Indices: 1, 2, 3
# Element count: 3
# Calculation: right - left + 1 = 3 - 1 + 1 = 3 ✅

# If we used right - left:
# Calculation: 3 - 1 = 2 ❌ (Actually 3 elements, but gives 2)
```

#### More Detailed Examples
```python
# Example 2: left=0, right=0 (single element)
nums = [2, 3, 1, 2, 4, 3, 1]
       [▼            ]  # Only index 0
        2                # 1 element

# Length calculation:
# right - left + 1 = 0 - 0 + 1 = 1 ✅ (correct)
# right - left = 0 - 0 = 0 ❌ (wrong)

# Example 3: left=2, right=5
nums = [2, 3, 1, 2, 4, 3, 1]
       [     ▼  ▼  ▼  ▼   ]  # Indices 2,3,4,5
             1  2  4  3       # 4 elements

# Length calculation:
# right - left + 1 = 5 - 2 + 1 = 4 ✅ (correct)
# right - left = 5 - 2 = 3 ❌ (wrong)
```

### Mathematical Explanation
```
For array index range [left, right]:
- Start index: left
- End index: right
- Element count = (end - start) + 1

Why +1 is needed:
- Indices start from 0, but counting starts from 1
- Example: indices 3 to 5 → 3,4,5 = 3 elements
- 5 - 3 = 2, but actually 3 elements
- 5 - 3 + 1 = 3 ✅
```

## Complete Execution Example

### Input: `target = 7, nums = [2,3,1,2,4,3,1]`

#### Initial State
```python
left = 0, current_sum = 0, min_length = ∞
nums = [2, 3, 1, 2, 4, 3, 1]
        ↑
      left
```

#### Step 1: right = 0
```python
current_sum += nums[0] = 0 + 2 = 2
current_sum = 2 < target(7)  # Condition not met, skip while loop

nums = [2, 3, 1, 2, 4, 3, 1]
        ↑
    left/right
```

#### Step 2: right = 1
```python
current_sum += nums[1] = 2 + 3 = 5
current_sum = 5 < target(7)  # Condition not met

nums = [2, 3, 1, 2, 4, 3, 1]
        ↑  ↑
     left  right
```

#### Step 3: right = 2
```python
current_sum += nums[2] = 5 + 1 = 6
current_sum = 6 < target(7)  # Condition not met

nums = [2, 3, 1, 2, 4, 3, 1]
        ↑     ↑
     left     right
```

#### Step 4: right = 3
```python
current_sum += nums[3] = 6 + 2 = 8
current_sum = 8 >= target(7)  # Condition met! Execute while loop

while current_sum >= target:
    # 1st iteration of while
    current_length = right - left + 1 = 3 - 0 + 1 = 4
    min_length = min(∞, 4) = 4
    
    current_sum -= nums[left] = 8 - nums[0] = 8 - 2 = 6
    left += 1  # left = 1
    
    # current_sum = 6 < target(7), exit while loop

nums = [2, 3, 1, 2, 4, 3, 1]
           ↑     ↑
        left     right
```

#### Step 5: right = 4
```python
current_sum += nums[4] = 6 + 4 = 10
current_sum = 10 >= target(7)  # Condition met!

while current_sum >= target:
    # 1st iteration of while
    current_length = right - left + 1 = 4 - 1 + 1 = 4
    min_length = min(4, 4) = 4
    
    current_sum -= nums[left] = 10 - nums[1] = 10 - 3 = 7
    left += 1  # left = 2
    
    # current_sum = 7 >= target(7), continue while loop
    
    # 2nd iteration of while
    current_length = right - left + 1 = 4 - 2 + 1 = 3
    min_length = min(4, 3) = 3
    
    current_sum -= nums[left] = 7 - nums[2] = 7 - 1 = 6
    left += 1  # left = 3
    
    # current_sum = 6 < target(7), exit while loop

nums = [2, 3, 1, 2, 4, 3, 1]
              ↑     ↑
           left     right
```

#### Step 6: right = 5
```python
current_sum += nums[5] = 6 + 3 = 9
current_sum = 9 >= target(7)  # Condition met!

while current_sum >= target:
    # 1st iteration of while
    current_length = right - left + 1 = 5 - 3 + 1 = 3
    min_length = min(3, 3) = 3
    
    current_sum -= nums[left] = 9 - nums[3] = 9 - 2 = 7
    left += 1  # left = 4
    
    # current_sum = 7 >= target(7), continue while loop
    
    # 2nd iteration of while
    current_length = right - left + 1 = 5 - 4 + 1 = 2  ← ★Minimum found!
    min_length = min(3, 2) = 2
    
    current_sum -= nums[left] = 7 - nums[4] = 7 - 4 = 3
    left += 1  # left = 5
    
    # current_sum = 3 < target(7), exit while loop

nums = [2, 3, 1, 2, 4, 3, 1]
                    ↑  ↑
                 left  right
```

#### Final Step: right = 6
```python
current_sum += nums[6] = 3 + 1 = 4
current_sum = 4 < target(7)  # Condition not met

# Final result: min_length = 2
```

### Discovered Minimum Subarray
```python
# When left=4, right=5, length 2 was found
nums = [2, 3, 1, 2, 4, 3, 1]
                   [4, 3]  # Sum = 7, Length = 2
```

## Time & Space Complexity

### Time Complexity: O(n)
```python
# Each element is accessed at most twice:
# - Once by right pointer (addition)
# - Once by left pointer (removal)
# Total: 2n = O(n)
```

### Space Complexity: O(1)
```python
# Only uses fixed-size variables:
# left, right, current_sum, min_length
```

## Edge Cases Handling

### No Solution Exists
```python
target = 15, nums = [1,2,3,4]
# No subarray has sum ≥ 15
# min_length remains float("inf")
# return 0
```

### Single Element Solution
```python
target = 4, nums = [1,4,2]
# nums[1] = 4 >= target
# Subarray of length 1 is the solution
```

### Entire Array Needed
```python
target = 10, nums = [1,2,3,4]
# Sum of all elements = 10
# Subarray of length 4 is the solution
```

## Alternative Approaches Comparison

### Approach 1: Brute Force
```python
def minSubArrayLen_brute_force(target, nums):
    min_length = float("inf")
    
    for i in range(len(nums)):
        current_sum = 0
        for j in range(i, len(nums)):
            current_sum += nums[j]
            if current_sum >= target:
                min_length = min(min_length, j - i + 1)
                break
    
    return 0 if min_length == float("inf") else min_length

# Time Complexity: O(n²)
# Space Complexity: O(1)
```

### Approach 2: Prefix Sum + Binary Search
```python
def minSubArrayLen_binary_search(target, nums):
    # Create prefix sum array: O(n)
    prefix_sum = [0]
    for num in nums:
        prefix_sum.append(prefix_sum[-1] + num)
    
    min_length = float("inf")
    
    # Binary search for each starting position: O(n log n)
    for i in range(len(nums)):
        # Find minimum j where prefix_sum[j] - prefix_sum[i] >= target
        target_sum = target + prefix_sum[i]
        
        # Binary search for target_sum
        left, right = i + 1, len(prefix_sum)
        while left < right:
            mid = (left + right) // 2
            if prefix_sum[mid] >= target_sum:
                right = mid
            else:
                left = mid + 1
        
        if left < len(prefix_sum):
            min_length = min(min_length, left - i)
    
    return 0 if min_length == float("inf") else min_length

# Time Complexity: O(n log n)
# Space Complexity: O(n)
```

### Current Solution (Sliding Window) Advantages
```python
# ✅ Time Complexity: O(n) - Most efficient
# ✅ Space Complexity: O(1) - Memory efficient
# ✅ Implementation simplicity
# ✅ Intuitive and easy to understand
```

## Debugging Tips

### Track Window State
```python
def minSubArrayLen_debug(target, nums):
    left = 0
    current_sum = 0
    min_length = float("inf")
    
    for right in range(len(nums)):
        current_sum += nums[right]
        print(f"Add nums[{right}]={nums[right]}, sum={current_sum}, window={nums[left:right+1]}")
        
        while current_sum >= target:
            current_length = right - left + 1
            min_length = min(min_length, current_length)
            print(f"  Valid window: {nums[left:right+1]}, length={current_length}, min_so_far={min_length}")
            
            current_sum -= nums[left]
            left += 1
            print(f"  Shrink: remove nums[{left-1}], sum={current_sum}, new_window={nums[left:right+1] if left <= right else []}")
    
    return 0 if min_length == float("inf") else min_length
```

### Test Boundary Conditions
```python
# Test cases
test_cases = [
    (7, [2,3,1,2,4,3,1]),  # Normal case
    (4, [1,4,4]),          # Single element solution
    (11, [1,1,1,1,1,1,1]), # No solution
    (6, [10,2,3]),         # First element solves
    (1, [1]),              # Minimum array
    (1, []),               # Empty array
]

for target, nums in test_cases:
    result = minSubArrayLen(target, nums)
    print(f"target={target}, nums={nums} → result={result}")
```

## Real-World Applications

1. **Network Bandwidth Management**: Minimum time to transfer target data
2. **Inventory Management**: Minimum period to achieve sales target
3. **Investment Portfolio**: Minimum stocks needed for target return
4. **Game Development**: Shortest path to achieve target score
5. **Data Analysis**: Minimum sample size for statistical significance

This problem demonstrates the **Sliding Window** technique, which is a crucial pattern applicable to many array problems. The key insight is understanding how to efficiently maintain a dynamic window while tracking the optimal solution.

## Key Takeaways

1. **Sliding Window** is ideal for contiguous subarray problems
2. **Two-pointer technique** provides O(n) efficiency
3. **Index calculation** requires careful handling of off-by-one errors
4. **Window expansion and contraction** must be balanced
5. **Edge case handling** ensures robust solutions