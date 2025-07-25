# 27. Remove Element - Solution Explanation

## Problem Overview
Given an integer array `nums` and an integer `val`, remove all occurrences of `val` in `nums` **in-place**. The order of the elements may be changed. Then return the number of elements in `nums` which are not equal to `val`.

Consider the number of elements in `nums` which are not equal to `val` be `k`, to get accepted, you need to do the following things:
- Change the array `nums` such that the first `k` elements of `nums` contain the elements which are not equal to `val`
- The remaining elements of `nums` are not important as well as the size of `nums`
- Return `k`

**Examples:**
- `nums = [3,2,2,3]`, `val = 3` → `nums = [2,2,_,_]`, return `2`
- `nums = [0,1,2,2,3,0,4,2]`, `val = 2` → `nums = [0,1,4,0,3,_,_,_]`, return `5`

**Constraints:**
- 0 ≤ nums.length ≤ 100
- 0 ≤ nums[i] ≤ 50
- 0 ≤ val ≤ 100

## Understanding the Problem

### What "In-Place" Modification Means
**In-place** modification means we cannot create a new array. We must rearrange the existing array so that:
- First `k` positions contain elements that are NOT equal to `val`
- Remaining positions can contain anything (marked as `_`)
- The relative order of kept elements may change

**Example:**
```
Original: [3, 2, 2, 3]  val = 3
Result:   [2, 2, _, _]  ← Return k=2
          ↑―――↑  ↑―――↑
        Valid elements  Ignored
```

### Key Difference from Array Deletion
We're not actually "deleting" elements in the traditional sense. Instead, we're:
1. **Collecting** elements we want to keep
2. **Placing** them at the beginning of the array
3. **Ignoring** what comes after

## Algorithm: Two Pointers Technique

The core idea uses **Two Pointers**:
- **`i` (Read pointer)**: Scans through the array sequentially
- **`k` (Write pointer)**: Points to where the next valid element should be placed

**Key Insight**: We can safely overwrite elements because the write pointer `k` never gets ahead of the read pointer `i`.

## Step-by-Step Algorithm Breakdown

### Step 1: Initialize Write Pointer
```python
k = 0
```
**Purpose**: 
- Points to the position where the next valid element should be placed
- Also serves as a counter of valid elements found so far
- Start from index 0 (beginning of array)

### Step 2: Scan Through Entire Array
```python
for i in range(len(nums)):
```
**Purpose**: Examine every element in the array
**`i`**: Current position being examined (read pointer)

### Step 3: Check if Element Should be Kept
```python
if nums[i] != val:
```
**Condition**: Current element is NOT the value we want to remove
**Meaning**: This element should be kept in the result

### Step 4: Place Valid Element and Advance Pointer
```python
nums[k] = nums[i]
k += 1
```
**Actions:**
1. Copy the valid element to position `k`
2. Increment `k` to point to next available position

**Safety**: Since `i >= k` always holds, we never overwrite unprocessed data

### Step 5: Return Count of Valid Elements
```python
return k
```
**Result**: `k` represents both the count and the end boundary of valid elements

## Detailed Example Walkthrough

**Input:** `nums = [3, 2, 2, 3]`, `val = 3`

### Initial State
```
nums: [3, 2, 2, 3]
       ↑           
    k=0, i=0 (starting position)
```

### i=0: nums[0]=3
```
nums[0] = 3, val = 3
3 == 3 (target value) → Skip, no action

nums: [3, 2, 2, 3]
       ↑  ↑        
       k=0, i=0→1
```

### i=1: nums[1]=2
```
nums[1] = 2, val = 3  
2 != 3 (valid element) → Keep it
nums[k] = nums[i] → nums[0] = 2
k++ → k=1

nums: [2, 2, 2, 3]
          ↑  ↑     
          k=1, i=1→2
```

### i=2: nums[2]=2
```
nums[2] = 2, val = 3
2 != 3 (valid element) → Keep it
nums[k] = nums[i] → nums[1] = 2  
k++ → k=2

nums: [2, 2, 2, 3]
             ↑  ↑  
             k=2, i=2→3
```

### i=3: nums[3]=3
```
nums[3] = 3, val = 3
3 == 3 (target value) → Skip, no action

nums: [2, 2, 2, 3]
             ↑     ↑
             k=2, i=3 (end)
```

### Final Result
```
nums: [2, 2, _, _]
       ↑―――↑
       k=2 valid elements

return k = 2
```

## Complex Example Walkthrough

**Input:** `nums = [0, 1, 2, 2, 3, 0, 4, 2]`, `val = 2`

### Step-by-Step Trace

| i | nums[i] | nums[i]≠2? | Action | Array State After | k |
|---|---------|------------|--------|--------------------|---|
| 0 | 0 | ✅ Yes | nums[0]=0, k++ | [0,1,2,2,3,0,4,2] | 1 |
| 1 | 1 | ✅ Yes | nums[1]=1, k++ | [0,1,2,2,3,0,4,2] | 2 |
| 2 | 2 | ❌ No | Skip | [0,1,2,2,3,0,4,2] | 2 |
| 3 | 2 | ❌ No | Skip | [0,1,2,2,3,0,4,2] | 2 |
| 4 | 3 | ✅ Yes | nums[2]=3, k++ | [0,1,3,2,3,0,4,2] | 3 |
| 5 | 0 | ✅ Yes | nums[3]=0, k++ | [0,1,3,0,3,0,4,2] | 4 |
| 6 | 4 | ✅ Yes | nums[4]=4, k++ | [0,1,3,0,4,0,4,2] | 5 |
| 7 | 2 | ❌ No | Skip | [0,1,3,0,4,0,4,2] | 5 |

### Final Result
```
nums: [0, 1, 3, 0, 4, _, _, _]
       ↑―――――――――――――↑
       k=5 valid elements

return k = 5
```

**Verification**: All elements `≠ 2` are collected in first 5 positions ✓

## Visual Array Transformation

### Transformation Process
```
Step 0: [3, 2, 2, 3]  val=3, k=0
        ↑
      Start scanning

Step 1: [3, 2, 2, 3]  k=0 (3==3, skip)
           ↑
        Continue scanning

Step 2: [2, 2, 2, 3]  k=1 (2≠3, move to position 0)
           ↑  ↑
         k=1  i=2

Step 3: [2, 2, 2, 3]  k=2 (2≠3, move to position 1)
              ↑  ↑
            k=2  i=3

Step 4: [2, 2, 2, 3]  k=2 (3==3, skip)
              ↑     ↑
            k=2   i=4(end)

Final:  [2, 2, _, _]
        ↑―――↑
      Valid section
```

## Key Algorithm Insights

### 1. Why Overwriting is Safe
```python
# The invariant i >= k always holds
# This means we never overwrite unprocessed data

Example at i=4, k=2:
nums[2] = nums[4]  # Safe: copying from ahead to behind
```

### 2. Dual Role of k
```python
k = 0  # Initial state

# Role 1: Position indicator
nums[k] = nums[i]  # Where to place next valid element

# Role 2: Counter  
return k  # How many valid elements found
```

### 3. Two Pointers Pattern
```
Reading:  i → → → → → → → →
Writing:    k   k   k   k
           ↑   ↑   ↑   ↑
        Valid elements only
```

### 4. Order Changes are Allowed
```python
# Original: [0,1,2,2,3,0,4,2]  val=2
# Result:   [0,1,3,0,4,_,_,_]
#            ↑ ↑ ↑ ↑ ↑
# Notice: 3 moved before 0, but that's okay
```

## Alternative Approaches

### Approach 1: Create New Array (Not In-Place)
```python
def removeElement(self, nums, val):
    result = []
    for num in nums:
        if num != val:
            result.append(num)
    # Copy back to original array
    for i in range(len(result)):
        nums[i] = result[i]
    return len(result)
```
**Problems**: 
- Not truly in-place (creates additional array)
- Extra space complexity O(n)

### Approach 2: Element Shifting (Inefficient)
```python
def removeElement(self, nums, val):
    i = 0
    while i < len(nums):
        if nums[i] == val:
            # Shift all elements left
            for j in range(i, len(nums)-1):
                nums[j] = nums[j+1]
            # Don't increment i (check same position again)
        else:
            i += 1
    return i
```
**Problems**:
- Time complexity O(n²) due to nested shifting
- Much slower for arrays with many target values

### Approach 3: Backwards Iteration
```python
def removeElement(self, nums, val):
    i = len(nums) - 1
    while i >= 0:
        if nums[i] == val:
            # Swap with last element and "shrink" array
            nums[i] = nums[len(nums)-1]
            nums.pop()  # Reduces array size
        else:
            i -= 1
    return len(nums)
```
**Problems**:
- Modifies array size (violates some constraints)
- More complex logic

## Current Solution Advantages

### Two Pointers Forward Scan - Our Solution
```python
def removeElement(self, nums, val):
    k = 0
    for i in range(len(nums)):
        if nums[i] != val:
            nums[k] = nums[i]
            k += 1
    return k
```

**Advantages:**
- ✅ **Time: O(n)** - single pass through array
- ✅ **Space: O(1)** - only uses two pointer variables
- ✅ **True in-place** - no additional data structures
- ✅ **Simple logic** - easy to understand and implement
- ✅ **Stable for valid elements** - maintains relative order of kept elements

## Time & Space Complexity Analysis

### Current Solution
- **Time Complexity**: **O(n)** where n = length of array
  - Single pass through the entire array
  - Constant time operations per element
  - Each element examined exactly once

- **Space Complexity**: **O(1)** - constant extra space
  - Only uses two integer variables (`i`, `k`)
  - No additional data structures needed
  - True in-place modification

### Complexity Comparison
| Approach | Time | Space | In-Place? | Notes |
|----------|------|-------|-----------|-------|
| **Two Pointers** | **O(n)** | **O(1)** | ✅ | **Optimal** |
| Element Shifting | O(n²) | O(1) | ✅ | Too slow |
| New Array | O(n) | O(n) | ❌ | Extra space |
| Backwards + Pop | O(n) | O(1) | ❌ | Changes size |

## Edge Cases Handled

### Empty Array
```python
nums = [], val = 1
# Loop doesn't execute, return k=0
# Result: [], return 0
```

### All Elements are Target Value
```python
nums = [2, 2, 2, 2], val = 2
# No nums[i] != val conditions met
# Result: [_, _, _, _], return 0
```

### No Target Values
```python
nums = [1, 3, 5, 7], val = 2
# All elements kept in same positions
# Result: [1, 3, 5, 7], return 4
```

### Single Element
```python
nums = [1], val = 1 → [_], return 0
nums = [1], val = 2 → [1], return 1
```

### All Elements Different
```python
nums = [1, 2, 3, 4], val = 5
# Every element kept
# Result: [1, 2, 3, 4], return 4
```

## Common Pitfalls and Tips

### 1. Incrementing k Incorrectly
```python
# ❌ Wrong: Always incrementing k
for i in range(len(nums)):
    nums[k] = nums[i]
    k += 1  # This includes target values!

# ✅ Correct: Only increment when keeping element
for i in range(len(nums)):
    if nums[i] != val:
        nums[k] = nums[i]
        k += 1
```

### 2. Wrong Condition Check
```python
# ❌ Wrong: Checking for equality (removes wrong elements)
if nums[i] == val:
    nums[k] = nums[i]

# ✅ Correct: Checking for inequality (keeps correct elements)  
if nums[i] != val:
    nums[k] = nums[i]
```

### 3. Forgetting to Return k
```python
# ❌ Incomplete: Missing return statement
def removeElement(self, nums, val):
    k = 0
    # ... algorithm ...
    # Missing: return k

# ✅ Complete: Return the count
def removeElement(self, nums, val):
    k = 0
    # ... algorithm ...
    return k
```

### 4. Overcomplicating the Logic
```python
# ❌ Overcomplicated: Unnecessary conditions
if nums[i] != val:
    if k != i:  # Unnecessary check
        nums[k] = nums[i]
    k += 1

# ✅ Simple: Assignment always works
if nums[i] != val:
    nums[k] = nums[i]  # Safe even when k==i
    k += 1
```

## Key Programming Concepts Demonstrated

1. **Two Pointers Technique**: Read and write pointers moving independently
2. **In-Place Array Modification**: Modifying array without extra space
3. **Element Filtering**: Keeping elements that meet certain criteria
4. **Loop Invariants**: Maintaining `i >= k` throughout execution
5. **Safe Overwriting**: Understanding when array modifications are safe

## Practice Tips

1. **Trace through examples**: Walk through with small arrays step by step
2. **Understand pointer roles**: `i` reads all elements, `k` writes valid ones
3. **Test edge cases**: Empty array, all target, no target values
4. **Verify invariants**: Check that `i >= k` always holds
5. **Draw the transformation**: Visualize how array changes during execution

## Relationship to Similar Problems

### Comparison with Problem 26 (Remove Duplicates)
| Aspect | Remove Duplicates | Remove Element |
|--------|------------------|----------------|
| **Target** | Duplicate values | Specific value |
| **Comparison** | `nums[i] != nums[i-1]` | `nums[i] != val` |
| **Starting k** | k=1 (first always unique) | k=0 (check all) |
| **Pattern** | Same two-pointers technique | Same two-pointers technique |

### Common Two-Pointers Applications
1. **Array partitioning** (this problem)
2. **Duplicate removal** (problem 26)
3. **Array merging** (merge sorted arrays)
4. **Finding pairs** (two sum variants)

## Real-World Applications

1. **Data Filtering**: Removing unwanted records from datasets
2. **Array Compaction**: Eliminating null/invalid entries
3. **Memory Management**: Compacting fragmented data structures
4. **Stream Processing**: Filtering elements in real-time data streams
5. **Database Operations**: In-place record deletion/filtering

This algorithm demonstrates an efficient approach to in-place array modification using the two pointers technique, providing optimal time and space complexity for element removal operations.