# 1. Two Sum - Solution Explanation

## Problem Overview
Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

You may assume that each input would have **exactly one solution**, and you may not use the same element twice.

You can return the answer in any order.

**Examples:**
- `nums = [2,7,11,15]`, `target = 9` → `[0,1]` (nums[0] + nums[1] = 2 + 7 = 9)
- `nums = [3,2,4]`, `target = 6` → `[1,2]` (nums[1] + nums[2] = 2 + 4 = 6)
- `nums = [3,3]`, `target = 6` → `[0,1]` (nums[0] + nums[1] = 3 + 3 = 6)

**Constraints:**
- 2 ≤ nums.length ≤ 10⁴
- -10⁹ ≤ nums[i] ≤ 10⁹
- -10⁹ ≤ target ≤ 10⁹
- Only one valid answer exists

## Understanding the Problem

### What We're Looking For
We need to find **two different indices** `i` and `j` such that:
- `nums[i] + nums[j] = target`
- `i ≠ j` (cannot use same element twice)
- Return `[i, j]` (the indices, not the values)

### Key Insight: Complement Strategy
For any number `x` in the array, we need to find its **complement** `target - x`.

```
If target = 9 and current number = 2
Then complement = 9 - 2 = 7
We need to find if 7 exists in the array
```

## Algorithm: Hash Map (One-Pass)

The most efficient solution uses a **Hash Map** to store numbers we've seen and their indices, allowing O(1) lookup time for complements.

**Core Strategy:**
1. Iterate through array once
2. For each number, calculate its complement
3. Check if complement exists in our hash map
4. If yes: return indices, if no: store current number and continue

## Step-by-Step Algorithm Breakdown

### Step 1: Initialize Hash Map
```python
num_map = {}
```
**Purpose**: Store `{number: index}` pairs for O(1) complement lookup
**Structure**: `{value: index}` - maps each number to its position

### Step 2: Iterate Through Array
```python
for index, num in enumerate(nums):
```
**`enumerate()`**: Provides both index and value simultaneously
**Example**: `[2, 7, 11]` → `(0, 2), (1, 7), (2, 11)`

### Step 3: Calculate Complement
```python
complement = target - num
```
**Logic**: If `num + complement = target`, then `complement = target - num`
**Example**: `target=9, num=2` → `complement=7`

### Step 4: Check if Complement Exists
```python
if complement in num_map:
    return [num_map[complement], index]
```
**Hash Map Lookup**: O(1) average time complexity
**Return**: `[previous_index, current_index]` in order of discovery

### Step 5: Store Current Number
```python
num_map[num] = index
```
**Purpose**: Save current number for future complement searches
**Important**: Store AFTER checking to avoid using same element twice

### Step 6: Handle No Solution (Theoretical)
```python
return []
```
**Note**: Problem guarantees exactly one solution exists, so this never executes

## Detailed Example Walkthrough

**Input:** `nums = [2, 7, 11, 15]`, `target = 9`

### Initial State
```
nums: [2, 7, 11, 15]
target: 9
num_map: {}
```

### Iteration 1: index=0, num=2
```
complement = 9 - 2 = 7
num_map = {} (empty)
7 not in num_map → continue
num_map[2] = 0

State: num_map = {2: 0}
```

### Iteration 2: index=1, num=7
```
complement = 9 - 7 = 2
num_map = {2: 0}
2 in num_map? YES! → found solution
return [num_map[2], 1] = [0, 1]

Result: [0, 1] ✓
```

**Verification**: `nums[0] + nums[1] = 2 + 7 = 9 = target` ✓

## More Complex Example

**Input:** `nums = [3, 2, 4]`, `target = 6`

### Iteration-by-Iteration Trace

| Iteration | index | num | complement | num_map before | complement found? | Action |
|-----------|-------|-----|------------|----------------|------------------|---------|
| 1 | 0 | 3 | 6-3=3 | `{}` | No | Store: `{3: 0}` |
| 2 | 1 | 2 | 6-2=4 | `{3: 0}` | No | Store: `{3: 0, 2: 1}` |
| 3 | 2 | 4 | 6-4=2 | `{3: 0, 2: 1}` | **Yes!** | Return `[1, 2]` |

**Result**: `[1, 2]` → `nums[1] + nums[2] = 2 + 4 = 6` ✓

## Edge Case: Duplicate Numbers

**Input:** `nums = [3, 3]`, `target = 6`

### Why This Works
```
Iteration 1: index=0, num=3
complement = 6 - 3 = 3
num_map = {} → 3 not found
Store: num_map = {3: 0}

Iteration 2: index=1, num=3  
complement = 6 - 3 = 3
num_map = {3: 0} → 3 found!
Return: [0, 1]
```

**Key Point**: We check for complement BEFORE storing current number, so we don't accidentally use the same index twice.

## Alternative Approaches Comparison

### Approach 1: Brute Force (Nested Loops)
```python
def twoSum(self, nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

**Analysis:**
- ✅ **Simple to understand**
- ✅ **No extra space needed**
- ❌ **Time: O(n²)** - checks all pairs
- ❌ **Inefficient for large arrays**

### Approach 2: Sort + Two Pointers
```python
def twoSum(self, nums, target):
    # Create list of (value, original_index) pairs
    indexed_nums = [(nums[i], i) for i in range(len(nums))]
    indexed_nums.sort()  # Sort by value
    
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = indexed_nums[left][0] + indexed_nums[right][0]
        if current_sum == target:
            return [indexed_nums[left][1], indexed_nums[right][1]]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []
```

**Analysis:**
- ✅ **Time: O(n log n)** - dominated by sorting
- ❌ **Space: O(n)** - for indexed pairs
- ❌ **More complex implementation**
- ❌ **Slower than hash map approach**

### Approach 3: Hash Map (Two-Pass)
```python
def twoSum(self, nums, target):
    # First pass: build hash map
    num_map = {}
    for i, num in enumerate(nums):
        num_map[num] = i
    
    # Second pass: find complements
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map and num_map[complement] != i:
            return [i, num_map[complement]]
    return []
```

**Analysis:**
- ✅ **Time: O(n)** - two linear passes
- ✅ **Space: O(n)** - hash map storage
- ❌ **Two passes instead of one**
- ❌ **Need extra check `num_map[complement] != i`**

## Current Solution Advantages

### Approach 4: Hash Map (One-Pass) - Our Solution
```python
def twoSum(self, nums, target):
    num_map = {}
    for index, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], index]
        num_map[num] = index
    return []
```

**Analysis:**
- ✅ **Time: O(n)** - single pass through array
- ✅ **Space: O(n)** - hash map storage  
- ✅ **Optimal for this problem**
- ✅ **Early termination** - stops as soon as solution found
- ✅ **Clean implementation**

## Time & Space Complexity Analysis

### Current Solution (Hash Map One-Pass)
- **Time Complexity**: **O(n)** where n = length of array
  - Single pass through the array
  - Hash map operations (lookup, insert) are O(1) average
  - Early termination when solution found

- **Space Complexity**: **O(n)** in worst case
  - Hash map stores at most n-1 elements
  - **Best case**: O(1) if solution found immediately
  - **Average case**: O(n/2) if solution found in middle
  - **Worst case**: O(n-1) if solution is last pair

### Complexity Comparison Table
| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| **Hash Map (1-pass)** | **O(n)** | **O(n)** | **Optimal** |
| Hash Map (2-pass) | O(n) | O(n) | Less efficient |
| Sort + Two Pointers | O(n log n) | O(n) | Slower due to sorting |
| Brute Force | O(n²) | O(1) | Too slow for large inputs |

## Hash Map Deep Dive

### Why Hash Maps Work Here
1. **Fast Lookup**: O(1) average time to check if complement exists
2. **Dynamic Storage**: Can store elements as we encounter them
3. **Index Preservation**: Maps values to their original positions

### Hash Map Operations
```python
# Store operation: O(1)
num_map[num] = index

# Lookup operation: O(1) average
if complement in num_map:
    # Found!
```

### Memory Layout Example
```python
nums = [2, 7, 11, 15], target = 9

After processing index 0:
num_map = {2: 0}

Memory visualization:
┌─────┬───────┐
│ Key │ Value │
├─────┼───────┤
│  2  │   0   │
└─────┴───────┘
```

## Edge Cases and Special Scenarios

### Case 1: Solution at Beginning
```python
nums = [2, 7, 11, 15], target = 9
# Found at indices [0, 1] - very early termination
```

### Case 2: Solution at End
```python
nums = [11, 15, 2, 7], target = 9  
# Found at indices [2, 3] - late termination
```

### Case 3: Duplicate Values (Different Indices)
```python
nums = [3, 3], target = 6
# Both values same, but different indices [0, 1]
```

### Case 4: Negative Numbers
```python
nums = [-1, -2, -3, -4, -5], target = -8
# complement of -3 is -8 - (-3) = -5
# Found: indices of -3 and -5
```

### Case 5: Zero Values
```python
nums = [0, 4, 3, 0], target = 0
# complement of 0 is 0 - 0 = 0
# Found: indices [0, 3]
```

## Common Pitfalls and Tips

### 1. Using Same Element Twice
```python
# ❌ Wrong: Checking complement before storing prevents this
num_map[num] = index  # Store first
if complement in num_map:  # Then check
    return [num_map[complement], index]  # Might return [i, i]

# ✅ Correct: Check first, then store
if complement in num_map:  # Check first
    return [num_map[complement], index]
num_map[num] = index  # Store after
```

### 2. Wrong Return Format
```python
# ❌ Wrong: Returning values instead of indices
return [complement, num]

# ✅ Correct: Return indices
return [num_map[complement], index]
```

### 3. Index Order Confusion
```python
# Both are acceptable since problem allows any order:
return [num_map[complement], index]  # Earlier index first
return [index, num_map[complement]]  # Current index first
```

### 4. Forgetting Edge Cases
```python
# ❌ Incomplete: Not handling guaranteed solution
def twoSum(self, nums, target):
    # ... algorithm ...
    # Missing return statement

# ✅ Complete: Include theoretical no-solution case
def twoSum(self, nums, target):
    # ... algorithm ...
    return []  # Though this never executes
```

## Key Programming Concepts Demonstrated

1. **Hash Map Usage**: Efficient key-value storage and O(1) lookup
2. **Complement Strategy**: Mathematical relationship exploitation
3. **Single-Pass Algorithm**: Processing data in one iteration
4. **Early Termination**: Stopping as soon as solution found
5. **Index Tracking**: Maintaining original positions during processing
6. **Space-Time Tradeoff**: Using extra space for better time complexity

## Practice Tips

1. **Understand the complement concept**: If you need sum=9 and have 2, look for 7
2. **Trace through examples**: Follow hash map state changes step by step
3. **Consider edge cases**: Duplicates, negatives, zeros
4. **Remember the order**: Check complement first, then store current number
5. **Test with different inputs**: Early solution, late solution, edge cases

## Real-World Applications

1. **Pair Matching Problems**: Finding complementary items in datasets
2. **Financial Analysis**: Finding transactions that sum to specific amounts
3. **Data Analytics**: Identifying related data points with target relationships
4. **Optimization Problems**: Quick lookup for constraint satisfaction
5. **Caching Strategies**: Using hash maps for fast data retrieval

## Why This Solution is Optimal

1. **Minimal Time Complexity**: O(n) is the theoretical minimum
2. **Practical Efficiency**: Hash map operations are very fast in practice  
3. **Early Termination**: Stops immediately when solution found
4. **Clean Code**: Simple, readable, and maintainable
5. **Handles All Cases**: Works with duplicates, negatives, and all edge cases

This algorithm demonstrates the power of hash maps for transforming O(n²) problems into O(n) solutions through strategic caching and complement-based thinking.